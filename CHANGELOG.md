# Changelog — JeGeekUtile

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [3.0.1] - 2026-05-13

### Added

- **Module AntiSpams** : Analyse locale d'emails pour détection violations RGPD
  - Scoring heuristique 0-100 (tracking pixels, opt-out, mention RGPD, etc.)
  - Connexion IMAP Free.fr (imap.free.fr:993 SSL, lecture seule)
  - Plaidoyer MD + JSON avec validation humaine obligatoire
  - Frontend Vanilla JS + CSS sombre (charte JGU)
  - Anonymisation données personnelles (emails, téléphones)
  - Tests pytest : 52/52 passés, coverage 91% (seuil 80%)
  - Port 8020, zéro dépendance externe (stdlib + Flask)

### Changed

- Mise à jour ROADMAP.md : ajout phase ANTISPAMS (urgent)
- Version package.json : 3.0.0-dev → 3.0.1

### Modified (v3)

- v3/.gitignore : ajustements
- v3/src/templates/dashboard.html : en cours responsiveness
- v3/temp_learnings.md : supprimé

---

## [3.0.0] - 2026-04-27

### Initial Release

- Core Dashboard + Auth + Reset MDP (Phase 5)
- App "Présentation" (Phase 6)
- Dashboard UI + Navigation (Phase 7)
- Système Progression (Phase 8 partielle)
- Panel Admin + Config Dynamique (Phase 9 partielle)
- Charte Graphique + Agencement UI (Phase 10 partielle)
- Tests coverage ≥ 85%

---

## Format

Ce fichier suit [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) et respecte le [Semantic Versioning](https://semver.org/).

### Types

- **Added** : Nouvelles fonctionnalités
- **Changed** : Changements d'architecture/API existante
- **Deprecated** : Fonctionnalités bientôt supprimées
- **Removed** : Fonctionnalités supprimées
- **Fixed** : Correctifs de bugs
- **Security** : Corrections failles de sécurité
