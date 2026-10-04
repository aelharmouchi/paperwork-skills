#!/usr/bin/env python3
"""
Calculateur déterministe de l'impôt sur le revenu (IR) — Maroc, barème annuel
(article 73-I du CGI, loi de finances 2025, applicable en 2026 sauf indication contraire).

Usage:
    python calc_ir_ma.py --revenu-net-imposable 120000
    python calc_ir_ma.py --revenu-net-imposable 120000 --personnes-a-charge 2
    python calc_ir_ma.py --salaire-brut-imposable 200000 --frais-pro --personnes-a-charge 1 --json

Ce que le script fait :
    - IR annuel selon le barème progressif (calculé de deux façons : tranche par
      tranche ET par la méthode « taux x revenu - somme à déduire »; les deux doivent
      coïncider, sinon le script s'arrête).
    - Réduction pour charges de famille (600 MAD par personne, 6 personnes max).
    - Optionnel : estimation des frais professionnels d'un salarié (--frais-pro),
      valeurs NON CONFIRMÉES (conflit de sources) : le script avertit.

Ce que le script NE fait PAS :
    - Détermination du revenu net imposable (cotisations CNSS/AMO, retraite, intérêts
      de prêt logement, autres déductions, abattements spécifiques).
    - Revenus fonciers, professionnels, agricoles, taux libératoires, MRE.
    - Régime de l'auto-entrepreneur, contribution sociale de solidarité.
    - Retenue à la source mensuelle (barème mensuel).

Les valeurs viennent de ../data/*.json.
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_values(data_dir):
    values = {}
    for path in sorted(Path(data_dir).glob("*.json")):
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        for key, leaf in doc.get("values", {}).items():
            if key in values:
                raise ValueError(f"Clé dupliquée : {key} ({path.name})")
            leaf = dict(leaf)
            leaf["_file"] = path.name
            values[key] = leaf
    return values


def v(values, key):
    return values[key]["value"]


def ir_par_tranches(revenu, brackets):
    if revenu <= 0:
        return 0.0
    impot, basse = 0.0, 0.0
    for t in brackets:
        haute = t["up_to"] if t["up_to"] is not None else float("inf")
        if revenu <= basse:
            break
        impot += (min(revenu, haute) - basse) * t["rate"]
        basse = haute
    return impot


def ir_par_somme_a_deduire(revenu, brackets):
    if revenu <= 0:
        return 0.0
    for t in brackets:
        haute = t["up_to"] if t["up_to"] is not None else float("inf")
        if revenu <= haute:
            return max(0.0, revenu * t["rate"] - t["deduction"])
    raise AssertionError("barème sans tranche supérieure")


def reduction_charges_famille(personnes, values):
    n = max(0, min(personnes, v(values, "family_charge_max_persons")))
    return min(n * v(values, "family_charge_per_person"), v(values, "family_charge_cap"))


def calcul_ir(revenu_net_imposable, personnes_a_charge, values):
    brackets = v(values, "ir_brackets")
    a = ir_par_tranches(revenu_net_imposable, brackets)
    b = ir_par_somme_a_deduire(revenu_net_imposable, brackets)
    if abs(a - b) > 0.01:
        raise AssertionError(f"Incohérence barème : tranches={a:.2f} vs somme à déduire={b:.2f}")
    reduction = reduction_charges_famille(personnes_a_charge, values)
    net = max(0.0, a - reduction)
    taux_marg = 0.0
    for t in brackets:
        haute = t["up_to"] if t["up_to"] is not None else float("inf")
        if revenu_net_imposable <= haute:
            taux_marg = t["rate"]
            break
    return {
        "revenu_net_imposable": revenu_net_imposable,
        "ir_brut": round(a, 2),
        "reduction_charges_famille": reduction,
        "ir_net": round(net, 2),
        "taux_moyen": round(net / revenu_net_imposable, 6) if revenu_net_imposable > 0 else 0.0,
        "taux_marginal": taux_marg,
    }


def frais_professionnels(brut_imposable, values):
    """Estimation NON CONFIRMÉE (voir data/deductions-et-retenues-2026.json)."""
    seuil = v(values, "frais_pro_threshold")
    taux = v(values, "frais_pro_rate_low") if brut_imposable <= seuil else v(values, "frais_pro_rate_high")
    return min(brut_imposable * taux, v(values, "frais_pro_cap"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--revenu-net-imposable", type=float, help="Revenu net imposable annuel (MAD)")
    g.add_argument("--salaire-brut-imposable", type=float,
                   help="Salaire brut imposable annuel (MAD), avec --frais-pro")
    p.add_argument("--frais-pro", action="store_true", help="Déduire les frais professionnels (non confirmé)")
    p.add_argument("--personnes-a-charge", type=int, default=0)
    p.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    values = load_values(args.data_dir)
    out = {}
    if args.salaire_brut_imposable is not None:
        if not args.frais_pro:
            p.error("--salaire-brut-imposable exige --frais-pro (sinon utiliser --revenu-net-imposable)")
        fp = frais_professionnels(args.salaire_brut_imposable, values)
        revenu = args.salaire_brut_imposable - fp
        out["frais_professionnels"] = round(fp, 2)
        print("AVERTISSEMENT [Non confirmé] frais professionnels : sources en conflit "
              "(35 %/25 % plafonné à 35 000 MAD selon LF 2023 vs 20 % selon d'autres sites).",
              file=sys.stderr)
    else:
        revenu = args.revenu_net_imposable
    out["ir"] = calcul_ir(revenu, args.personnes_a_charge, values)

    if "ir_brackets" in values and values["ir_brackets"]["confidence"] != "official":
        print("AVERTISSEMENT barème non officiel", file=sys.stderr)
    if values["family_charge_per_person"]["confidence"] != "official":
        print("AVERTISSEMENT [Source secondaire] réduction pour charges de famille (600 MAD).",
              file=sys.stderr)

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    i = out["ir"]
    if "frais_professionnels" in out:
        print(f"Frais professionnels (estimation non confirmée) : {out['frais_professionnels']:,.2f} MAD")
    print(f"Revenu net imposable   : {i['revenu_net_imposable']:,.2f} MAD")
    print(f"IR brut                : {i['ir_brut']:,.2f} MAD")
    print(f"Charges de famille     : -{i['reduction_charges_famille']:,.2f} MAD")
    print(f"IR net                 : {i['ir_net']:,.2f} MAD")
    print(f"Taux moyen {i['taux_moyen']:.2%} | taux marginal {i['taux_marginal']:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
