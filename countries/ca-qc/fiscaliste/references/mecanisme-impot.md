# Mécanisme de l'impôt sur le revenu — résident du Québec (2026)

Un résident du Québec produit **deux déclarations** : une fédérale (ARC, T1) et une
provinciale (Revenu Québec, TP-1). Les deux impôts sont calculés séparément et
s'additionnent.

## Séquence de calcul (cas simple : salarié, un seul employeur)

| Étape | Fédéral | Québec |
|---|---|---|
| 1 | Revenu imposable (après déductions) | Revenu imposable (après déductions) |
| 2 | Impôt brut par tranches | Impôt brut par tranches |
| 3 | Moins crédit personnel de base : montant x 14 % | Moins crédit personnel de base : montant x 14 % |
| 4 | = impôt fédéral de base | = impôt du Québec net |
| 5 | Moins abattement du Québec : 16,5 % de l'impôt de base `[Inférence : base exacte non relue sur le formulaire ARC]` | |
| 6 | = impôt fédéral net | |

**Total = impôt fédéral net + impôt du Québec net.**

Les revenu imposables fédéral et provincial peuvent différer (certaines déductions
et inclusions diffèrent). Le calculateur du skill suppose qu'ils sont identiques :
`[Inférence]` valable pour un salarié sans situation particulière.

## Exemple chiffré (revenu imposable 75 000 $)

Vérifié par `scripts/calc_impot_qc.py` et par un calcul manuel indépendant.

**Fédéral**
- 58 523 x 14 % = 8 193,22
- (75 000 − 58 523) = 16 477 x 20,5 % = 3 377,79
- Impôt brut = 11 571,01
- Crédit : 16 452 x 14 % = 2 303,28 → impôt de base = 9 267,73
- Abattement du Québec : 9 267,73 x 16,5 % = 1 529,17 → **impôt fédéral net = 7 738,55**

**Québec**
- 54 345 x 14 % = 7 608,30
- (75 000 − 54 345) = 20 655 x 19 % = 3 924,45
- Impôt brut = 11 532,75
- Crédit : 18 950 x 14 % = 2 653,00 `[Source secondaire]` → **impôt du Québec net = 8 879,75**

**Total = 16 618,30 $**, taux moyen 22,16 %. Taux marginal combiné approximatif
36,12 % (20,5 % x (1 − 16,5 %) + 19 %), ce qui suppose que seuls les barèmes
jouent à la marge.

## Taux marginal combiné — rappel

Le taux marginal fédéral s'applique **après** l'abattement du Québec :
`taux fédéral x (1 − 0,165) + taux du Québec`. Ne pas additionner simplement les deux
taux nominaux.

## Ce qui n'est pas dans ce mécanisme simplifié

Autres crédits non remboursables (âge, frais médicaux, dons, études, etc.), déduction
pour cotisations supplémentaires au RRQ, dividendes, impôt minimum de remplacement,
prestations soumises à un revenu familial. Ils doivent être traités séparément et
signalés à l'utilisateur comme hors du calcul.

Sources : voir [sources-officielles.md](sources-officielles.md).
