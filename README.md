<p align="center">
  <img src="assets/banner.svg" alt="paperwork-skills : skills pour agents IA, paperasse fiscale pays par pays" width="100%">
</p>

<p align="center">
  <a href="https://github.com/aelharmouchi/paperwork-skills/actions/workflows/validate.yml"><img src="https://github.com/aelharmouchi/paperwork-skills/actions/workflows/validate.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-blue" alt="Licence MIT"></a>
  <a href="STATUS.md"><img src="https://img.shields.io/badge/version-0.1.0-orange" alt="Version 0.1.0"></a>
  <a href="STATUS.md"><img src="https://img.shields.io/badge/statut-partiellement%20v%C3%A9rifi%C3%A9-yellow" alt="Statut partiellement vérifié"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-bienvenues-brightgreen" alt="PRs bienvenues"></a>
</p>

<p align="center">
  <b>Des skills pour agents IA qui connaissent la paperasse fiscale, pays par pays,<br>et qui disent clairement ce qu'ils savent et ce qu'ils ne savent pas.</b>
</p>

---

## En bref

Un skill est un dossier de Markdown et de données JSON qu'un agent IA (Claude, Codex, Cursor, etc.) lit pour répondre à une question de fiscalité. Ici, chaque valeur (taux, plafond, seuil) est **liée à sa source** et porte un **niveau de confiance**. Quand une information n'est pas vérifiée, l'agent doit l'écrire : `[Source secondaire]`, `[Inférence]`, `[Non confirmé]`.

Le projet s'inspire de [Paperasse](https://github.com/romainsimon/paperasse) (France) et le généralise à plusieurs pays, avec un format commun et un validateur automatique pour que d'autres puissent ajouter le leur.

> [!WARNING]
> **Version 0.1 : partiellement vérifiée.** Ces skills sont un outil d'aide à la compréhension, **pas un avis fiscal, juridique ou comptable**. Plusieurs valeurs viennent de sources secondaires et sont étiquetées comme telles. Voir [STATUS.md](STATUS.md) pour le détail. Seules les autorités fiscales font foi.

## Pays disponibles

| | Pays | Skill | Contenu | Statut |
|---|---|---|---|---|
| 🇨🇦 | **Canada — Québec** (`ca-qc`) | [`fiscaliste`](countries/ca-qc/fiscaliste/SKILL.md) | Impôt fédéral + Québec 2026, abattement du Québec, REER, CELI, CELIAPP, cotisations RRQ, RQAP, AE | partiellement vérifié |
| 🇲🇦 | **Maroc — المغرب** (`ma`) | [`fiscaliste`](countries/ma/fiscaliste/SKILL.md) | Barème de l'IR, charges de famille, retenue sur loyers | partiellement vérifié |
| ➕ | **Votre pays** | | [Ajouter un pays en 7 étapes](CONTRIBUTING.md) | |

## Exemple

Question à l'agent : *« Je vis au Québec, revenu imposable 75 000 $ en 2026. Combien d'impôt ? »*

Le skill montre la séquence complète et vérifie le résultat avec un calculateur déterministe :

```text
$ python countries/ca-qc/fiscaliste/scripts/calc_impot_qc.py --revenu-imposable 75000
Revenu imposable : 75,000.00 $
— Fédéral —
  Impôt brut (barème)            : 11,571.01 $
  Crédit personnel de base       : -2,303.28 $ (montant 16,452 $)
  Impôt fédéral de base          : 9,267.73 $
  Abattement du Québec           : -1,529.17 $
  Impôt fédéral net              : 7,738.55 $
— Québec —
  Impôt brut (barème)            : 11,532.75 $
  Crédit personnel de base       : -2,653.00 $
  Impôt du Québec net            : 8,879.75 $
TOTAL                            : 16,618.30 $
```

Le script avertit aussi sur la sortie d'erreur quand une valeur utilisée n'est pas officielle (par exemple le montant personnel de base du Québec, de source secondaire).

## Ce qui distingue ce projet

