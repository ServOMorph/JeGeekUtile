# Contexte — vertia

## Objectif (immuable sauf décision explicite)
Concevoir et faire évoluer VertIA, projet porté par l'association Je Geek Utile pour fédérer une communauté autour des IA locales hébergées sur les ordinateurs personnels. L'agent structure une solution scalable : information et documentation, recommandations de projets open source selon les caractéristiques du PC, puis tableau de bord téléchargeable pour gérer les IA locales et leurs fonctionnalités. Sa priorité initiale est de préparer le lancement public : roadmap complète et landing page du MVP 1 pour recruter des personnes intéressées.

## Stack / contraintes techniques (stable, rarement modifié)
- Projet parent : Je Geek Utile, association loi 1901 ; valeurs d'éthique, transparence, sécurité des données et éco-responsabilité.
- Stack web existante : Flask, SQLAlchemy, SQLite et Flask-Login ; interfaces également développées en HTML/CSS/JavaScript vanilla.
- Contraintes UI du projet parent : thème sombre obligatoire, pixels blancs < 5 %, préférence pour zéro dépendance externe et une architecture modulaire.
- MVP 1 demandé : landing page de communication et de recueil d'intérêt. Les comptes, l'espace communautaire, la recommandation selon les spécifications du PC et le dashboard local sont des étapes ultérieures.
- Références : `README.md`, `CONTEXT.md`, `config.json`, `applis/modele_appli/` et `site internet/` à consulter avant toute décision d'intégration au projet parent.

## État actuel (réécrit intégralement à chaque /close)
La landing statique MVP 1 est dans `site/`, avec formulaire Netlify Forms, pages de confirmation et confidentialité.
Trois directions graphiques HTML sont disponibles dans `designs/`.
Netlify publie `site/` sans commande de build ; le déploiement brouillon est validé.
Les tests de landing passent (6/6).
Avant lancement public : finaliser les mentions de confidentialité et activer/tester la notification de soumission dans Netlify.

## Décisions structurantes (append only — 10 entrées max, 5 lignes max/entrée, archiver au-delà)
- 2026-08-29 : Le lancement public vise d'abord à identifier et fédérer des personnes intéressées ; la landing page constitue le MVP 1 avant les fonctionnalités communautaires et le dashboard local.
- 2026-08-29 : Le MVP 1 est une landing statique déployée par Netlify ; le formulaire utilise Netlify Forms plutôt qu'une route Flask.
- 2026-08-29 : VertIA affirme l'écologie, l'écoresponsabilité, l'éthique, la durabilité et une IA au service du jugement humain.
- 2026-08-29 : La commande Netlify est explicitement vide afin de neutraliser une configuration Hugo héritée ; le dossier publié est `site`.
