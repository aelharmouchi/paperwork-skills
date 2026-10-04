# Cotisations salariales 2026 — RRQ, RQAP, assurance-emploi (Québec)

Sources : [Revenu Québec, principaux changements 2026](https://www.revenuquebec.ca/fr/entreprises/retenues-a-la-source-et-cotisations-de-lemployeur/trousse-employeur/principaux-changements-pour-2026-trousse-employeur/) et [ARC, T4032-QC janvier 2026](https://www.canada.ca/fr/agence-revenu/services/formulaires-publications/retenues-paie/t4032-tables-retenues-paie/t4032qc-jan/t4032qc-janvier-information-generale.html).

## Tableau (part de l'employé)

| Régime | Gains maximaux | Taux | Cotisation maximale |
|---|---|---|---|
| RRQ de base + 1re supplémentaire | 74 600 $, exemption 3 500 $ | 6,30 % (5,30 % + 1,00 %) | 4 479,30 $ |
| RRQ 2e supplémentaire | de 74 600 $ à 85 000 $ `[Inférence]` | 4,00 % | 416 $ |
| RQAP | 103 000 $ | 0,430 % | 442,90 $ |
| Assurance-emploi (Québec) | 68 900 $ | 1,30 % | 895,70 $ |

La part de l'employeur n'est pas traitée ici (voir un futur skill `comptable-pme`).

## Exemple (salaire brut 80 000 $)

- RRQ : (74 600 − 3 500) x 6,30 % = 4 479,30 $
- RRQ 2e supplémentaire : (80 000 − 74 600) x 4 % = 216,00 $
- RQAP : 80 000 x 0,430 % = 344,00 $
- AE : plafonnée à 895,70 $
- **Total = 5 935,00 $**

Vérifié par le script et les tests.

## Réserves

- Le plafond supérieur de 85 000 $ de la deuxième cotisation supplémentaire est une **inférence** : Revenu Québec mentionne la plage 74 600 $ à 85 000 $; 85 000 $ est aussi le maximum 2026 fédéral (ARC). À confirmer sur la page RRQ.
- Le traitement fiscal des cotisations (déduction vs crédit) n'est pas calculé par le script : il faut le signaler à l'utilisateur.
- Les travailleurs autonomes paient des taux différents (non couverts).
