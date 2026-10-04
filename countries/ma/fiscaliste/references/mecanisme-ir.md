# Mécanisme de l'IR au Maroc (barème applicable en 2026)

## Séquence (revenu salarial simple)

1. Revenu brut imposable annuel (salaire et avantages imposables).
2. Moins les frais professionnels (article 59 du CGI), voir `deductions-et-retenues.md`
   `[Non confirmé]`.
3. Moins les autres déductions admises (cotisations de retraite et de prévoyance,
   intérêts de prêt logement principal, etc.) : **non détaillées dans ce skill**.
4. = revenu net imposable annuel.
5. IR brut : (revenu net imposable x taux) − somme à déduire, selon le barème (article 73-I).
6. Moins la réduction pour charges de famille (article 74-I).
7. = IR net annuel (jamais négatif).

## Barème (source officielle : ministère de l'Économie et des Finances, LF 2025)

| Tranche (MAD) | Taux | Somme à déduire |
|---|---|---|
| 0 – 40 000 | 0 % | 0 |
| 40 001 – 60 000 | 10 % | 4 000 |
| 60 001 – 80 000 | 20 % | 10 000 |
| 80 001 – 100 000 | 30 % | 18 000 |
| 100 001 – 180 000 | 34 % | 22 000 |
| > 180 000 | 37 % | 27 400 |

Contrôle de cohérence (vérifié par test) : aux bornes, les deux méthodes donnent le
même montant (par exemple 12 000 MAD à 100 000 MAD de revenu net imposable).

## Exemples chiffrés (vérifiés par le script et par calcul manuel)

**Revenu net imposable 100 000 MAD, sans personne à charge**
- Par tranches : 20 000 x 10 % + 20 000 x 20 % + 20 000 x 30 % = 2 000 + 4 000 + 6 000 = **12 000 MAD**
- Par somme à déduire : 30 % x 100 000 − 18 000 = 12 000 MAD

**Revenu net imposable 120 000 MAD, 2 personnes à charge**
- IR brut : 34 % x 120 000 − 22 000 = 18 800 MAD
- Charges de famille : 2 x 600 = 1 200 MAD `[Source secondaire]`
- **IR net = 17 600 MAD**, taux moyen 14,67 %

**Revenu net imposable 200 000 MAD**
- IR brut : 37 % x 200 000 − 27 400 = **46 600 MAD**

## Points d'attention

- Le barème est **annuel**. La retenue mensuelle sur salaire utilise un barème mensuel
  équivalent (non couvert ici).
- Les montants de charges de famille et de frais professionnels ont changé plusieurs
  fois (LF 2023, LF 2025, LF 2026). Toujours confirmer l'année.
- Pour les non-résidents, les revenus de source marocaine peuvent suivre d'autres
  taux (retenue libératoire) : hors scope, ne pas extrapoler.
