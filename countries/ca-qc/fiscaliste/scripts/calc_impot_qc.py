#!/usr/bin/env python3
"""
Calculateur déterministe d'impôt sur le revenu des particuliers — Québec, année 2026.

Usage:
    python calc_impot_qc.py --revenu-imposable 75000
    python calc_impot_qc.py --revenu-imposable 75000 --json
    python calc_impot_qc.py --salaire-brut 80000 --cotisations

Ce que le script fait :
    - Impôt fédéral : barème, crédit personnel de base (avec réduction progressive),
      abattement du Québec (16,5 % de l'impôt fédéral de base).
    - Impôt du Québec : barème, crédit personnel de base.
    - Cotisations salariales RRQ, RQAP, AE (Québec) sur un salaire brut.
    - Part imposable d'un gain en capital (taux d'inclusion).

Ce que le script NE fait PAS (à traiter manuellement ou à signaler) :
    - Autres crédits non remboursables (âge, pensions, frais médicaux, dons, etc.).
    - Déduction pour cotisations supplémentaires RRQ, déduction du REER : le
      revenu imposable doit être fourni après déductions.
    - Dividendes (majoration et crédits), prestations (Allocation canadienne
      pour enfants, Solidarité, Prime au travail), impôt minimum de remplacement.
    - Revenu familial, fractionnement.

Les valeurs viennent de ../data/*.json. Pour une autre année, fournir --data-dir.
Le champ "confidence" de chaque valeur indique si elle est officielle,
secondaire ou non confirmée; le script en avertit sur stderr.
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_values(data_dir):
    """Charge tous les fichiers data/*.json et retourne {clé: feuille}."""
    values = {}
    for path in sorted(Path(data_dir).glob("*.json")):
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        for key, leaf in doc.get("values", {}).items():
            if key in values:
                raise ValueError(f"Clé dupliquée dans les données : {key} ({path.name})")
            leaf = dict(leaf)
            leaf["_file"] = path.name
            values[key] = leaf
    return values


def v(values, key):
    return values[key]["value"]


def impot_par_tranches(revenu, tranches):
    """Applique un barème progressif. tranches = [{'up_to': n|None, 'rate': r}, ...]."""
    if revenu <= 0:
        return 0.0
    impot = 0.0
    borne_basse = 0.0
    for t in tranches:
        haute = t["up_to"] if t["up_to"] is not None else float("inf")
        if revenu <= borne_basse:
            break
        base = min(revenu, haute) - borne_basse
        impot += base * t["rate"]
        borne_basse = haute
    return impot


def tranche_marginale(revenu, tranches):
    borne_basse = 0.0
    for t in tranches:
        haute = t["up_to"] if t["up_to"] is not None else float("inf")
        if revenu <= haute:
            return t["rate"]
        borne_basse = haute
    return tranches[-1]["rate"]


def montant_personnel_federal(revenu_net, values):
    """Montant personnel de base fédéral, réduit linéairement entre deux seuils."""
    mx = v(values, "federal_bpa_max")
    mn = v(values, "federal_bpa_min")
    debut = v(values, "federal_bpa_phaseout_start")
    fin = v(values, "federal_bpa_phaseout_end")
    if revenu_net <= debut:
        return float(mx)
    if revenu_net >= fin:
        return float(mn)
    return mx - (mx - mn) * (revenu_net - debut) / (fin - debut)


def calcul_federal(revenu_imposable, values):
    brut = impot_par_tranches(revenu_imposable, v(values, "federal_brackets"))
    bpa = montant_personnel_federal(revenu_imposable, values)
    credit = bpa * v(values, "federal_credit_rate")
    base = max(0.0, brut - credit)
    abattement = base * v(values, "quebec_abatement_rate")
    net = base - abattement
    return {
        "impot_brut": brut,
        "montant_personnel_de_base": bpa,
        "credit_personnel_de_base": credit,
        "impot_federal_de_base": base,
        "abattement_du_quebec": abattement,
        "impot_federal_net": net,
    }


def calcul_quebec(revenu_imposable, values):
    brut = impot_par_tranches(revenu_imposable, v(values, "quebec_brackets"))
    credit = v(values, "quebec_bpa") * v(values, "quebec_credit_rate")
    net = max(0.0, brut - credit)
    return {
        "impot_brut": brut,
        "credit_personnel_de_base": credit,
        "impot_quebec_net": net,
    }


def calcul_impot(revenu_imposable, values):
    fed = calcul_federal(revenu_imposable, values)
    qc = calcul_quebec(revenu_imposable, values)
    total = fed["impot_federal_net"] + qc["impot_quebec_net"]
    marginal = (
        tranche_marginale(revenu_imposable, v(values, "federal_brackets"))
        * (1 - v(values, "quebec_abatement_rate"))
        + tranche_marginale(revenu_imposable, v(values, "quebec_brackets"))
    )
    return {
        "revenu_imposable": revenu_imposable,
        "federal": fed,
        "quebec": qc,
        "impot_total": total,
        "taux_moyen": total / revenu_imposable if revenu_imposable > 0 else 0.0,
        "taux_marginal_combine": marginal,
    }


def cotisations_salariales(salaire_brut, values):
    """Cotisations de l'employé (RRQ, RQAP, AE Québec). Arrondies au cent."""
    exemption = v(values, "rrq_basic_exemption")
    mgap = v(values, "rrq_max_pensionable_earnings")
    taux = v(values, "rrq_base_plus_first_additional_rate")
    gains_cot = max(0.0, min(salaire_brut, mgap) - exemption)
    rrq_base = min(gains_cot * taux, v(values, "rrq_max_contribution_base_first_additional"))

    haut2 = v(values, "rrq_second_additional_upper_limit")
    gains_2 = max(0.0, min(salaire_brut, haut2) - mgap)
    rrq_2 = min(gains_2 * v(values, "rrq_second_additional_rate"),
                v(values, "rrq_second_additional_max"))

    rqap = min(min(salaire_brut, v(values, "rqap_max_insurable_earnings"))
               * v(values, "rqap_employee_rate"), v(values, "rqap_employee_max"))
    ae = min(min(salaire_brut, v(values, "ae_max_insurable_earnings"))
             * v(values, "ae_employee_rate_qc"), v(values, "ae_employee_max_qc"))
    out = {
        "rrq_base_et_premiere_supplementaire": round(rrq_base, 2),
        "rrq_deuxieme_supplementaire": round(rrq_2, 2),
        "rqap": round(rqap, 2),
        "ae": round(ae, 2),
    }
    out["total"] = round(sum(out.values()), 2)
    return out


def gain_en_capital_imposable(gain, values):
    return gain * v(values, "capital_gains_inclusion_rate")


def avertissements_confiance(values, cles):
    msgs = []
    for k in cles:
        leaf = values.get(k)
        if leaf and leaf.get("confidence") != "official":
            msgs.append(f"[{leaf['confidence']}] {k} ({leaf['_file']})")
    return msgs


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--revenu-imposable", type=float, help="Revenu imposable après déductions (CAD)")
    p.add_argument("--salaire-brut", type=float, help="Salaire brut annuel (pour les cotisations)")
    p.add_argument("--cotisations", action="store_true", help="Calculer aussi RRQ/RQAP/AE")
    p.add_argument("--gain-capital", type=float, help="Gain en capital réalisé (part imposable)")
    p.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    values = load_values(args.data_dir)
    result = {}
    used = []

    if args.revenu_imposable is not None:
        result["impot"] = calcul_impot(args.revenu_imposable, values)
        used += ["federal_brackets", "quebec_brackets", "federal_bpa_max", "federal_bpa_min",
                 "federal_bpa_phaseout_start", "federal_bpa_phaseout_end", "federal_credit_rate",
                 "quebec_bpa", "quebec_credit_rate", "quebec_abatement_rate"]
    if args.salaire_brut is not None and args.cotisations:
        result["cotisations"] = cotisations_salariales(args.salaire_brut, values)
        used += ["rrq_second_additional_upper_limit"]
    if args.gain_capital is not None:
        result["gain_capital_imposable"] = gain_en_capital_imposable(args.gain_capital, values)
        used += ["capital_gains_inclusion_rate"]

    if not result:
        p.error("Fournir --revenu-imposable, --salaire-brut --cotisations ou --gain-capital")

    for m in avertissements_confiance(values, used):
        print(f"AVERTISSEMENT valeur non officielle : {m}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if "impot" in result:
        i = result["impot"]
        f, q = i["federal"], i["quebec"]
        print(f"Revenu imposable : {i['revenu_imposable']:,.2f} $")
        print("— Fédéral —")
        print(f"  Impôt brut (barème)            : {f['impot_brut']:,.2f} $")
        print(f"  Crédit personnel de base       : -{f['credit_personnel_de_base']:,.2f} $ (montant {f['montant_personnel_de_base']:,.0f} $)")
        print(f"  Impôt fédéral de base          : {f['impot_federal_de_base']:,.2f} $")
        print(f"  Abattement du Québec           : -{f['abattement_du_quebec']:,.2f} $")
        print(f"  Impôt fédéral net              : {f['impot_federal_net']:,.2f} $")
        print("— Québec —")
        print(f"  Impôt brut (barème)            : {q['impot_brut']:,.2f} $")
        print(f"  Crédit personnel de base       : -{q['credit_personnel_de_base']:,.2f} $")
        print(f"  Impôt du Québec net            : {q['impot_quebec_net']:,.2f} $")
        print(f"TOTAL                            : {i['impot_total']:,.2f} $")
        print(f"Taux moyen {i['taux_moyen']:.2%} | taux marginal combiné {i['taux_marginal_combine']:.2%}")
    if "cotisations" in result:
        c = result["cotisations"]
        print("Cotisations salariales :", json.dumps(c, ensure_ascii=False))
    if "gain_capital_imposable" in result:
        print(f"Gain en capital imposable : {result['gain_capital_imposable']:,.2f} $")
    return 0


if __name__ == "__main__":
    sys.exit(main())
