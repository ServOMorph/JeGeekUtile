# VertIA

## Objectif
Projet porté par Je Geek Utile pour fédérer une communauté autour des IA locales hébergées sur les ordinateurs personnels. La priorité initiale est le lancement public : MVP 1 constitué d'une landing page de communication et de recueil d'intérêt, avant les fonctionnalités communautaires, la recommandation matérielle et le tableau de bord local.

## Stack
- Landing statique : HTML/CSS, sans dépendance externe (`site/`).
- Recueil d'intérêt : Netlify Forms (pas de backend Flask pour le MVP 1).
- Déploiement : Netlify, dossier publié `site`, commande de build vide (`netlify.toml`).
- Scripts : `scripts/netlify_api.py` (client API Netlify), `scripts/netlify_deploy.ps1` (tests + déploiement).
- Tests : `python -m unittest discover -s tests`.

## Structure
- `site/` : landing page en production (`index.html`, `styles.css`, `confidentialite.html`, `merci/`).
- `designs/` : trois propositions graphiques non retenues, à nettoyer.
- `tests/` : tests automatisés de la landing.
- `scripts/` : intégration Netlify (API + déploiement).
- `_contexte/` : signals.md et contexte.md, protocole vibecoding de la zone.
- `specification_mvp1.md`, `roadmap_vertia.md` : cadrage et suivi de phases.

## État actuel
La landing MVP 1 est en production sur `https://vertia-v0.netlify.app`, formulaire Netlify Forms actif avec notification vers `jegeekutile.rec@gmail.com`, politique de confidentialité complète. La direction graphique retenue est la palette verte de `site/styles.css`. Tests : 9/9. Restent à faire : vérification mobile/accessibilité, test d'inscription réel, nettoyage de `designs/`.
