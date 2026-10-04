## Description

<!-- Quoi et pourquoi : nouveau pays, nouveau skill, correction de valeur, mise à jour annuelle. -->

## Pays et skill concernés

<!-- ex. ca-qc / fiscaliste -->

## Liste de contrôle

- [ ] `python tools/validate_skills.py --strict` passe sans erreur ni avertissement
- [ ] Les tests passent (`python -m unittest discover -s countries/<pays>/<skill>/tests`)
- [ ] Chaque valeur ajoutée ou modifiée a une `source` (URL https) et une `confidence` correcte
- [ ] Les valeurs non officielles sont `secondary` ou `unconfirmed`, avec une `note` étiquetée `[Inférence]` ou `[Non confirmé]` si nécessaire
- [ ] Les valeurs de `display` apparaissent à l'identique dans `SKILL.md`
- [ ] `last_updated` et `STATUS.md` sont à jour
- [ ] Les valeurs attendues des tests ont été **calculées à la main**, pas copiées de la sortie du script
- [ ] Aucun texte protégé par le droit d'auteur n'est recopié (résumés et liens seulement)
- [ ] Aucun lien symbolique

## Sources consultées

<!-- Liens vers les sources officielles lues. Indiquez celles qui n'étaient pas lisibles. -->

## Points d'incertitude restants

<!-- Ce qui n'a pas pu être confirmé. -->
