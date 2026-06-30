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
- Ollama intégré comme 7ème outil dans la section "L'arsenal" (suppression de la section "Valeur de base" séparée)
- Codex repositionné en 3ème position dans l'arsenal
- Layout outils : grille 3+4 (3 cartes ligne 1, 4 cartes ligne 2)
- Tuile "Présence / À ton rythme" ajoutée dans la section Format

### Livrables produits ou modifiés
- `site internet/V4/index.html` : refonte section outils (7 cartes, layout 3+4, Ollama intégré, section valeur de base supprimée), tuile Présence ajoutée

### Hypothèses validées / invalidées
- VALIDE : intégrer Ollama dans l'arsenal des outils plutôt qu'en section séparée

### Prochaine étape exacte
Nettoyer le projet : supprimer AGENTS/, console-agents/, donnees/agents.json, sessions/, trace_workflow.py et commandes Claude agents. Puis mettre à jour README et CHANGELOG.

### Question bloquante pour la session suivante
Aucune
