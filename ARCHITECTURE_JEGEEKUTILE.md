# Architecture — JeGeekUtile

Ce document détaille l'écosystème technique de JeGeekUtile, intégrant le site web, les agents IA et les services satellites.

## 🏗️ Vision d'Ensemble

JeGeekUtile est conçu comme un hub d'outils pour associations, orchestré par l'IA et axé sur l'éco-responsabilité. Le projet est actuellement en transition vers la **Version 3.0**, visant une refonte de l'UI et une modularité accrue.


### Arborescence Structurée

```text
JeGeekUtile/
├── .claude/                # Intelligence (Claude Code)
│   └── commands/           # Logique des agents (Robert, Halu, etc.)
├── AGENTS/                 # Documentation métier des agents
├── site internet/          # Application Flask (Cœur)
│   ├── app.py              # Backend & Routes
│   ├── templates/          # Vues Jinja2 (25 pages)
│   └── instance/           # BDD SQLite
├── console-agents/         # Interface de pilotage (Vanilla JS)
├── applis/                 # Services satellites
│   ├── auto_ia/            # Automatisation clavier/souris
│   └── stat_usage_ia/      # Tracker d'usage IA
├── donnees/                # Données centralisées (JSON)
├── docs/                   # Documentation projet
└── tests/                  # Validation système
```

## 🤖 Système d'Agents IA

Les agents sont organisés en hiérarchie de commande :

1.  **Robert (Orchestrateur)** : Reçoit les demandes, délègue aux agents de niveau 1, et valide le résultat final.
2.  **Halu (Niveau 1)** : Gardien de la vérité. Détecte les hallucinations et incohérences.
3.  **PromptParfait (Niveau 2)** : Optimise les instructions pour maximiser la clarté et l'efficacité des modèles.
4.  **ComIA / AdminIA** : Agents métier spécialisés dans la communication et l'administratif.

## 🌐 Site Internet (Flask)

- **Backend** : Flask avec SQLAlchemy pour la gestion SQLite.
- **Frontend** : Templates Jinja2 utilisant un thème sombre "éco-responsable" (< 5% de pixels blancs).
- **Fonctionnalités** : Gestion des membres, journalisation d'activité, système Geekos, gestion d'événements.

## 📡 Applications Satellites

- **auto_ia** : Expose une API REST locale pour permettre aux agents IA de simuler des interactions humaines (souris/clavier).
- **stat_usage_ia** : Tableau de bord de suivi de la consommation IA (Local vs Cloud).
- **console-agents** : Dashboard unifié pour monitorer les sessions des agents et les benchmarks.

## 💾 Flux de Données & Persistance

1.  **Centralisation** : Les configurations d'agents et les statistiques de sessions sont stockées dans `donnees/*.json`.
2.  **Traçabilité** : Chaque étape de workflow est enregistrée via `trace_workflow.py` pour un audit complet.
3.  **Bases de données** : SQLite est utilisé pour les données structurées relationnelles (membres, logs, événements).

---
*Dernière génération : 27/04/2026*
