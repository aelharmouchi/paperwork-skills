# Sécurité et signalement d'erreurs

## Vulnérabilités du code

Les scripts du dépôt (`tools/`, `countries/*/*/scripts/`) lisent des fichiers locaux et n'ouvrent aucune connexion réseau. Si vous trouvez une vulnérabilité (exécution de code, lecture de fichiers inattendue, dépendance à risque), **ne la publiez pas dans une issue publique**. Utilisez l'onglet **Security → Report a vulnerability** du dépôt GitHub pour la signaler en privé.

## Erreurs de données fiscales

Une valeur fausse (taux, plafond, seuil) est un problème de qualité, pas de sécurité, mais elle peut induire en erreur. Pour la signaler :

1. Ouvrez une issue avec le modèle **« Valeur incorrecte »**.
2. Indiquez le fichier, la valeur, la valeur attendue et **un lien vers une source officielle**.

Les corrections avec source officielle sont traitées en priorité. Le statut de vérification de chaque élément est suivi dans [STATUS.md](STATUS.md).

## Ce que ce projet ne fait pas

Ces skills ne sont pas un avis professionnel. Ne les utilisez pas comme seule base d'une déclaration d'impôt ou d'une décision financière importante.
