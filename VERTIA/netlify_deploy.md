# Déploiement Netlify

1. Copier `.env.netlify.example` en `.env.netlify` et renseigner `NETLIFY_AUTH_TOKEN` ; ne jamais versionner ce fichier.
2. Créer ou lier le site Netlify, puis renseigner `NETLIFY_SITE_ID` si nécessaire.
3. Depuis `VERTIA`, exécuter `./scripts/netlify_deploy.ps1` pour une prévisualisation, ou `./scripts/netlify_deploy.ps1 -Production` pour la publication.

Le script exécute les tests avant le déploiement et publie le dossier `site`.
