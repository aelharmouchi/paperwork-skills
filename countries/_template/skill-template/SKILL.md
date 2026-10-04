---
name: xx-metier
description: |
  TODO : en 3 à 5 lignes, ce que couvre ce skill pour <pays> (public visé, sujets, année).

  Triggers: TODO mots-clés que l'utilisateur écrira (termes locaux, sigles, formulaires).

  Hors scope : TODO ce que ce skill ne fait pas, et vers quel autre skill renvoyer.
metadata:
  country: xx
  language: fr
  last_updated: "AAAA-MM-JJ"
  tax_year: "AAAA"
  status: experimental
license: MIT
---

# Titre du skill — <Pays>

TODO : une phrase sur la posture (ex. « trouver la solution dans le cadre légal, expliquer chaque étape »).

> **Avertissement.** Ce skill est un outil d'aide à la compréhension, pas un avis
> fiscal, juridique ou comptable. Seule l'autorité compétente fait foi. Pour une
> décision importante, consulter un professionnel du pays.

## Règles absolues

1. **Ne jamais donner un chiffre sans montrer la séquence de calcul.**
2. **Ne jamais inventer un barème ni un taux.** Utiliser seulement les valeurs de ce fichier et de `data/*.json`.
3. **Étiqueter l'incertitude** : `[Source secondaire]`, `[Inférence]`, `[Non confirmé]`.
4. **Demander plutôt que deviner.**
5. **Citer la source** (article de loi, circulaire, page officielle).

## Fraîcheur des données

Si `metadata.last_updated` a plus de 6 mois, avertir l'utilisateur et renvoyer vers la source officielle.

## Valeurs de référence

TODO : écrire ici les valeurs clés, **exactement** comme dans le champ `display` des fichiers `data/*.json`
(le validateur vérifie que chaque `display` apparaît dans ce fichier).

## Workflow

| Sujet | Référence |
|---|---|
| TODO | [references/exemple.md](references/exemple.md) |

1. Identifier la question et l'année.
2. Collecter le contexte.
3. Calculer (étapes numérotées).
4. Restituer : **Faits** → **Hypothèses** → **Calculs** → **Résultat** → **Étiquettes d'incertitude** → **À vérifier**.

## Limites

- Les règles changent chaque année : confirmer l'année concernée.
- TODO : situations non couvertes.
- Ce skill ne remplace pas un professionnel. Seule l'autorité fait foi.
