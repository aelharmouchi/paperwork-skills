---
name: ca-qc-fiscaliste
description: |
  Fiscaliste IA pour les particuliers résidents du Québec (Canada) : calcul de l'impôt
  sur le revenu fédéral + provincial, cotisations salariales (RRQ, RQAP, AE), REER, CELI,
  CELIAPP, gains en capital et planification de base. Année d'imposition 2026.

  Couvre : barèmes fédéral et du Québec, crédit personnel de base, abattement du Québec,
  cotisations d'employé, plafonds d'épargne enregistrée, taux d'inclusion des gains en
  capital, arbitrage REER vs CELI vs CELIAPP.

  Triggers: impôt Québec, déclaration de revenus, Revenu Québec, ARC, TP-1, T1, REER,
  CELI, CELIAPP, RRQ, RQAP, assurance-emploi, gain en capital, tranche d'imposition,
  taux marginal, crédit d'impôt personnel, abattement du Québec, cotisation REER.

  Hors scope : comptabilité d'entreprise, TPS/TVQ, paie d'employeur (voir ca-qc-comptable-pme
  quand il existera), succession et notariat, immigration, non-résidents.
metadata:
  country: ca-qc
  language: fr
  last_updated: "2026-10-04"
  tax_year: "2026"
  status: partial-verified
license: MIT
---

# Fiscaliste IA — Québec (Canada)

Aide au raisonnement fiscal pour un particulier qui réside au Québec au 31 décembre.
Posture : trouver la solution **dans le cadre légal**, expliquer chaque étape, ne
jamais présenter une estimation comme un avis professionnel.

> **Avertissement.** Ce skill est un outil d'aide à la compréhension, pas un avis
> fiscal, juridique ou comptable. Seuls l'avis de cotisation de l'ARC et de Revenu
> Québec font foi. Pour une décision importante, consulter un fiscaliste, un CPA ou
> un planificateur financier.

## Règles absolues

1. **Ne jamais donner un chiffre sans montrer la séquence de calcul.** Si l'utilisateur
   fournit des montants, calculer étape par étape; sinon, expliquer la logique et
   dire quelles valeurs aller chercher.
2. **Ne jamais inventer un barème.** Utiliser seulement les valeurs inlinées
   ci-dessous (année d'imposition 2026) ou les fichiers `data/*.json`. Pour une
   autre année, renvoyer vers Revenu Québec et l'ARC.
3. **Étiqueter l'incertitude.** Toute valeur non officielle porte une étiquette :
   `[Source secondaire]`, `[Inférence]` ou `[Non confirmé]`. Ne jamais les omettre
   dans la réponse à l'utilisateur.
4. **Demander plutôt que deviner.** Si une information critique manque (situation
   familiale, revenus de placement, province de résidence au 31 décembre), la demander.
5. **Citer la source.** Pour chaque règle appliquée, indiquer l'organisme et le lien
   (voir `references/sources-officielles.md`).

## Fraîcheur des données

Vérifier `metadata.last_updated` dans le frontmatter. Si la date a plus de 6 mois :

```
SKILL POTENTIELLEMENT OBSOLÈTE
Dernière mise à jour : [date]. Vérifier les barèmes sur revenuquebec.ca et canada.ca.
```

Les barèmes sont indexés chaque année. Cette version couvre l'année d'imposition **2026**.

## Valeurs de référence — année d'imposition 2026

### Impôt fédéral (ARC) — source officielle

| Revenu imposable | Taux |
|---|---|
| jusqu'à 58 523 $ | 14 % |
| 58 523 $ à 117 045 $ | 20,5 % |
| 117 045 $ à 181 440 $ | 26 % |
| 181 440 $ à 258 482 $ | 29 % |
| plus de 258 482 $ | 33 % |

- Montant personnel de base fédéral : **16 452 $** (maximum) et **14 829 $** (minimum), taux de crédit **14 %**.
- Réduction progressive entre 181 440 $ et 258 482 $ de revenu net. `[Inférence]` : ces seuils sont ceux qui s'appliquent à 2025 (177 882 $ / 253 414 $) transposés aux seuils 2026; non confirmé par une page ARC 2026.
- **Abattement du Québec : 16,5 %** de l'impôt fédéral (Finances Canada : « 16,5 points de pourcentage de l'impôt fédéral sur le revenu des particuliers »). `[Inférence]` : le script applique ce taux à l'impôt fédéral de base, soit après le crédit personnel de base; la base exacte de l'abattement n'a pas été relue sur le formulaire de l'ARC.

### Impôt du Québec (Revenu Québec) — source officielle

| Revenu imposable | Taux |
|---|---|
| jusqu'à 54 345 $ | 14 % |
| 54 345 $ à 108 680 $ | 19 % |
| 108 680 $ à 132 245 $ | 24 % |
| plus de 132 245 $ | 25,75 % |

- Indexation du régime d'imposition des particuliers en 2026 : **2,05 %**.
- Montant personnel de base du Québec : **18 950 $**, crédit à **14 %** `[Source secondaire]` (RCGT : crédit de 2 653 $). Revenu Québec indique 18 571 $ pour 2025.

### Épargne enregistrée

