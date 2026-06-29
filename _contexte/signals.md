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

## Dernière session — 2026-06-29

### Décisions prises
- La landing page V4 est le point d'entrée public du projet (standalone HTML, sans backend)
- Ollama/IA locale posé comme valeur de base, pas option secondaire
- Flux Discord pur : aucune inscription, aucun formulaire
- Nettoyage du système agents IA reporté à la prochaine session

### Livrables produits ou modifiés
- `site internet/V4/index.html` : créé et finalisé
- `site internet/V4/README.md` : créé
- `CHANGELOG.md` : entrée [4.0.0] ajoutée
- `README.md` : V4 intégrée, version bumpée à 4.0.0
- `_contexte/signals.md` : TODO nettoyage agents ajouté

### Prochaine étape exacte
Nettoyer le projet : supprimer AGENTS/, console-agents/, donnees/agents.json, sessions/, trace_workflow.py et commandes Claude agents. Puis mettre à jour README et CHANGELOG.
