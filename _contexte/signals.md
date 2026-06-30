# Signaux - Actions ouvertes et blocages

## [P1] Nettoyage projet — suppression système agents IA

Supprimer toute la partie agents IA du projet :
- `AGENTS/`
- `donnees/agents.json`, `donnees/sessions.json`
- `sessions/` (archives sessions agents)
- `console-agents/`
- `trace_workflow.py`
- `.claude/commands/` : robert.md, halu.md, promptparfait.md, adminia.md, comia.md, partenaires-integrateur.md
- Mettre à jour `README.md` et `CHANGELOG.md` en conséquence

fait quand: ces dossiers/fichiers sont absents du repo et README ne les mentionne plus
réf: README.md section "Vue d'ensemble" + "Agents IA", CHANGELOG.md

## [P2] Compléter la landing page V4

- Remplacer le placeholder `https://discord.gg/` par le vrai lien Discord
- Définir le jour fixe de la semaine pour les sessions (actuellement "à définir ensemble")

fait quand: aucun placeholder dans site internet/V4/index.html
réf: site internet/V4/index.html — occurrences "discord.gg/" et "à définir ensemble"

---

## Dernière session — 2026-06-30

### Décisions prises
- Reformulation des textes au futur puis au présent partiel pour cibler précisément les étudiants et valoriser leurs études.
- Simplification des redondances : suppression des sections concept et étapes, simplification de la carte outil 05 et du bouton "Voir le projet" en bas de page.

### Livrables produits ou modifiés
- `site internet/V4/index.html` : modifié

### Hypothèses validées / invalidées
- VALIDE : alléger la page en enlevant les doublons fluidifie le parcours de lecture.

### Prochaine étape exacte
Nettoyer le projet : supprimer les répertoires et fichiers liés aux agents IA (AGENTS/, console-agents/, etc.).

### Question bloquante pour la session suivante
Aucune