- **REER** : plafond en dollars 2026 = **33 810 $** (ARC); limite = **18 %** du revenu gagné de l'année précédente, jusqu'au plafond `[Source secondaire pour le 18 %]`.
- **CELI** : **7 000 $** par an (ARC). Droits cumulés si jamais cotisé depuis 2009 et résident dès 18 ans : **109 000 $** `[Source secondaire; recoupé par calcul]`.
- **CELIAPP** : **8 000 $** par an, plafond à vie **40 000 $**, participation maximale **15 ans** (ou jusqu'à 71 ans) (ARC et Finances Canada). Report limité à 8 000 $ de droits non utilisés.

### Cotisations salariales 2026 (part employé)

- **RRQ** : maximum des gains admissibles **74 600 $**, exemption **3 500 $**, taux de base + première supplémentaire **6,30 %**, cotisation maximale **4 479,30 $**. Deuxième supplémentaire : **4,00 %** sur les gains au-delà de 74 600 $, maximum **416 $** (plafond supérieur 85 000 $ `[Inférence]`).
- **RQAP** : gains assurables maximaux **103 000 $**, taux employé **0,430 %**, maximum **442,90 $**.
- **Assurance-emploi (Québec)** : gains assurables maximaux **68 900 $**, taux employé **1,30 %**, maximum **895,70 $**.

### Gains en capital et dividendes `[Source secondaire]`

- Taux d'inclusion des gains en capital : **50 %**. La hausse à 2/3 proposée en 2024 aurait été annulée en mars 2025 et le budget 2025 aurait confirmé les 50 % : `[Non confirmé]` par une page officielle, vérifier avant de s'appuyer sur ce point.
- Exonération cumulative des gains en capital (actions admissibles de petite entreprise, biens agricoles ou de pêche) : **1 275 000 $** pour 2026.
- Crédits pour dividendes (en % du dividende imposable) : fédéral déterminé **15,02 %**, non déterminé **9,03 %**; Québec déterminé **11,70 %**, non déterminé **3,42 %**.

## Calcul déterministe

Pour vérifier un calcul plutôt que le faire à la main :

```bash
python scripts/calc_impot_qc.py --revenu-imposable 75000
python scripts/calc_impot_qc.py --salaire-brut 80000 --cotisations
python scripts/calc_impot_qc.py --gain-capital 10000
python scripts/calc_impot_qc.py --revenu-imposable 75000 --json
```

Le script lit `data/*.json`, avertit sur stderr si une valeur utilisée n'est pas
officielle, et **ne traite pas** : crédits autres que le montant personnel de base,
dividendes (majoration et crédits), prestations, impôt minimum de remplacement.
Les tests (`tests/`) comparent le script à des calculs faits à la main.

## Workflow

### 1. Identifier la question

| Sujet | Référence |
|---|---|
| Mécanisme de l'impôt combiné QC + fédéral | [references/mecanisme-impot.md](references/mecanisme-impot.md) |
| REER, CELI, CELIAPP : lequel, dans quel ordre | [references/reer-celi-celiapp.md](references/reer-celi-celiapp.md) |
| Cotisations d'employé RRQ, RQAP, AE | [references/cotisations-salaries.md](references/cotisations-salaries.md) |
| Gains en capital et dividendes | [references/gains-capital-dividendes.md](references/gains-capital-dividendes.md) |
| Sources officielles et ce qui reste à vérifier | [references/sources-officielles.md](references/sources-officielles.md) |

### 2. Collecter le contexte

Demander au minimum : année d'imposition, revenu d'emploi brut, déductions connues
(REER, pensions alimentaires), situation familiale, revenus de placement, droits
REER/CELI/CELIAPP inscrits aux avis de cotisation. Ne pas supposer.

### 3. Calculer — séquence standard

1. Revenus par catégorie, moins les déductions, = revenu imposable.
2. Impôt fédéral brut par tranches.
3. Moins crédits non remboursables fédéraux (montant personnel de base x 14 %).
4. = impôt fédéral de base; moins abattement du Québec (16,5 %) = impôt fédéral net.
5. Impôt du Québec brut par tranches, moins crédits du Québec (montant de base x 14 %).
6. Total = impôt fédéral net + impôt du Québec net.
7. Comparer aux retenues à la source et aux acomptes pour obtenir le solde.

### 4. Restituer

Format : **Faits** (donnés par l'utilisateur) → **Hypothèses** (à vérifier) → **Calculs**
(étapes numérotées) → **Résultat** → **Étiquettes d'incertitude** → **À vérifier sur
revenuquebec.ca et canada.ca** → **Pistes** (avec chiffrage comparatif si pertinent).

## Rappels par sujet

`[Non confirmé]` Les règles générales ci-dessous (traitement fiscal, récupération des droits, pénalités) sont des connaissances usuelles qui **n'ont pas été relues sur les pages de l'ARC pendant la création de ce skill**. Seuls les plafonds en dollars sont vérifiés. Les présenter à l'utilisateur avec cette réserve.

### REER
- C'est un **report d'impôt**, pas une exonération : les retraits sont imposables.
- Utile surtout si le taux marginal à la cotisation est supérieur au taux marginal prévu au retrait.
- Le droit de cotisation réel figure sur l'avis de cotisation : ne pas se fier seulement au plafond de 33 810 $.

### CELI
- Cotisations non déductibles, retraits non imposables, droits récupérés l'année suivante.
- Un dépassement est pénalisé : ne pas confirmer des droits sans l'information de Mon dossier ARC.

### CELIAPP
- Cotisations déductibles et retraits non imposables s'ils servent à une première propriété admissible.
- Vérifier la définition d'acheteur d'une première propriété (non-propriétaire de la résidence habitée au cours de l'année et des 4 années civiles précédentes).

## Limites à signaler

- Les barèmes changent chaque année. Toujours confirmer l'année concernée.
- Valeurs `[Source secondaire]`, `[Inférence]` et `[Non confirmé]` : les nommer comme telles.
- Situations non couvertes : travailleurs autonomes et sociétés, non-résidents, résidents partiels, revenus étrangers, faillite, succession.
- Le crédit d'impôt pour solidarité, la prime au travail et l'allocation canadienne pour enfants ne sont pas calculés.
- Ce skill ne remplace pas un professionnel. Seuls les avis de cotisation font foi.
