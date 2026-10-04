# scripts/ (optionnel mais recommandé)

Un calculateur déterministe qui lit `../data/*.json` évite que le modèle fasse
l'arithmétique. Modèles à suivre :

- `countries/ca-qc/fiscaliste/scripts/calc_impot_qc.py` (barèmes + crédits + abattement)
- `countries/ma/fiscaliste/scripts/calc_ir_ma.py` (barème calculé de deux façons et recoupé)

Ajoutez un dossier `tests/` avec des valeurs attendues **calculées à la main**, et un test
qui vérifie que les évals avec champ `calc` correspondent à la sortie réelle du script.
