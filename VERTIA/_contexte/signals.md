# Signals — vertia   (MAJ 2026-08-29)

## Actions ouvertes
- [P1|ouvert] Activer et tester la notification Netlify Forms vers l'adresse de réception définie.
  - fait quand: une soumission de test validée génère un e-mail de notification.
  - réf: `site/index.html`, tableau Netlify > Forms et Notifications.
- [P1|ouvert] Compléter les informations obligatoires de confidentialité avant publication publique.
  - fait quand: responsable, contact, durée de conservation et droits sont renseignés dans la politique.
  - réf: `site/confidentialite.html`, `specification_mvp1.md`.
- [P2|ouvert] Choisir une des trois directions graphiques pour la faire évoluer.
  - fait quand: une direction est explicitement sélectionnée.
  - réf: `designs/index.html`.

## Contexte chaud
- Déploiement brouillon validé : `https://6a93025eaa31b9e46662d284--vertia-v0.netlify.app`.
- La configuration Netlify utilise `VERTIA` comme base, `site` comme dossier publié et une commande de build vide.

## Dernière session (2026-08-29)
# Session du 2026-08-29

## Décisions prises
- Le MVP 1 est une landing statique Netlify avec formulaire Netlify Forms.
- Les valeurs de sobriété, éthique, durabilité et assistance au jugement humain sont intégrées.

## Livrables produits ou modifiés
- `site/`, `designs/`, `specification_mvp1.md` et `roadmap_vertia.md` : créés et mis à jour.
- `netlify.toml` et `scripts/` : intégration Netlify adaptée à une landing statique.

## Hypothèses validées / invalidées
- VALIDE : un déploiement brouillon Netlify de la landing fonctionne.
- INVALIDE : Hugo n'est pas nécessaire ; la commande de build est vide.
- EN ATTENTE : notification Forms et informations de confidentialité avant publication publique.

## Prochaine étape exacte
Activer puis tester une notification de soumission Netlify, compléter la politique de confidentialité et choisir une direction graphique.

## Question bloquante pour la session suivante
Aucune.
