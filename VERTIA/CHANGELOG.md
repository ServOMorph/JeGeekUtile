# Changelog — VertIA

## v0.2 — 2026-09-01

### Modifié
- `site/styles.css` : styles de focus visibles (`:focus-visible`), respect de `prefers-reduced-motion` sur le défilement, plancher de taille des titres abaissé et `overflow-wrap` sur `h1/h2/h3` pour prévenir le débordement horizontal sur petits écrans.

### Supprimé
- Dossier `designs/` (trois propositions graphiques non retenues) ; historique conservé dans le commit `0c0b59f`.

### Ajouté
- `tests_manuels.md` : file d'attente des contrôles manuels (rendu mobile + zoom, navigation clavier, inscription réelle).

## v0.1 — 2026-08-30

### Ajouté
- Politique de confidentialité complétée : responsable du traitement (Raphaël Richard, à titre personnel), contact unique, finalité, base légale, durée de conservation, destinataires, transfert hors UE, droits RGPD, recours CNIL.
- Trois tests de conformité de la politique de confidentialité.

### Modifié
- Notification Netlify Forms redirigée vers `jegeekutile.rec@gmail.com`.
- `specification_mvp1.md` : mention "association loi 1901" corrigée.
- `scripts/netlify_deploy.ps1` : correction d'un bug PowerShell bloquant (stderr des commandes natives).

### Corrigé
- Suppression de l'encadré "à compléter avant publication" de la page de confidentialité, déployée en production.
