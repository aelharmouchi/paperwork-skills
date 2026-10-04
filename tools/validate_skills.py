#!/usr/bin/env python3
"""
Validateur de skills — paperwork-skills.

Vérifie, pour chaque skill sous countries/<code>/<skill>/ :
  1. SKILL.md avec frontmatter valide (name, description, metadata.*).
  2. name == "<code-pays>-<dossier>" (unicité globale).
  3. Le champ metadata.country correspond au dossier du pays.
  4. last_updated au format AAAA-MM-JJ (avertissement si > 180 jours).
  5. Section "## Limites" présente et avertissement (« pas un avis ») présent.
  6. Tous les liens relatifs de SKILL.md pointent vers des fichiers existants.
  7. Chaque data/*.json a _meta, sources, values; chaque valeur a une source
     connue et un niveau de confiance cohérent :
        - confidence "official"  => la source doit être de type "official"
        - confidence "secondary" => la source doit être "secondary" ou "official"
        - confidence "unconfirmed" => une "note" obligatoire (étiquette [Inférence]
          ou [Non confirmé])
  8. Chaque valeur avec "display" apparaît telle quelle dans SKILL.md
     (empêche qu'un chiffre du SKILL.md diverge du JSON).
  9. Chaque source a une URL https.
 10. evals/evals.json existe avec >= 3 évals, chacune avec "assertions".
 11. Aucun lien symbolique (installation par upload cassée).
 12. Si status == "verified", aucune valeur "unconfirmed" ni "secondary".

Chaque pays doit avoir country.json (code, name, language, status).

Usage :  python tools/validate_skills.py [--strict]
  --strict : les avertissements deviennent des erreurs.
Code de sortie : 0 si OK, 1 sinon.
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML requis : pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "countries"
ALLOWED_STATUS = {"verified", "partial-verified", "community", "experimental"}
CONFIDENCE = {"official", "secondary", "unconfirmed"}
FRESHNESS_DAYS = 180
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)]+)\)")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"ERREUR  {where} : {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"AVERT.  {where} : {msg}")


def parse_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)), text[m.end():]


def check_country(cdir, rep):
    cj = cdir / "country.json"
    where = str(cdir.relative_to(ROOT))
    if not cj.exists():
        rep.err(where, "country.json manquant")
        return None
    try:
        data = json.loads(cj.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.err(where, f"country.json invalide : {e}")
        return None
    for k in ("code", "name", "language", "status"):
        if k not in data:
            rep.err(where, f"country.json : champ '{k}' manquant")
    if data.get("code") != cdir.name:
        rep.err(where, f"country.json code '{data.get('code')}' != dossier '{cdir.name}'")
    if data.get("status") not in ALLOWED_STATUS:
        rep.err(where, f"country.json status invalide : {data.get('status')}")
    return data


def check_data_file(path, skill_text, skill_status, rep):
    where = str(path.relative_to(ROOT))
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.err(where, f"JSON invalide : {e}")
        return
    for k in ("_meta", "sources", "values"):
        if k not in doc:
            rep.err(where, f"clé '{k}' manquante")
            return
    sources = {}
    for s in doc["sources"]:
        sid = s.get("id")
        if not sid:
            rep.err(where, "source sans id")
            continue
        if sid in sources:
            rep.err(where, f"source dupliquée : {sid}")
        sources[sid] = s
        if not str(s.get("url", "")).startswith("https://"):
            rep.err(where, f"source {sid} : URL https:// manquante")
        if s.get("authority") not in {"official", "secondary"}:
            rep.err(where, f"source {sid} : authority doit être official|secondary")
        if not s.get("fetched"):
            rep.err(where, f"source {sid} : date 'fetched' manquante")
    for key, leaf in doc["values"].items():
        loc = f"{where}:{key}"
        if "value" not in leaf:
            rep.err(loc, "champ 'value' manquant")
        src = sources.get(leaf.get("source"))
        if src is None:
            rep.err(loc, f"source inconnue : {leaf.get('source')}")
            continue
        conf = leaf.get("confidence")
        if conf not in CONFIDENCE:
            rep.err(loc, f"confidence invalide : {conf}")
            continue
        if conf == "official" and src["authority"] != "official":
            rep.err(loc, "confidence 'official' avec une source non officielle")
        if conf == "secondary" and src["authority"] not in {"official", "secondary"}:
            rep.err(loc, "confidence 'secondary' incohérente avec la source")
        if conf == "unconfirmed":
            note = leaf.get("note", "")
            if "[Inférence]" not in note and "[Non confirmé]" not in note:
                rep.err(loc, "valeur 'unconfirmed' sans note étiquetée [Inférence] ou [Non confirmé]")
        if skill_status == "verified" and conf != "official":
            rep.err(loc, f"skill 'verified' contient une valeur '{conf}'")
        disp = leaf.get("display")
        if disp and disp not in skill_text:
            rep.err(loc, f"valeur affichée « {disp} » absente de SKILL.md (divergence possible)")


def check_skill(cdir, sdir, rep):
    where = str(sdir.relative_to(ROOT))
    skill_md = sdir / "SKILL.md"
    if not skill_md.exists():
        rep.err(where, "SKILL.md manquant")
        return
    text = skill_md.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except yaml.YAMLError as e:
        rep.err(where, f"frontmatter YAML invalide : {e}")
        return
    if fm is None:
        rep.err(where, "frontmatter manquant (--- ... ---)")
        return

    expected_name = f"{cdir.name}-{sdir.name}"
    if fm.get("name") != expected_name:
        rep.err(where, f"name '{fm.get('name')}' != '{expected_name}'")
    if not str(fm.get("description", "")).strip():
        rep.err(where, "description vide")
    elif len(str(fm["description"])) > 1024:
        rep.warn(where, "description > 1024 caractères")
    md = fm.get("metadata") or {}
    for k in ("country", "language", "last_updated", "status"):
        if k not in md:
            rep.err(where, f"metadata.{k} manquant")
    if md.get("country") != cdir.name:
        rep.err(where, f"metadata.country '{md.get('country')}' != '{cdir.name}'")
    if md.get("status") not in ALLOWED_STATUS:
        rep.err(where, f"metadata.status invalide : {md.get('status')}")
    lu = str(md.get("last_updated", ""))
    try:
        d = datetime.strptime(lu, "%Y-%m-%d").date()
        age = (date.today() - d).days
        if age > FRESHNESS_DAYS:
            rep.warn(where, f"last_updated vieux de {age} jours (> {FRESHNESS_DAYS})")
        if age < 0:
            rep.err(where, "last_updated dans le futur")
    except ValueError:
        rep.err(where, f"last_updated doit être AAAA-MM-JJ (reçu : {lu!r})")

    if "## Limites" not in body:
        rep.err(where, "section '## Limites' manquante")
    if not re.search(r"pas un avis|not (a|an) .{0,20}advice", body, re.I):
        rep.err(where, "avertissement « pas un avis » manquant")

    for link in LINK_RE.findall(body):
        target = (sdir / link.split("#")[0]).resolve()
        if not target.exists():
            rep.err(where, f"lien relatif cassé : {link}")

    data_dir = sdir / "data"
    if data_dir.is_dir():
        for p in sorted(data_dir.glob("*.json")):
            check_data_file(p, text, md.get("status"), rep)
    else:
        rep.warn(where, "pas de dossier data/")

    evals = sdir / "evals" / "evals.json"
    if not evals.exists():
        rep.err(where, "evals/evals.json manquant")
    else:
        try:
            ev = json.loads(evals.read_text(encoding="utf-8")).get("evals", [])
            if len(ev) < 3:
                rep.err(where, f"au moins 3 évals requis (trouvé {len(ev)})")
            for e in ev:
                if not e.get("assertions"):
                    rep.err(where, f"eval {e.get('id')} sans assertions")
                if not e.get("prompt"):
                    rep.err(where, f"eval {e.get('id')} sans prompt")
        except json.JSONDecodeError as e:
            rep.err(where, f"evals.json invalide : {e}")

    for p in sdir.rglob("*"):
        if p.is_symlink():
            rep.err(str(p.relative_to(ROOT)), "lien symbolique interdit")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    rep = Report()
    seen_names = set()
    n_skills = 0

    for cdir in sorted(p for p in COUNTRIES.iterdir() if p.is_dir() and not p.name.startswith("_")):
        if check_country(cdir, rep) is None:
            continue
        for sdir in sorted(p for p in cdir.iterdir() if p.is_dir()):
            if not (sdir / "SKILL.md").exists() and not (sdir / "data").exists():
                continue
            n_skills += 1
            check_skill(cdir, sdir, rep)
            seen_names.add(f"{cdir.name}-{sdir.name}")

    for line in rep.warnings + rep.errors:
        print(line)
    print(f"\n{n_skills} skill(s) vérifié(s) : {len(rep.errors)} erreur(s), {len(rep.warnings)} avertissement(s).")
    fail = bool(rep.errors) or (args.strict and bool(rep.warnings))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
