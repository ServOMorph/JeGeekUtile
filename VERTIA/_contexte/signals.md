# Signals — vertia   (MAJ 2026-09-01)

## Actions ouvertes
- [P2|ouvert] Redéployer la landing en production pour publier les correctifs CSS d'accessibilité et de rendu mobile.
  - fait quand: un déploiement production postérieur au 2026-09-01 est effectué et le site renvoie HTTP 200 avec le nouveau `styles.css`.
  - réf: `scripts/netlify_deploy.ps1` (option `-Production`), `site/styles.css`.
- [P2|ouvert] Exécuter les tests manuels de `tests_manuels.md` : rendu mobile + zoom 200 %, navigation clavier, inscription réelle.
  - fait quand: les trois sections de `tests_manuels.md` sont validées et le fichier vidé.
  - réf: `tests_manuels.md`, `roadmap_vertia.md` (Phase 2), `site/index.html`, `site/styles.css`.
- [P3|ouvert] Test d'inscription réelle sur le formulaire pour confirmer la réception de la notification.
  - fait quand: un e-mail de notification est reçu sur jegeekutile.rec@gmail.com suite à une soumission de test.
  - réf: hook Netlify `submission_created` du site `vertia-v0`, formulaire `interet-vertia`, `tests_manuels.md`.
- [P3|ouvert] Réexaminer la durée de conservation de 24 mois affichée dans la politique de confidentialité : valeur par défaut, non sourcée.
  - fait quand: une durée validée par l'utilisateur remplace la valeur par défaut, ou celle-ci est explicitement confirmée.
  - réf: `site/confidentialite.html`.
- [P3|ouvert] Mettre à jour le responsable du traitement dans `site/confidentialite.html` lorsque l'association Je Geek Utile sera déclarée (actuellement Raphaël Richard à titre personnel).
  - fait quand: l'association est déclarée et la page reflète l'association comme responsable.
  - réf: `site/confidentialite.html`.

## Contexte chaud
- Site en production : `https://vertia-v0.netlify.app` (HTTP 200). Dernier déploiement production : `6a935786c5856ebc40a97cc9` (antérieur aux correctifs CSS du 2026-09-01, donc pas encore en ligne).
- Hook Netlify Forms `submission_created` actif sur le site `vertia-v0` (id site `cef2f73a-a3dd-4972-9cc6-904700477d23`), destinataire `jegeekutile.rec@gmail.com`.
- Le site n'est pas lié à un dépôt Git côté Netlify (`repo_url` vide) : chaque mise en production nécessite un déploiement manuel via `scripts/netlify_deploy.ps1 -Production`.
- Revue statique d'accessibilité faite le 2026-09-01 : contrastes de la palette verte tous conformes WCAG AA (plus faible ~7.5:1) ; aucune `<img>`, aucun lien mort, aucun texte provisoire.

## Dernière session (2026-09-01)
# Session du 2026-09-01

## Décisions prises
- Dossier `designs/` supprimé du dépôt (méthode retenue : suppression, pas archivage) ; historique conservé dans le commit `0c0b59f`.
- Correctifs accessibilité / rendu mobile bas risque appliqués sans attendre la validation visuelle ; celle-ci reste un test manuel.

## Livrables produits ou modifiés
- `VERTIA/designs/` (4 fichiers) : supprimés (`git rm`).
- `site/styles.css` : `:focus-visible` ajouté, `@media (prefers-reduced-motion: reduce)`, plancher `clamp` du `h1` abaissé à `2.2rem` + `overflow-wrap` sur `h1/h2/h3`, `.message/.legal h1` plancher abaissé à `2rem`.
- `tests_manuels.md` : créé, 3 contrôles en attente.
- Revue statique accessibilité + contrastes des 4 pages du site : effectuée et documentée dans l'échange.

## Hypothèses validées / invalidées
- VALIDE : tous les contrastes de la palette verte passent WCAG AA (calcul statique).
- VALIDE : l'action "committer `netlify_deploy.ps1`" était déjà résolue — correction incluse dans le commit `4cdac46`.
- EN ATTENTE : débordement horizontal du `h1` sur écrans <= 360 px — risque identifié, correctif préventif appliqué, non confirmé sur appareil réel.
- EN ATTENTE : durée de conservation (24 mois) toujours non sourcée.

## Prochaine étape exacte
Redéployer en production (`scripts/netlify_deploy.ps1 -Production`) pour publier les correctifs CSS, puis exécuter les 3 tests manuels de `tests_manuels.md`. Après validation, franchir le checkpoint de fin de Phase 2.

## Question bloquante pour la session suivante
Aucune.
