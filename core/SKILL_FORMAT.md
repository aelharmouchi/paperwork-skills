# Format d'un skill — règles communes

## Arborescence

```
countries/<code>/<skill>/
├── SKILL.md              obligatoire
├── data/*.json           valeurs sourcées (recommandé)
├── references/*.md       fiches détaillées liées depuis SKILL.md
├── scripts/              calculateurs déterministes (optionnel)
├── tests/                tests des scripts (si scripts)
└── evals/evals.json      au moins 3 évals, dont un piège
```

## Frontmatter de SKILL.md

Champs obligatoires : `name` (`<code-pays>-<dossier>`), `description`, `metadata.country`,
`metadata.language`, `metadata.last_updated` (AAAA-MM-JJ), `metadata.status`.
Champs recommandés : `metadata.tax_year`, `license`.

## Contenu minimal de SKILL.md

1. Avertissement « pas un avis ».
2. Règles absolues (séquence de calcul, pas de barème inventé, étiquettes d'incertitude).
3. Fraîcheur des données.
4. Valeurs de référence (chaque `display` des JSON y apparaît).
5. Workflow et table des références.
6. Section `## Limites`.

## Fichiers de données

```json
{
  "_meta": { "country": "xx", "tax_year": 2026, "last_verified": "AAAA-MM-JJ", "note": "..." },
  "sources": [
    { "id": "...", "title": "...", "url": "https://...", "authority": "official|secondary", "fetched": "AAAA-MM-JJ" }
  ],
  "values": {
    "cle": { "value": 0, "source": "<id>", "confidence": "official|secondary|unconfirmed", "display": "texte exact", "note": "..." }
  }
}
```

Règles : `official` exige une source `official`; `unconfirmed` exige une `note` avec
`[Inférence]` ou `[Non confirmé]`; un skill `verified` ne contient que des valeurs `official`.

## Évals

Chaque éval : `id`, `name`, `prompt`, `expected_output`, `assertions[]`. Champ optionnel
`calc` : `{ "args": [...], "expect": { "chemin.json": valeur } }` pour relier l'éval à la
sortie réelle du calculateur.

## Étiquettes d'incertitude (dans les réponses de l'agent)

- `[Source secondaire]` : valeur lue sur une source non officielle.
- `[Inférence]` : déduction non confirmée.
- `[Non confirmé]` : information non vérifiable ou en conflit.
