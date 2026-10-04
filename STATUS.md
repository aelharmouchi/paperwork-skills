# Statut de vérification par pays

Dernière mise à jour : 2026-10-04.

Niveaux (champ `status` dans `country.json` et `metadata.status` de chaque skill) :

| Niveau | Signification |
|---|---|
| `verified` | Toutes les valeurs proviennent de sources officielles; relu par un humain compétent. |
| `partial-verified` | Les valeurs clés sont officielles; certaines sont secondaires ou non confirmées et étiquetées comme telles. |
| `community` | Contribué par la communauté, structure validée automatiquement, contenu non relu. |
| `experimental` | Ébauche. |

Aucun skill n'est `verified` aujourd'hui. Le validateur interdit ce statut tant qu'une valeur n'est pas officielle.

## ca-qc / fiscaliste — partial-verified

| Élément | Niveau | Remarque |
|---|---|---|
| Barème fédéral 2026 | officiel | ARC |
| Barème du Québec 2026, indexation 2,05 % | officiel | Revenu Québec |
| Montant personnel de base fédéral (max/min), crédit 14 % | officiel | ARC T4032-QC |
| Abattement du Québec 16,5 % | officiel | Finances Canada |
| Plafonds REER, CELI, CELIAPP | officiel | ARC, Finances Canada |
| RRQ, RQAP, AE (taux et maximums) | officiel | Revenu Québec, ARC |
| Montant personnel de base du Québec 18 950 $ | secondaire | déduit du crédit de 2 653 $ (RCGT) |
| Seuils de réduction du montant personnel fédéral | non confirmé | transposés de 2025 |
| Plafond supérieur 2e cotisation RRQ (85 000 $) | non confirmé | inférence |
| Règle de 18 % du REER, droits CELI cumulés | secondaire | recoupé par calcul pour le CELI |
| Taux d'inclusion des gains en capital 50 % | secondaire | à confirmer sur canada.ca |
| Crédits pour dividendes, ECGC | secondaire | |

## ma / fiscaliste — partial-verified

| Élément | Niveau | Remarque |
|---|---|---|
| Barème IR (art. 73-I), LF 2025 | officiel | note du ministère des Finances; applicabilité 2026 non confirmée par la LF 2026 lue en entier |
| Charges de famille 600 MAD / 3 600 MAD | secondaire | circulaire DGI n° 737 non lisible en direct |
| Retenue à la source 5 % sur loyers | secondaire | modalités non confirmées |
| Frais professionnels (art. 59) | **non confirmé, sources en conflit** | 35 %/25 % (LF 2023) vs 20 % (autres sites) |
| Exonération des pensions de retraite | non confirmé | périmètre non vérifié |

## Skills prévus (non créés)

- `ca-qc / comptable-pme` : TPS/TVQ (taux 5 % et 9,975 %, petit fournisseur 30 000 $ vérifiés sur Revenu Québec), DAS, incorporation.
- `ma / comptable-pme` : PCGE, IS (20 % / 35 % / 40 %), TVA (20 % / 10 %), CNSS/AMO, auto-entrepreneur.
