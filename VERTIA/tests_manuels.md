# Tests manuels — VertIA

## Rendu mobile de la landing

Contrôler sur un écran réel ou l'émulation navigateur en largeurs 320 px, 360 px et 768 px, sur `index.html`, `confidentialite.html` et `merci/index.html` :
- absence de débordement horizontal (vérifier en particulier le `h1` de l'accueil : « Explorer l'IA locale, sur votre ordinateur. »)
- lisibilité des titres et des paragraphes, pas de texte tronqué ni chevauché
- grilles `.cards` et `.project-grid` bien empilées sous 680 px
- cibles tactiles du formulaire (champs, case à cocher, bouton) confortables
- zoom navigateur à 200 % sans perte de contenu ni scroll horizontal

Fait quand : les trois pages sont contrôlées aux trois largeurs + zoom 200 %, résultat noté.

## Navigation clavier et accessibilité de base de la landing

Sur `index.html` puis `confidentialite.html` :
- parcours complet à la touche Tab : ordre logique, focus toujours visible (contour vert)
- activation des liens d'ancrage de la navigation au clavier
- remplissage et soumission du formulaire au clavier seul
- messages de validation natifs déclenchés si e-mail vide/invalide ou consentement non coché

Fait quand : parcours clavier complet réalisé sur les deux pages, focus visible confirmé, résultat noté.

## Test d'inscription réelle

Soumettre le formulaire `interet-vertia` en production (`https://vertia-v0.netlify.app`) avec une adresse de test.
- la redirection vers `/merci/` s'effectue
- la soumission apparaît dans Netlify Forms
- un e-mail de notification arrive sur `jegeekutile.rec@gmail.com`

Fait quand : e-mail de notification reçu suite à la soumission de test.
