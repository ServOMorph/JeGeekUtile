# Signals — vertia   (MAJ 2026-08-30)

## Actions ouvertes
- [P2|ouvert] Vérifier le rendu mobile et l'accessibilité de base de la landing (reste de la phase 2 de la roadmap).
  - fait quand: rendu contrôlé sur mobile et vérification d'accessibilité de base effectuée et documentée.
  - réf: `roadmap_vertia.md` (Phase 2), `site/index.html`.
- [P2|ouvert] Nettoyer ou archiver `designs/` : les trois directions n'ont jamais été retenues, le site utilise une palette verte propre, distincte des trois fichiers.
  - fait quand: `designs/` est supprimé, archivé, ou une note y précise qu'aucune des trois directions n'est utilisée.
  - réf: `designs/01-nexus.html`, `designs/02-sillage.html`, `designs/03-orbite.html`, `site/styles.css`.
- [P3|ouvert] Tester une inscription réelle sur le formulaire pour confirmer la réception de la notification à la nouvelle adresse.
  - fait quand: un e-mail de notification est reçu sur jegeekutile.rec@gmail.com suite à une soumission de test.
  - réf: hook Netlify `submission_created` du site `vertia-v0`, formulaire `interet-vertia`.
- [P3|ouvert] Committer la correction de `scripts/netlify_deploy.ps1` (bug PowerShell bloquant sur stderr, corrigé mais non committé).
  - fait quand: le fichier corrigé est committé.
  - réf: `scripts/netlify_deploy.ps1`.
- [P3|ouvert] Réexaminer la durée de conservation de 24 mois affichée dans la politique de confidentialité : valeur choisie par défaut, non sourcée dans le projet.
  - fait quand: une durée validée par l'utilisateur remplace la valeur par défaut, ou celle-ci est explicitement confirmée.
  - réf: `site/confidentialite.html`.
- [P3|ouvert] Mettre à jour le responsable du traitement dans `site/confidentialite.html` lorsque l'association Je Geek Utile sera déclarée (actuellement Raphaël Richard à titre personnel).
  - fait quand: l'association est déclarée et la page reflète l'association comme responsable.
  - réf: `site/confidentialite.html`.

## Contexte chaud
- Site en production : `https://vertia-v0.netlify.app` (HTTP 200). Dernier déploiement production : `6a935786c5856ebc40a97cc9`.
- Hook Netlify Forms `submission_created` actif sur le site `vertia-v0` (id site `cef2f73a-a3dd-4972-9cc6-904700477d23`), destinataire `jegeekutile.rec@gmail.com`.
- Le site n'est pas lié à un dépôt Git côté Netlify (`repo_url` vide) : chaque mise en production nécessite un déploiement manuel via `scripts/netlify_deploy.ps1 -Production`.

## Dernière session (2026-08-30)
# Session du 2026-08-30

## Décisions prises
- Notification Netlify Forms redirigée vers jegeekutile.rec@gmail.com et validée par l'utilisateur.
- Politique de confidentialité complétée ; responsable désigné : Raphaël Richard, à titre personnel (association non déclarée à ce jour).
- Charte graphique JGU officielle (Aurore Humaine) testée puis écartée : la palette verte existante du site est la direction retenue.

## Livrables produits ou modifiés
- `site/confidentialite.html` : réécrite, mentions RGPD obligatoires complètes.
- `site/styles.css` : styles de la page légale ajoutés, palette verte inchangée.
- `specification_mvp1.md` : mention "association loi 1901" corrigée.
- `tests/test_landing.py` : 3 tests de conformité ajoutés (9/9 passent).
- `scripts/netlify_deploy.ps1` : bug PowerShell corrigé (stderr bloquant).
- Déploiement production Netlify effectué (`6a935786c5856ebc40a97cc9`).

## Hypothèses validées / invalidées
- VALIDE : le hook de notification Netlify Forms existait déjà et fonctionne (mise à jour d'adresse confirmée par relecture API).
- INVALIDE : la charte JGU officielle n'est pas retenue pour VertIA -> pivot vers la palette verte existante.
- EN ATTENTE : durée de conservation (24 mois) non sourcée ; envoi de test réel non confirmé après changement d'adresse.

## Prochaine étape exacte
Vérifier rendu mobile et accessibilité de la landing, nettoyer `designs/`, tester une inscription réelle pour confirmer la réception e-mail.

## Question bloquante pour la session suivante
Aucune.