| Principe | Mise en oeuvre |
|---|---|
| **Chaque valeur est sourcée** | `data/*.json` : URL, date de consultation, `official` / `secondary` / `unconfirmed` |
| **L'incertitude est dite** | Étiquettes obligatoires dans les réponses ; un skill `verified` ne peut contenir que des valeurs officielles |
| **Pas de dérive silencieuse** | [`tools/validate_skills.py`](tools/validate_skills.py) refuse un chiffre du `SKILL.md` qui diverge du JSON, un lien cassé ou une source manquante |
| **Les calculs ne sont pas laissés au modèle** | Calculateurs testés contre des calculs faits à la main |
| **Des pièges dans les evals** | Mauvais taux cité par l'utilisateur, année non couverte, cas hors périmètre |
| **Installation simple** | Pas de liens symboliques : un skill = un dossier autonome |

## Installation

**Claude Code** : copier le dossier du skill (par exemple `countries/ca-qc/fiscaliste`) dans `~/.claude/skills/ca-qc-fiscaliste/`.

**Autres agents** : copier le dossier dans le répertoire de skills de l'outil, ou demander à l'agent de lire le `SKILL.md` du dossier.

**Claude Desktop / Web** : compresser le dossier du skill en `.zip` avec `SKILL.md` à la racine, puis le téléverser dans les paramètres.

> Les chemins d'installation suivent la logique de Paperasse et n'ont pas été testés sur chaque outil `[Non confirmé]`.

## Structure

```text
paperwork-skills/
├── countries/
│   ├── ca-qc/                 Canada — Québec
│   │   ├── country.json
│   │   └── fiscaliste/        SKILL.md, data/, references/, scripts/, tests/, evals/
│   ├── ma/                    Maroc
│   │   └── fiscaliste/
│   └── _template/             modèle à copier pour un nouveau pays
├── core/SKILL_FORMAT.md       format commun
├── tools/validate_skills.py   validateur
├── STATUS.md                  niveau de vérification, valeur par valeur
└── marketplace.json
```

Le nom d'un skill est `<code-pays>-<dossier>` (ex. `ca-qc-fiscaliste`).

## Feuille de route

- [ ] `ca-qc / comptable-pme` : TPS et TVQ, DAS, incorporation
- [ ] `ma / comptable-pme` : PCGE, IS, TVA, CNSS, auto-entrepreneur
- [ ] Lanceur d'evals contre un agent, pour mesurer l'apport réel des skills
- [ ] Confirmer les valeurs secondaires auprès de sources officielles (liste dans [STATUS.md](STATUS.md))
- [ ] Relecture par un professionnel de chaque pays, pour passer en `verified`
- [ ] Nouveaux pays : [ouvrir une proposition](https://github.com/aelharmouchi/paperwork-skills/issues/new/choose)

## Contribuer

Les contributions sont bienvenues : un nouveau pays, un nouveau métier, ou la correction d'un chiffre. La règle d'or : **une valeur sans source officielle n'est pas un fait**.

- [CONTRIBUTING.md](CONTRIBUTING.md) : ajouter un pays en 7 étapes
- [Signaler une valeur incorrecte](https://github.com/aelharmouchi/paperwork-skills/issues/new/choose)
- [SECURITY.md](SECURITY.md) : erreurs de données sensibles et vulnérabilités
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

```bash
pip install pyyaml
python tools/validate_skills.py --strict
python -m unittest discover -s countries/ca-qc/fiscaliste/tests
python -m unittest discover -s countries/ma/fiscaliste/tests
```

## Licence

[MIT](LICENSE). Voir aussi [CHANGELOG.md](CHANGELOG.md).

---

<details>
<summary><b>English summary</b></summary>

`paperwork-skills` is a multi-country collection of AI-agent skills for tax and administrative paperwork. Each value in the data files carries a source URL and a confidence level (`official`, `secondary`, `unconfirmed`), and an automated validator enforces consistency between `SKILL.md`, JSON data, links and sources. Version 0.1 covers Québec (Canada) and Morocco, is only partially verified, and is **not tax, legal or accounting advice**. To add a country, copy `countries/_template`, fill it in, run `python tools/validate_skills.py`, and open a pull request. Skill content is written in each country's main language, declared in `country.json`.

</details>
