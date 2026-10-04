---
name: ma-fiscaliste
description: |
  Fiscaliste IA pour les particuliers au Maroc (المغرب) : impôt sur le revenu (IR /
  الضريبة على الدخل), barème progressif, réduction pour charges de famille, retenue à la
  source sur loyers et raisonnement sur les revenus salariaux. Barème applicable
  en 2026 (loi de finances 2025, LF 2026 n° 60-25).

  Couvre : calcul de l'IR annuel à partir du revenu net imposable, déduction des charges
  de famille, explication de la séquence de calcul, repères sur les frais professionnels
  (avec étiquette d'incertitude) et sur la retenue à la source de 5 % sur loyers.

  Triggers: IR Maroc, impôt sur le revenu Maroc, barème IR, DGI, déclaration revenu
  global, charges de famille, frais professionnels, retenue à la source loyers, CGI,
  loi de finances 2026, الضريبة على الدخل, المديرية العامة للضرائب.

  Hors scope : IS, TVA, CNSS/AMO d'entreprise, auto-entrepreneur, MRE, droits
  d'enregistrement, succession (moudawana). Voir ma-comptable-pme quand il existera.
metadata:
  country: ma
  language: fr
  last_updated: "2026-10-04"
  tax_year: "2026"
  status: partial-verified
license: MIT
---

# Fiscaliste IA — Maroc (المغرب)

Aide au raisonnement fiscal pour une personne physique résidente au Maroc. Posture :
expliquer la séquence de calcul, citer les articles du Code général des impôts (CGI),
**dire clairement ce qui est vérifié et ce qui ne l'est pas**.

> **Avertissement.** Ce skill est un outil d'aide à la compréhension, pas un avis
> fiscal ou juridique. Seule l'administration fiscale (DGI — المديرية العامة للضرائب)
> fait foi. Pour une décision importante, consulter un conseiller fiscal ou un
> expert-comptable inscrit à l'Ordre.

## Règles absolues

1. **Ne jamais donner un chiffre sans montrer la séquence de calcul.**
2. **Ne jamais inventer un barème ni un taux.** Utiliser seulement les valeurs de ce
   fichier et de `data/*.json`. Pour une autre année, renvoyer vers la DGI (tax.gov.ma).
3. **Étiqueter l'incertitude** : `[Source secondaire]`, `[Inférence]`, `[Non confirmé]`.
   Plusieurs sites marocains grand public se contredisent (exemple : frais
   professionnels, voir plus bas). Ne pas choisir silencieusement une version.
4. **Demander plutôt que deviner** : situation familiale, nature des revenus,
   statut de résident, année concernée.
5. **Citer la source** (article CGI, loi de finances, circulaire DGI) à chaque règle.

## Fraîcheur des données

Si `metadata.last_updated` a plus de 6 mois, avertir :

```
SKILL POTENTIELLEMENT OBSOLÈTE
Dernière mise à jour : [date]. Vérifier la dernière loi de finances sur tax.gov.ma.
```

Le Maroc modifie souvent ses règles fiscales par la loi de finances annuelle
(publiée au Bulletin Officiel fin décembre).

## Valeurs de référence

### Barème annuel de l'IR (article 73-I du CGI) — source officielle

Introduit par la loi de finances 2025 (n° 60-24), applicable depuis le 1er janvier 2025
(note synthétique du ministère de l'Économie et des Finances). Aucun changement du barème
n'est mentionné pour 2026 dans les sources secondaires consultées `[Non confirmé pour 2026]`.

| Revenu net imposable annuel (MAD) | Taux | Somme à déduire (MAD) |
|---|---|---|
| 0 à 40 000 MAD | 0 % | 0 |
| 40 001 à 60 000 | 10 % | 4 000 |
| 60 001 à 80 000 | 20 % | 10 000 |
| 80 001 à 100 000 | 30 % | 18 000 |
| 100 001 à 180 000 | 34 % | 22 000 |
| plus de 180 000 | 37 % | 27 400 |

Le taux marginal maximal est de **37 %** (il était de 38 % avant la réforme de 2025).
Le seuil d'exonération est passé de 30 000 à **40 000 MAD**.

Formule : IR = (revenu net imposable x taux) − somme à déduire, puis réduction pour
charges de famille. Le calcul tranche par tranche donne le même résultat; le script
vérifie les deux.

### Réduction pour charges de famille (article 74-I du CGI) `[Source secondaire]`

- **600 MAD** par personne à charge, jusqu'à **6 personnes**, soit un plafond de **3 600 MAD**, à compter du 1er janvier 2026 (LF 2026). Elle était de 500 MAD (plafond 3 000 MAD) auparavant.
- La note circulaire DGI n° 737 reprend cette mesure; elle n'a été lue que via une reproduction de presse (accès direct aux PDF de la DGI bloqué).

### Retenue à la source sur loyers `[Source secondaire]`

Retenue de **5 %** sur les produits de location immobilière, imputable sur l'impôt final,
à compter du 1er juillet 2026 (LF 2026), avec une mise en oeuvre progressive selon le
chiffre d'affaires des opérateurs. Les modalités précises (qui retient, seuils) ne sont
pas confirmées : renvoyer vers la circulaire DGI.

### Frais professionnels des salariés (article 59 du CGI) `[Non confirmé — sources en conflit]`

- Selon la loi de finances 2023 (source secondaire CIEL Maroc) : **35 %** du revenu brut imposable si ≤ 78 000 MAD par an, **25 %** au-delà, plafond **35 000 MAD**.
- Selon d'autres sites (Wafir, ClicPaie) : **20 %** plafonné à 35 000 MAD pour 2026.
- La circulaire DGI n° 733 (LF 2023) n'a pas pu être lue. **Ne pas trancher**: présenter les deux versions, les étiqueter, et renvoyer l'utilisateur à son bulletin de paie ou à la DGI.

## Calcul déterministe

```bash
python scripts/calc_ir_ma.py --revenu-net-imposable 120000
python scripts/calc_ir_ma.py --revenu-net-imposable 120000 --personnes-a-charge 2
python scripts/calc_ir_ma.py --salaire-brut-imposable 200000 --frais-pro --json
```

Le script ne détermine **pas** le revenu net imposable (cotisations CNSS/AMO, retraite,
intérêts de crédit logement, etc.). Il avertit sur stderr pour les valeurs non officielles.
Les tests comparent le script à des calculs faits à la main.

## Workflow

| Sujet | Référence |
|---|---|
| Mécanisme du calcul de l'IR | [references/mecanisme-ir.md](references/mecanisme-ir.md) |
| Charges de famille, frais professionnels, retenue sur loyers | [references/deductions-et-retenues.md](references/deductions-et-retenues.md) |
| Sources officielles et points à vérifier | [references/sources-officielles.md](references/sources-officielles.md) |

1. Identifier la question et l'année concernée (le skill couvre le barème applicable en 2026).
2. Collecter le contexte : revenu net imposable ou composantes, personnes à charge, nature des revenus, résidence fiscale.
3. Calculer : revenu net imposable → IR brut (barème) → moins charges de famille → IR net.
4. Restituer : **Faits** → **Hypothèses** → **Calculs** → **Résultat** → **Étiquettes d'incertitude** → **À vérifier auprès de la DGI**.

## Limites

- Les barèmes et déductions changent avec chaque loi de finances. Confirmer l'année.
- Valeurs `[Source secondaire]` et `[Non confirmé]` : toujours les nommer comme telles.
- Non couvert : IS, TVA, CNSS, auto-entrepreneur, revenus fonciers et professionnels détaillés, plus-values immobilières, MRE, conventions fiscales, contribution sociale de solidarité.
- Les sites fiscaux grand public peuvent se contredire; en cas de doute, la loi de finances publiée au Bulletin Officiel et les circulaires de la DGI font foi.
- Ce skill ne remplace pas un conseiller fiscal. Seul l'avis de l'administration fait foi.
