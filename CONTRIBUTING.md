# Contribuer à paperwork-skills

Vous voulez ajouter un pays, un métier, ou corriger un chiffre ? Bienvenue. La règle d'or :
**une valeur sans source officielle n'est pas un fait.**

## Ajouter un pays en 7 étapes

1. **Copiez** `countries/_template` vers `countries/<code>` (code ISO 3166-1 alpha-2 en minuscules, avec sous-région si utile : `ca-qc`, `fr`, `tn`, `be-wal`).
2. **Remplissez `country.json`** : `code`, `name`, `language`, `currency`, `status` (`community` ou `experimental` au départ), `authorities`.
3. **Renommez** le dossier `skill-template` selon le métier (`fiscaliste`, `comptable-pme`, `notaire`...). Le `name` du `SKILL.md` doit être `<code-pays>-<dossier>`.
4. **Créez les fichiers `data/*.json`** : chaque valeur a `value`, `source`, `confidence`, et idéalement `display` (la chaîne exacte écrite dans `SKILL.md`).
5. **Écrivez `SKILL.md`** dans la langue du pays (déclarée dans `country.json`), avec : avertissement « pas un avis », règles absolues, fraîcheur des données, valeurs de référence, workflow, section `## Limites`.
6. **Ajoutez des evals** (au moins 3) dont au moins un piège (mauvaise hypothèse de l'utilisateur, année non couverte ou hors périmètre) et, si possible, un calculateur avec des tests dont les valeurs attendues sont calculées **à la main**.
7. **Lancez le validateur**, puis ouvrez une pull request :

```bash
pip install pyyaml
python tools/validate_skills.py
```

## Règles de contenu

- **Sources** : une source de type `official` est un site gouvernemental, un journal officiel ou une autorité fiscale. Une source de cabinet, de média ou de blog est `secondary`.
- **Niveaux de confiance** :
  - `official` : la valeur est écrite dans une source officielle que vous avez lue.
  - `secondary` : la valeur vient d'une source secondaire.
  - `unconfirmed` : déduction, ou sources en conflit. Une `note` commençant par `[Inférence]` ou `[Non confirmé]` est obligatoire.
- **Conflit de sources** : ne tranchez pas silencieusement. Documentez les deux versions et marquez `unconfirmed`.
- **Pas de lecture contournée** : si un site interdit la lecture automatisée (robots.txt), ne la contournez pas; notez la source comme « non lisible » et vérifiez-la à la main.
- **Ne copiez jamais de texte protégé par le droit d'auteur** : résumez et citez avec lien.
- **Pas de liens symboliques** (les installations par simple copie ou zip les cassent).
- **Statut `verified`** : réservé à un skill dont toutes les valeurs sont `official` **et** relu par une personne compétente (fiscaliste, comptable ou juriste du pays). Indiquez son nom dans `country.json`, champ `maintainers`.

## Nommage

- Dossier pays : code en minuscules (`ca-qc`, `ma`).
- Dossier skill : nom du métier, minuscules, tirets.
- `name` dans `SKILL.md` : `<code-pays>-<dossier>`.

## Frontmatter attendu

```yaml
---
name: ma-fiscaliste
description: |
  Description claire de ce que couvre le skill, avec mots déclencheurs et hors-scope.
metadata:
  country: ma
  language: fr
  last_updated: "2026-10-04"
  tax_year: "2026"
  status: partial-verified
license: MIT
---
```

## Mise à jour annuelle

Chaque loi de finances change les barèmes. Mettez à jour `data/*.json`, `SKILL.md`,
`last_updated` et `STATUS.md` ensemble; le validateur signale un `last_updated` de plus de
180 jours.

## Licence

En contribuant, vous acceptez que votre contribution soit publiée sous licence MIT.
