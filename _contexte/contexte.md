# Contexte stable

## Objectif
JeGeekUtile — boîte à outils open source pour associations. La technologie au service de l'humain.

## État actuel
- V4 landing page affinée : Ollama intégré en 7ème outil (arsenal 3+4), section "Valeur de base" supprimée, tuile "Présence / À ton rythme" ajoutée au Format
- V3 (Flask) stable : dashboard responsive, tests 74/74, coverage 91.67%
- Nettoyage agents IA à faire (P1 — voir signals.md)
- Deux éléments V4 à compléter : lien Discord réel + jour de la semaine

## Décisions structurantes
- Charte graphique : neon #00ff88 / bg #050705 / magenta #ff2d95 — obligatoire sur toutes les surfaces
- Éco-responsabilité : thème sombre, pixels blancs < 5%, zéro dépendance externe inutile
- IA locale (Ollama) = valeur de base, pas option — mentionner systématiquement aux côtés des outils cloud
- Flux V4 : Discord uniquement, sans formulaire ni inscription
- V4 = fichier HTML standalone (pas de backend)

## Stack
- Site V3 : Python 3.8+, Flask, SQLAlchemy, SQLite, Jinja2
- Landing V4 : HTML/CSS standalone, Google Fonts uniquement
- Agents : Claude Code (`.claude/commands/`)
- Applications satellites : Vanilla JS + Flask
