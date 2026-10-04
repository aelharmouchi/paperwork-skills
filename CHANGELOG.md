# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Les versions suivent [SemVer](https://semver.org/lang/fr/) : le numéro de version décrit la structure du projet, pas l'exactitude fiscale (voir `STATUS.md`).

## [0.1.0] — 2026-10-04

### Ajouté
- Format commun de skill (`core/SKILL_FORMAT.md`) et validateur `tools/validate_skills.py` (cohérence `SKILL.md` / JSON, sources et niveaux de confiance, liens, evals, absence de liens symboliques).
- `ca-qc/fiscaliste` : impôt fédéral et du Québec 2026, abattement du Québec, plafonds REER, CELI, CELIAPP, cotisations RRQ, RQAP, AE, calculateur testé, 8 evals.
- `ma/fiscaliste` : barème de l'IR (art. 73-I), charges de famille, retenue sur loyers, calculateur testé, 7 evals.
- Gabarit de pays `countries/_template`.
- Intégration continue (validation et tests) sur GitHub Actions.
- Modèles d'issues et de pull requests, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`.

### Limites connues
- Plusieurs valeurs sont de sources secondaires ou non confirmées (frais professionnels marocains en conflit de sources, montant personnel de base du Québec, taux d'inclusion des gains en capital, etc.). Voir `STATUS.md`.
- Aucune relecture par un professionnel; aucun skill n'est `verified`.
- Les evals décrivent des réponses attendues mais n'ont pas encore été exécutées contre un agent.
