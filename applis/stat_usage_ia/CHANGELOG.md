# Changelog - Tracker Usage IA

## v1.0 - 26/11/2025

### Fonctionnalités initiales

- Dashboard avec boutons cliquables par IA
- Gestion IA (ajout/suppression)
- Statistiques détaillées
- Footer "@Je Geek Utile" avec date et version
- Persistance JSON avec horodatage

### IAs pré-configurées

**Cloud (5)** :
- ChatGPT
- Claude
- Comet
- Grok
- Gemini

**Local (2)** :
- VertIA
- Whisper

### Améliorations visuelles

#### Séparation Cloud/Local
- Dashboard divisé en 2 sections distinctes
- En-tête pour chaque section avec compteur
- Couleurs différenciées :
  - **Local** : Vert (#6b8e23) - Background #2d5016
  - **Cloud** : Orange (#ff8c00) - Background #3d2d1d

#### Headers de section
- Background vert foncé (#2d5016) pour IAs Locales
- Background marron (#4a3020) pour IAs Cloud
- Bordure gauche épaisse (6px) avec couleur type
- Compteur d'IAs dans chaque section

#### Cartes IA
- Bordures 3px (4px au hover)
- Backgrounds différents par type
- Hover avec elevation et glow
- Transitions fluides

### Corrections

- Gestion erreurs améliorée (messages détaillés)
- Validation champ nom obligatoire
- Chemins absolus dans server.py
- Logs console pour debugging
- Script start.bat pour Windows

### Documentation

- README.md : Documentation complète
- GUIDE_UTILISATION.md : Guide utilisateur
- DEMARRAGE.md : Guide démarrage et dépannage
- CHANGELOG.md : Historique versions

---

## Palette Couleurs

### IAs Locales
- Bordure : #6b8e23 (vert)
- Background : #2d5016 (vert foncé)
- Hover : #3d6026 (vert moyen)
- Header : #2d5016

### IAs Cloud
- Bordure : #ff8c00 (orange)
- Background : #3d2d1d (marron foncé)
- Hover : #4d3d2d (marron moyen)
- Header : #4a3020

### Global
- Background principal : #1a1a1a
- Texte principal : #b8b8b8
- Footer : #2d2d2d

---

## Objectif

**Favoriser usage IAs locales : ≥ 70%**

### Pourquoi ?
- Confidentialité des données
- Pas de coûts d'abonnement
- Pas de latence réseau
- Autonomie complète

---

**Version actuelle** : 1.0
**Auteur** : @Je Geek Utile
**Date** : 26/11/2025
