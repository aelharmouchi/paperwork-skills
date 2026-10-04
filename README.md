# paperwork-skills

**Des skills pour agents IA qui comprennent la paperasse fiscale et administrative, pays par pays.**
*AI agent skills for tax and administrative paperwork, country by country.*

Chaque skill est un dossier de Markdown et de données JSON qu'un agent (Claude, Codex, Cursor, etc.) peut lire pour répondre avec **des chiffres sourcés, des calculs montrés étape par étape et une incertitude étiquetée**. Le projet s'inspire de [Paperasse](https://github.com/romainsimon/paperasse) (France) et l'étend à plusieurs pays.

> **Avertissement / Disclaimer.** Ces skills sont des outils d'aide à la compréhension, **pas un avis fiscal, juridique ou comptable**. Seules les autorités compétentes font foi. *These skills are not tax, legal or accounting advice.*

## Pays disponibles

| Code | Pays | Skills | Statut |
|---|---|---|---|
| `ca-qc` | Canada — Québec | `fiscaliste` (IR fédéral + QC, REER/CELI/CELIAPP, cotisations) | partial-verified |
| `ma` | Maroc (المغرب) | `fiscaliste` (IR, charges de famille, retenue sur loyers) | partial-verified |

Le détail de ce qui est vérifié, secondaire ou non confirmé est dans [STATUS.md](STATUS.md).
**Ajoutez votre pays** : voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Ce qui distingue ce projet

1. **Chaque valeur a une source et un niveau de confiance** (`official`, `secondary`, `unconfirmed`) dans `data/*.json`. Un skill ne peut pas être marqué `verified` s'il contient une valeur non officielle.
2. **Étiquettes d'incertitude obligatoires** dans les réponses : `[Source secondaire]`, `[Inférence]`, `[Non confirmé]`.
3. **Un validateur automatique** (`tools/validate_skills.py`) refuse un skill dont un chiffre du `SKILL.md` diverge du JSON, dont un lien est cassé, ou dont une source manque.
4. **Des calculateurs déterministes** testés contre des calculs faits à la main, plutôt que de laisser le modèle faire l'arithmétique.
5. **Des evals** qui incluent des pièges (mauvais taux cité par l'utilisateur, année non couverte, hors périmètre).
6. **Pas de liens symboliques** : chaque skill est autonome et s'installe par simple copie de dossier.

## Structure

```
paperwork-skills/
├── countries/
│   ├── ca-qc/
│   │   ├── country.json
│   │   └── fiscaliste/   SKILL.md, data/, references/, scripts/, tests/, evals/
│   ├── ma/
│   │   └── fiscaliste/
│   └── _template/        modèle à copier pour un nouveau pays
├── core/                 format SKILL.md et règles communes
├── tools/                validate_skills.py
├── STATUS.md             niveau de vérification par pays
└── marketplace.json
```

Le nom d'un skill est `<code-pays>-<dossier>` (ex. `ca-qc-fiscaliste`).

## Installation

**Claude Code** : copier le dossier du skill voulu (par exemple `countries/ca-qc/fiscaliste`) dans `~/.claude/skills/ca-qc-fiscaliste`.

**Autres agents** : copier le dossier dans le répertoire de skills de l'outil, ou demander à l'agent de lire `SKILL.md` du dossier.

**Claude (Desktop/Web)** : compresser le dossier du skill en `.zip` avec `SKILL.md` à la racine du zip, puis le téléverser dans les paramètres (exécution de code activée).

## Exemples

```
> Je vis au Québec, revenu imposable 75 000 $ en 2026. Calcule mon impôt fédéral et provincial.
> Le plafond REER est de 33 810 $, je gagne 60 000 $ : je peux cotiser 33 810 $ ?
> Au Maroc, revenu net imposable 120 000 MAD, 2 enfants à charge : quel est mon IR ?
> Quel est le taux des frais professionnels d'un salarié marocain ?   (réponse attendue : étiquette d'incertitude)
```

## Développement

```bash
pip install pyyaml
python tools/validate_skills.py          # validation de tous les skills
python -m unittest discover -s countries/ca-qc/fiscaliste/tests
python -m unittest discover -s countries/ma/fiscaliste/tests
```

## Licence

MIT. Voir [LICENSE](LICENSE).

---

## English summary

`paperwork-skills` is a multi-country collection of AI-agent skills for tax and administrative paperwork. Each value in the data files carries a source URL and a confidence level (`official`, `secondary`, `unconfirmed`); an automated validator enforces consistency between `SKILL.md`, JSON data, links and sources. Contributions of new countries are welcome: copy `countries/_template`, fill it in, and open a pull request. Skill content is written in the country's main language (declared in `country.json`).
