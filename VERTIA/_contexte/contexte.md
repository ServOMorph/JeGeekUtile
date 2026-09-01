# Contexte — vertia

## Objectif (immuable sauf décision explicite)
Concevoir et faire évoluer VertIA, projet porté par l'association Je Geek Utile pour fédérer une communauté autour des IA locales hébergées sur les ordinateurs personnels. L'agent structure une solution scalable : information et documentation, recommandations de projets open source selon les caractéristiques du PC, puis tableau de bord téléchargeable pour gérer les IA locales et leurs fonctionnalités. Sa priorité initiale est de préparer le lancement public : roadmap complète et landing page du MVP 1 pour recruter des personnes intéressées.

## Stack / contraintes techniques (stable, rarement modifié)
- Projet parent : Je Geek Utile, projet associatif en cours de constitution (association non encore déclarée au 2026-08-30) ; valeurs d'éthique, transparence, sécurité des données et éco-responsabilité.
- Stack web existante : Flask, SQLAlchemy, SQLite et Flask-Login ; interfaces également développées en HTML/CSS/JavaScript vanilla.
- Contraintes UI du projet parent : thème sombre obligatoire, pixels blancs < 5 %, préférence pour zéro dépendance externe et une architecture modulaire.
- MVP 1 demandé : landing page de communication et de recueil d'intérêt. Les comptes, l'espace communautaire, la recommandation selon les spécifications du PC et le dashboard local sont des étapes ultérieures.
- Références : `README.md`, `CONTEXT.md`, `config.json`, `applis/modele_appli/` et `site internet/` à consulter avant toute décision d'intégration au projet parent.

## État actuel (réécrit intégralement à chaque /close)
La landing MVP 1 est en production sur `https://vertia-v0.netlify.app`, avec formulaire Netlify Forms, page de confirmation et politique de confidentialité complète (responsable, contact, finalité, base légale, durée de conservation, droits, CNIL). Notification active vers `jegeekutile.rec@gmail.com`.
Direction graphique retenue : palette verte de `site/styles.css`. Le dossier `designs/` a été supprimé du dépôt.
Revue statique d'accessibilité effectuée : contrastes conformes WCAG AA ; correctifs `:focus-visible`, `prefers-reduced-motion` et anti-débordement du `h1` appliqués à `site/styles.css` mais pas encore déployés en production.
Tests automatisés : 9/9.
Restent avant communication large : redéploiement des correctifs CSS, tests manuels (rendu mobile, navigation clavier, inscription réelle).

## Décisions structurantes (append only — 10 entrées max, 5 lignes max/entrée, archiver au-delà)
- 2026-08-29 : Le lancement public vise d'abord à identifier et fédérer des personnes intéressées ; la landing page constitue le MVP 1 avant les fonctionnalités communautaires et le dashboard local.
- 2026-08-29 : Le MVP 1 est une landing statique déployée par Netlify ; le formulaire utilise Netlify Forms plutôt qu'une route Flask.
- 2026-08-29 : VertIA affirme l'écologie, l'écoresponsabilité, l'éthique, la durabilité et une IA au service du jugement humain.
- 2026-08-29 : La commande Netlify est explicitement vide afin de neutraliser une configuration Hugo héritée ; le dossier publié est `site`.
- 2026-08-30 : La direction graphique retenue pour VertIA est la palette verte déjà présente dans `site/styles.css`, pas la charte JGU officielle (Aurore Humaine) ni l'une des trois propositions de `designs/`.
- 2026-08-30 : L'association Je Geek Utile n'étant pas déclarée, le responsable du traitement des inscriptions VertIA est Raphaël Richard à titre personnel, jusqu'à la création de l'association.
- 2026-08-30 : Le contact unique de VertIA est `jegeekutile.rec@gmail.com` (formulaire et politique de confidentialité) ; les adresses `@jegeekutile.org` ne sont pas utilisées, l'association n'existant pas.
- 2026-09-01 : Le dossier `designs/` est supprimé du dépôt (historique dans le commit `0c0b59f`) ; correctifs d'accessibilité et de rendu mobile appliqués à `site/styles.css`.
