# Contexte stable

## Objectif
JeGeekUtile — boîte à outils open source pour associations. La technologie au service de l'humain.

## État actuel
- V4 landing page restructurée : suppression des sections concept et étapes, intégration des textes ciblés sur les étudiants en informatique.
- V3 (Flask) stable : dashboard responsive, tests 74/74, coverage 91.67%
- Nettoyage agents IA à faire (P1 — voir signals.md)
- Éléments V4 restants : lien Discord réel + jour de la semaine à définir (P2 — voir signals.md)

## Décisions structurantes
- Charte graphique : neon #00ff88 / bg #050705 / magenta #ff2d95 — obligatoire sur toutes les surfaces
- Éco-responsabilité : thème sombre, pixels blancs < 5%, zéro dépendance externe inutile
- IA locale (Ollama) = valeur de base, pas option — mentionner systématiquement aux côtés des outils cloud
- Flux V4 : Discord uniquement, sans formulaire ni inscription
- V4 = fichier HTML standalone (pas de backend)
- Simplification du contenu : élimination systématique des redondances pour privilégier une page concise.

## Stack
- Site V3 : Python 3.8+, Flask, SQLAlchemy, SQLite, Jinja2
- Landing V4 : HTML/CSS standalone, Google Fonts uniquement
- Agents : Claude Code (`.claude/commands/`)
- Applications satellites : Vanilla JS + Flask
