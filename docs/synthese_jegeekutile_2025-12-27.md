# Synthese Projet Je Geek Utile

**Date de generation** : 27/12/2025
**Version** : 1.0

---

## Table des matieres

1. [Presentation generale](#presentation-generale)
2. [Architecture du projet](#architecture-du-projet)
3. [Console Agents IA](#console-agents-ia)
4. [Applications](#applications)
5. [Site Internet](#site-internet)
6. [Systeme de benevoles](#systeme-de-benevoles)
7. [Administration](#administration)
8. [Documentation](#documentation)
9. [Configuration](#configuration)
10. [Tests et qualite](#tests-et-qualite)

---

## Presentation generale

**Je Geek Utile** est un projet associatif comprenant :
- Un systeme de gestion d'agents IA avec orchestration
- Un site internet pour l'association
- Des applications de suivi et d'automatisation
- Un systeme de benevolat avec monnaie virtuelle (Geekos)

### Fichiers racine

| Fichier | Description |
|---------|-------------|
| [README.md](../README.md) | Documentation principale du projet |
| [LANCEMENT.md](../LANCEMENT.md) | Guide de demarrage rapide |
| [config.json](../config.json) | Configuration globale |
| [trace_workflow.py](../trace_workflow.py) | Tracage des workflows agents |

---

## Architecture du projet

```
JeGeekUtile/
|-- .claude/                    # Instructions Claude Code
|-- administration/             # Gouvernance association
|-- applis/                     # Applications
|   |-- auto_ia/               # Automatisation souris/clavier
|   |-- modele_appli/          # Template applications
|   |-- stat_usage_ia/         # Tracker usage IA
|-- benevolat/                  # Systeme benevoles
|-- communication/              # Supports communication
|-- console-agents/             # Interface web agents IA
|-- docs/                       # Documentation
|-- donnees/                    # Donnees partagees
|-- notes_persos/               # Notes personnelles
|-- plan_d_actions/             # Planification
|-- sessions/                   # Archives sessions
|-- site internet/              # Site web Flask
|-- tests/                      # Tests automatises
```

---

## Console Agents IA

Systeme de gestion, orchestration et benchmark d'agents IA avec interface web eco-responsable.

### Agents configures

| Agent | Role | Niveau |
|-------|------|--------|
| **Robert** | Orchestrateur principal | 0 |
| **Halu** | Detecteur d'hallucinations | 1 |
| **PromptParfait** | Optimiseur de prompts | 2 |
| **AdminIA** | Specialiste demarches administratives | 1 |

### Fichiers console-agents

| Fichier | Description |
|---------|-------------|
| [index.html](../console-agents/index.html) | Page principale interface |
| [app.js](../console-agents/app.js) | Application Vanilla JS |
| [eco.css](../console-agents/eco.css) | Styles eco-responsables |
| [config.json](../console-agents/config.json) | Configuration UI |
| [donnees/agents.json](../console-agents/donnees/agents.json) | Base agents |
| [donnees/sessions.json](../console-agents/donnees/sessions.json) | Index sessions |

### Commandes Claude Code

| Commande | Fichier | Description |
|----------|---------|-------------|
| /robert | [robert.md](../.claude/commands/robert.md) | Orchestrateur workflow |
| /halu | [halu.md](../.claude/commands/halu.md) | Detecteur hallucinations |
| /promptparfait | [promptparfait.md](../.claude/commands/promptparfait.md) | Optimiseur prompts |
| /start | [start.md](../.claude/commands/start.md) | Hook demarrage |
| /close | [close.md](../.claude/commands/close.md) | Hook fin session |

### Workflow /robert

```
1. Reception prompt utilisateur
2. Validation initiale (/halu)
3. Optimisation prompt (/promptparfait)
4. Validation finale (/halu)
5. Demande confirmation -> Execution
```

### Lancement interface

```bash
cd console-agents
python -m http.server 8000
# URL: http://localhost:8000
```

---

## Applications

### 1. Tracker Usage IA

Application web pour monitorer l'utilisation des IA locales vs cloud.
**Objectif** : 70% d'utilisation IA locales

| Fichier | Description |
|---------|-------------|
| [README.md](../applis/stat_usage_ia/README.md) | Documentation |
| [GUIDE_UTILISATION.md](../applis/stat_usage_ia/GUIDE_UTILISATION.md) | Guide utilisateur |
| [DEMARRAGE.md](../applis/stat_usage_ia/DEMARRAGE.md) | Instructions demarrage |
| [index.html](../applis/stat_usage_ia/index.html) | Interface web |
| [app.js](../applis/stat_usage_ia/app.js) | Frontend JavaScript |
| [style.css](../applis/stat_usage_ia/style.css) | Styles mode sombre |
| [server.py](../applis/stat_usage_ia/server.py) | Backend Flask |
| [start.bat](../applis/stat_usage_ia/start.bat) | Script lancement Windows |
| [donnees/ias.json](../applis/stat_usage_ia/donnees/ias.json) | Liste IA configurees |
| [donnees/clics.json](../applis/stat_usage_ia/donnees/clics.json) | Historique clics |

**Lancement** :
```bash
cd applis/stat_usage_ia
python server.py
# URL: http://localhost:5000
```

### 2. Auto IA

Application d'automatisation de clics souris et copier-coller via API HTTP.
**Version** : 1.6.3

| Fichier | Description |
|---------|-------------|
| [README.md](../applis/auto_ia/README.md) | Documentation complete |
| [PROMPT_COMET.md](../applis/auto_ia/PROMPT_COMET.md) | Prompt pour Comet |
| [main.py](../applis/auto_ia/main.py) | Point d'entree serveur |
| [requirements.txt](../applis/auto_ia/requirements.txt) | Dependances Python |
| [test_api.py](../applis/auto_ia/test_api.py) | Tests API |

**Modules core** :
| Fichier | Description |
|---------|-------------|
| [core/mouse_controller.py](../applis/auto_ia/core/mouse_controller.py) | Controle souris |
| [core/keyboard_clipboard.py](../applis/auto_ia/core/keyboard_clipboard.py) | Clavier et presse-papiers |
| [core/actions.py](../applis/auto_ia/core/actions.py) | Gestionnaire actions |
| [core/zones.py](../applis/auto_ia/core/zones.py) | Zones nommees |
| [core/tutorial.py](../applis/auto_ia/core/tutorial.py) | Tutoriel gamifie |

**Interface web** :
| Fichier | Description |
|---------|-------------|
| [web/index.html](../applis/auto_ia/web/index.html) | Interface principale |
| [web/styles.css](../applis/auto_ia/web/styles.css) | Styles mode sombre |
| [web/app.js](../applis/auto_ia/web/app.js) | Application JavaScript |

**Lancement** :
```bash
cd applis/auto_ia
pip install -r requirements.txt
python main.py
# API: http://127.0.0.1:8000
```

### 3. Modele Application

Template reutilisable pour toutes les applications du projet.

| Fichier | Description |
|---------|-------------|
| [README.md](../applis/modele_appli/README.md) | Documentation modele |
| [CHARTE_GRAPHIQUE_APPLI.md](../applis/modele_appli/CHARTE_GRAPHIQUE_APPLI.md) | Charte graphique |
| [OPTIMISATIONS.md](../applis/modele_appli/OPTIMISATIONS.md) | Guide optimisations |
| [index.html](../applis/modele_appli/index.html) | Template HTML |
| [app.js](../applis/modele_appli/app.js) | Template JavaScript |
| [style.css](../applis/modele_appli/style.css) | Template CSS |
| [donnees/config.json](../applis/modele_appli/donnees/config.json) | Template config |

**Charte graphique** :
```css
--bg-primary: #1a1a1a       /* Background principal */
--bg-secondary: #2d2d2d     /* Background secondaire */
--accent-primary: #2d5016   /* Accent vert fonce */
--accent-secondary: #6b8e23 /* Accent vert clair */
--text-primary: #b8b8b8     /* Texte principal */
```

---

## Site Internet

Site web Flask pour l'association Je Geek Utile avec systeme de comptes utilisateurs et administration.

### Fichiers principaux

| Fichier | Description |
|---------|-------------|
| [app.py](../site%20internet/app.py) | Application Flask principale |
| [requirements.txt](../site%20internet/requirements.txt) | Dependances Python |
| [run.bat](../site%20internet/run.bat) | Script lancement Windows |
| [SEO_CHECKLIST.md](../site%20internet/SEO_CHECKLIST.md) | Checklist SEO |

### Templates

| Fichier | Description |
|---------|-------------|
| [base.html](../site%20internet/templates/base.html) | Template de base |
| [accueil.html](../site%20internet/templates/accueil.html) | Page d'accueil |
| [a_propos.html](../site%20internet/templates/a_propos.html) | Page a propos |
| [services.html](../site%20internet/templates/services.html) | Page services |
| [contact.html](../site%20internet/templates/contact.html) | Page contact |
| [login.html](../site%20internet/templates/login.html) | Page connexion |
| [inscription.html](../site%20internet/templates/inscription.html) | Page inscription |
| [profil.html](../site%20internet/templates/profil.html) | Page profil utilisateur |
| [espace_membre.html](../site%20internet/templates/espace_membre.html) | Espace membre |
| [formulaire_benevole.html](../site%20internet/templates/formulaire_benevole.html) | Formulaire benevole |
| [admin.html](../site%20internet/templates/admin.html) | Administration |
| [admin_stats.html](../site%20internet/templates/admin_stats.html) | Statistiques admin |
| [admin_benevole_detail.html](../site%20internet/templates/admin_benevole_detail.html) | Detail benevole |
| [admin_logs.html](../site%20internet/templates/admin_logs.html) | Logs activite |
| [404.html](../site%20internet/templates/404.html) | Page erreur 404 |

### Assets statiques

| Fichier | Description |
|---------|-------------|
| [static/css/style.css](../site%20internet/static/css/style.css) | Feuille de styles |
| [static/js/main.js](../site%20internet/static/js/main.js) | JavaScript principal |
| [static/robots.txt](../site%20internet/static/robots.txt) | Fichier robots.txt |
| [static/sitemap.xml](../site%20internet/static/sitemap.xml) | Sitemap XML |
| [static/images/logo.png](../site%20internet/static/images/logo.png) | Logo association |
| [static/images/favicon.png](../site%20internet/static/images/favicon.png) | Favicon |
| [static/images/geekos.png](../site%20internet/static/images/geekos.png) | Logo Geekos |

### Base de donnees

| Fichier | Description |
|---------|-------------|
| [instance/jegeekutile.db](../site%20internet/instance/jegeekutile.db) | Base SQLite |

### Fonctionnalites

- Inscription/Connexion utilisateurs
- Espace membre personnalise
- Gestion profil benevole
- Administration (gestion benevoles, stats, logs)
- Tracking activite utilisateurs
- Monnaie virtuelle Geekos

**Lancement** :
```bash
cd "site internet"
pip install -r requirements.txt
python app.py
# URL: http://localhost:5000
```

**Compte admin par defaut** :
- Email: admin@admin.com
- Mot de passe: admin123

---

## Systeme de benevoles

### Monnaie virtuelle Geekos

| Fichier | Description |
|---------|-------------|
| [monnaie_virtuelle.md](docs/monnaie_virtuelle.md) | Documentation Geekos |

**Bareme indicatif** :

| Action | Geekos |
|--------|--------|
| Mission courte (< 2h) | 10-30 |
| Mission moyenne (2-5h) | 30-80 |
| Mission longue (> 5h) | 80-200 |
| Participation evenement | 20 |
| Formation suivie | 50 |
| Formation animee | 100 |
| Parrainage actif | 50 |

### Appetences disponibles

- Informatique
- Communication
- Evenementiel
- Formation
- Redaction
- Design graphique
- Comptabilite
- Logistique
- Accueil
- Animation

---

## Administration

| Fichier | Description |
|---------|-------------|
| [gouvernance.txt](../administration/gouvernance.txt) | Regles de gouvernance |
| [association loi 1901.txt](../administration/association%20loi%201901.txt) | Statuts association |

---

## Documentation

### Dossier docs/

| Fichier | Description |
|---------|-------------|
| [tracking.md](docs/tracking.md) | Suivi des sessions |
| [monnaie_virtuelle.md](docs/monnaie_virtuelle.md) | Documentation Geekos |
| [prompts/init.txt](docs/prompts/init.txt) | Prompt initial |

### Plaidoyer

| Fichier | Description |
|---------|-------------|
| [playdoyer_v1.md](docs/plaidoyer/playdoyer_v1.md) | Plaidoyer version 1 |
| [playdoyer_v2.md](docs/plaidoyer/playdoyer_v2.md) | Plaidoyer version 2 |
| [sources/Plaidoyer Pour un accueil local inconditionnel -1.pdf](docs/sources/Plaidoyer%20Pour%20un%20accueil%20local%20inconditionnel%20-1.pdf) | Source PDF |

### Site internet

| Fichier | Description |
|---------|-------------|
| [GUIDE_SEO_IA_SEARCH.md](docs/site_internet/GUIDE_SEO_IA_SEARCH.md) | Guide SEO pour IA |

### Plan d'actions

| Fichier | Description |
|---------|-------------|
| [plan-optimise.md](../plan_d_actions/plan-optimise.md) | Plan optimise console agents |
| [spec-technique.json](../plan_d_actions/spec-technique.json) | Specifications techniques |

---

## Configuration

### Configuration globale

Fichier : [config.json](../config.json)

```json
{
  "chemins": {
    "agents": ".claude/commandes",
    "tests": "tests",
    "sessions": "sessions",
    "donnees": "donnees"
  },
  "ui": {
    "theme": {
      "bg": "#1a1a1a",
      "primary": "#2d5016",
      "text": "#b8b8b8",
      "accent": "#6b8e23"
    },
    "refresh_ms": 5000,
    "pixels_blancs_max_pct": 5
  },
  "tests": {
    "auto": true,
    "seuil_reussite": 80,
    "timeout_sec": 30
  },
  "trace": {
    "active": true,
    "niveau": "complet",
    "retention_jours": 365
  }
}
```

### Instructions Claude Code

Fichier : [.claude/CLAUDE.md](../.claude/CLAUDE.md)

- Communication en francais
- Ton professionnel
- Optimisation tokens
- Pas d'emojis dans le code

---

## Tests et qualite

### Runner de tests

| Fichier | Description |
|---------|-------------|
| [runner.py](../tests/runner.py) | Executeur tests unifie |

**Execution** :
```bash
python tests/runner.py
```

**Tests effectues** :
- Tests agents (definis dans agents.json)
- Test structure dossiers
- Test archivage sessions
- Test indexation recherche
- Test presence UI
- Test configuration valide

### Derniere session

- **Date** : 26/11/2025
- **Score** : 100% (11/11 tests)
- **Tokens** : ~87k

---

## Donnees partagees

| Fichier | Description |
|---------|-------------|
| [donnees/agents.json](../donnees/agents.json) | Configuration agents |
| [donnees/sessions.json](../donnees/sessions.json) | Historique sessions |

---

## Principes de conception

1. **Simplicite** : Architecture minimale, pas de sur-ingenierie
2. **Performance** : Vanilla JS, pas de dependances externes
3. **Eco-responsabilite** : Pixels blancs <5%, theme sombre
4. **Tracabilite** : Tous echanges enregistres et consultables
5. **Autonomie** : Systeme complet, auto-suffisant
6. **Modularite** : Agents independants, ajout facile

---

## Statistiques projet

| Metrique | Valeur |
|----------|--------|
| Fichiers core | ~50 |
| Applications | 3 |
| Agents IA | 4 |
| Score tests | 100% |
| Optimisation tokens plan | -77% |
| Reduction latence | -90% |

---

**Document genere automatiquement par /robert**
**Je Geek Utile - 2025**
