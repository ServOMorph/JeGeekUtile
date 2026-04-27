<p align="center">
  <img src="ASSETS/IMAGES/LOGOS/logo_titre_transparent_1.png" alt="Je Geek Utile" width="400"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/ServOMorph/JeGeekUtile?color=2d5016" alt="Licence MIT"/>
  <img src="https://img.shields.io/badge/tests-100%25-brightgreen" alt="Tests 100%"/>
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/version-3.0--dev-informational" alt="Version 3.0-dev"/>
  <img src="https://img.shields.io/badge/statut-en--developpement-orange" alt="En développement"/>
  <img src="https://img.shields.io/badge/pixels--blancs-%3C5%25-2d5016" alt="Eco-responsable"/>
</p>

# Je Geek Utile

**La technologie au service de l'humain — pas l'inverse.**

Boîte à outils open source pour associations : site web Flask complet, agents IA Claude Code orchestrés, console de gestion, et applications satellites. Éco-responsable par conception, traçable, auto-suffisant. Conçu par et pour des bénévoles qui veulent que la tech reste un outil, pas une fin.

---

## Pourquoi ce projet ?

Les associations manquent d'outils numériques adaptés — soit trop chers, soit trop complexes, soit conçus sans elles. JGU part d'un constat simple : la tech devrait être au service de ceux qui s'engagent, pas l'inverse.

- **L'IA doit rester un outil, pas un oracle.** Notre système d'agents orchestrés (Robert, Halu, PromptParfait...) intègre la détection d'hallucinations dès le départ — parce qu'on pense que l'IA fiable, c'est une IA qu'on contrôle.
- **Le numérique a un coût énergétique.** On impose thème sombre, zéro dépendance externe, moins de 5% de pixels blancs. Pas comme contrainte, comme valeur.
- **Un bénévole ne devrait pas avoir besoin d'une DSI.** Tout est auto-hébergeable, documenté, modulaire, et lancé en 3 commandes.

---

## Vue d'ensemble

Le projet regroupe plusieurs composants interdépendants :

- **Site internet** — Application Flask (25 templates, BDD SQLite, espace membre/admin)
- **Système d'agents IA** — 6 agents Claude Code orchestrés par Robert
- **Console agents** — Interface web de gestion/benchmark des agents (Vanilla JS)
- **Applications satellites** — auto_ia, stat_usage_ia, modele_appli

---

## Architecture

```
JeGeekUtile/
├── .claude/
│   ├── CLAUDE.md                         # Instructions Claude Code
│   └── commands/                         # 9 commandes Claude Code
│       ├── robert.md                     # Orchestrateur workflow
│       ├── halu.md                       # Détecteur hallucinations
│       ├── promptparfait.md              # Optimiseur prompts
│       ├── adminia.md                    # Démarches administratives
│       ├── comia.md                      # Communication GitHub/Mastodon
│       ├── partenaires-integrateur.md    # Intégration valeurs partenaires
│       ├── rgpd.md                       # Analyse conformité RGPD
│       ├── imageprompt.md                # Générateur prompts images
│       ├── start.md                      # Hook démarrage session
│       └── close.md                      # Hook fin session
│
├── AGENTS/
│   └── Agent Gestion Partenariats Multi-Valeurs/
│       └── Agent Gestion Partenariats Multi-Valeurs.md
│
├── applis/
│   ├── auto_ia/                          # API HTTP automatisation souris/clavier (v1.6.3)
│   │   ├── api/                          # http_server.py (Flask)
│   │   ├── core/                         # mouse, keyboard, actions, zones, tutorial
│   │   ├── web/                          # Interface Vanilla JS
│   │   └── main.py
│   │
│   ├── stat_usage_ia/                    # Tracker usage IA local vs cloud
│   │   ├── donnees/                      # ias.json, clics.json
│   │   ├── index.html
│   │   ├── app.js
│   │   ├── style.css
│   │   └── server.py                     # Backend Flask
│   │
│   └── modele_appli/                     # Template réutilisable pour toutes applis JGU
│       ├── donnees/config.json
│       ├── app.js / index.html / style.css
│       └── CHARTE_GRAPHIQUE_APPLI.md
│
├── administration/                       # Cadre légal association loi 1901
├── communication/                        # Charte graphique, prompts visuels, ComIA
│   └── visuels/                          # Logos, banners, geekos, Mastodon, vidéos
│
├── console-agents/                       # Interface web agents (Vanilla JS, port 8000)
│   ├── index.html / app.js / eco.css
│   ├── config.json
│   └── donnees/                          # agents.json, sessions.json (copies locales)
│
├── docs/
│   ├── COM/                              # Prompts images, logos, banners
│   ├── monnaie_virtuelle.md              # Système Geekos
│   ├── plaidoyer/                        # Arguments société
│   └── site_internet/GUIDE_SEO_IA_SEARCH.md
│
├── donnees/                              # Données centralisées
│   ├── agents.json                       # 6 agents configurés
│   └── sessions.json                     # Index + statistiques (6 sessions, 100% moy.)
│
├── sessions/                             # Archives sessions tests (par date)
│   └── {AAAA-MM-JJ}/{id}.json
│
├── site internet/                        # Application Flask
│   ├── app.py                            # 100+ routes, Flask + SQLAlchemy
│   ├── instance/jegeekutile.db           # BDD SQLite
│   ├── static/
│   │   ├── css/                          # style.css, theme-famicloud.css
│   │   ├── images/                       # banners, cards, logos, membres, nav
│   │   └── js/main.js
│   ├── templates/                        # 25 templates Jinja2
│   └── requirements.txt
│
├── tests/
│   └── runner.py                         # Exécuteur tests unifié
│
├── config.py                             # PORT_SITE=5000, DEBUG
├── config.json                           # Configuration globale complète
├── run.py                                # Lanceur site web (ouvre navigateur automatiquement)
├── trace_workflow.py                     # Traçage workflows agents
├── CONTEXT.md                            # Document de référence complet du projet
└── README.md
```

---

## Démarrage rapide

### Prérequis

- Python 3.8+
- Navigateur web moderne

### Site internet (port 5000)

```bash
# Lancer le site Flask (ouvre le navigateur automatiquement)
python run.py
```

Ou manuellement :

```bash
cd "site internet"
pip install -r requirements.txt
python app.py
# http://localhost:5000
```


### Console agents (port 8000)

```bash
cd console-agents
python -m http.server 8000
# http://localhost:8000
```

### Tracker usage IA (port 5000 — lancer séparément du site)

```bash
cd applis/stat_usage_ia
pip install -r requirements.txt
python server.py
```

### API auto_ia (port 8000)

```bash
cd applis/auto_ia
python main.py
```

---

## Agents IA

6 agents Claude Code organisés en hiérarchie :

| Agent | Niveau | Parent | Rôle |
|-------|--------|--------|------|
| **Robert** | 0 | — | Orchestrateur principal |
| **Halu** | 1 | Robert | Détecteur d'hallucinations |
| **AdminIA** | 1 | Robert | Démarches administratives |
| **ComIA** | 1 | Robert | Communication GitHub/Mastodon |
| **Partenaires-Intégrateur** | 1 | Robert | Intégration valeurs partenaires |
| **PromptParfait** | 2 | Halu | Optimiseur de prompts |

### Commandes disponibles

| Commande | Fonction |
|----------|----------|
| `/robert [demande]` | Orchestre workflow complet (validation → optimisation → confirmation) |
| `/halu [prompt]` | Détecte contradictions, extrapolations, incohérences |
| `/promptparfait [prompt]` | Réécriture pour concision et clarté maximales |
| `/adminia [demande]` | Rédaction lettres, formulaires administratifs |
| `/comia [action]` | Génère posts Mastodon, met à jour roadmap GitHub |
| `/partenaires-integrateur` | Workflow intégration valeurs partenaires en 5 étapes |
| `/rgpd [texte/config]` | Analyse conformité RGPD |
| `/imageprompt [description]` | Génère prompts images (Midjourney/DALL-E) |

### Workflow /robert

```
1. Réception prompt utilisateur
2. Validation anti-hallucination (Halu)
3. Optimisation prompt (PromptParfait)
4. Validation finale (Halu)
5. Confirmation utilisateur → Exécution
```

---

## Site Internet Flask

### Modèles de données (BDD SQLite)

- **User** — email, mot de passe, profil bénévole, monnaie Geekos, missions
- **Appetence** — centres d'intérêt (M2M avec User)
- **ActivityLog** — traçage complet sessions/événements
- **Evenement** — titre, date, lieu, statut
- **MembreEquipe** — équipe, bio, liens

### Templates (25 pages)

**Public** : accueil, à propos, services, contact, mentions légales, RGPD, cookies, login, inscription, notre projet, qui sommes-nous

**Espace membre** : profil, tableau de bord bénévole, formulaire bénévole, suppression compte

**Administration** : dashboard, statistiques, détail bénévole, aperçu bénévole, gestion événements, logs d'activité

---

## Applications Satellites

### auto_ia (v1.6.3)

API HTTP REST pour automatisation souris/clavier depuis un agent IA :

- Souris : déplacement, clic, double-clic, scroll
- Clavier : écriture, raccourcis, copier-coller
- File d'actions FIFO avec worker thread
- Zones nommées (abstraction coordonnées)
- Tutoriel gamifié, safe mode, rate limiting (200 actions/min)

**Endpoints principaux** : `POST /action`, `POST /queue/actions`, `GET /queue/status`, `POST /zones`

### stat_usage_ia

Tracker du ratio usage IA local vs cloud. Objectif : 70% local.

- Dashboard avec boutons par IA
- Statistiques en temps réel
- Persistance JSON (ias.json, clics.json)

### modele_appli

Template HTML/JS/CSS réutilisable pour toutes les nouvelles applis JGU, conforme à la charte graphique.

---

## Tests

```bash
python tests/runner.py
```

Dernière session (2026-02-25) : **100% — 19/19 tests réussis** (6 agents couverts)

Seuil de réussite : **80%**

**Tests effectués** :
- Tests agents (définis dans `donnees/agents.json`)
- Tests système : structure dossiers, archivage sessions, indexation, UI, config

**Résultat** : Score global, détails par test (OK/ERR), archive automatique dans `sessions/`.

---

## Traçage des Workflows

```python
from trace_workflow import WorkflowTracer

tracer = WorkflowTracer()
tracer.log_etape(
    agent='robert',
    type_etape='reception_prompt',
    contenu='Mon prompt...',
    resultat='Workflow démarré'
)
tracer.calculer_score()
tracer.sauvegarder()
```

Consultation : Console web → Vue Recherche → Clic sur session

---

## Configuration

### config.py

```python
PORT_SITE = 5000
DEBUG = True
```

### config.json (global)

```json
{
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
    "seuil_reussite": 80,
    "timeout_sec": 30,
    "iterations": 5
  },
  "trace": {
    "active": true,
    "niveau": "complet",
    "retention_jours": 365
  },
  "performance": {
    "limite_tokens": 200000,
    "optimisation_eco": true
  }
}
```

---

## Créer un Nouvel Agent

**1. Créer `.claude/commands/monagent.md` :**

```markdown
# /monagent - Description courte

## Rôle
Description du rôle.

## Tâche
1. Étape 1
2. Étape 2
```

**2. Ajouter dans `donnees/agents.json` :**

```json
{
  "id": "monagent",
  "nom": "MonAgent",
  "role": "Description courte",
  "niveau": 1,
  "parent": "robert",
  "competences": ["competence1", "competence2"],
  "score": 0,
  "tests": [{"nom": "test-1", "type": "validation"}]
}
```

**3. Créer via interface web :** Console → Vue Pyramide → "Créer nouvel agent"

---

## Monnaie Virtuelle — Geekos

Système de récompense pour bénévoles (10 à 200 geekos selon mission). Non convertible, personnel, non transférable, sans expiration.

---

## Principes de Conception

1. **Simplicité** — Architecture minimale, pas de sur-ingénierie
2. **Performance** — Vanilla JS, zéro dépendance externe
3. **Éco-responsabilité** — Pixels blancs < 5%, thème sombre obligatoire
4. **Traçabilité** — Tous échanges enregistrés et consultables
5. **Autonomie** — Système complet, auto-suffisant
6. **Modularité** — Agents indépendants, ajout facile

---

## Ressources

- **Référence projet** : `CONTEXT.md`
- **Instructions Claude Code** : `.claude/CLAUDE.md`
- **Suivi développement** : `docs/tracking.md`
- **Charte graphique** : `communication/CHARTE_GRAPHIQUE_JGU.md`
- **Guide SEO** : `docs/site_internet/GUIDE_SEO_IA_SEARCH.md`

---

## Statistiques

| Métrique | Valeur |
|----------|--------|
| Agents configurés | 6 |
| Commandes Claude Code | 9 |
| Templates Jinja2 | 25 |
| Sessions tests archivées | 6 |
| Dernier score tests | 100% (19/19) |
| Applications satellites | 3 |
| Partenariats documentés | En cours |

---

## Roadmap

Suivi complet de la progression : objectifs, tâches par phase, métriques.

Voir [docs/ROADMAP_GITHUB_VISIBILITE.md](docs/ROADMAP_GITHUB_VISIBILITE.md)

---

## Comment contribuer ?

Les contributions sont les bienvenues — issues, PRs, retours d'usage.

1. Fork le repo
2. Crée une branche (`git checkout -b feature/ma-contribution`)
3. Commit (`git commit -m 'feat: description'`)
4. Push et ouvre une PR

Pour les bugs ou idées : ouvre une [issue](https://github.com/ServOMorph/JeGeekUtile/issues).

---

## Licence

MIT — voir [LICENSE](LICENSE)

---

**Version :** 3.0 (dev)
**Dernière mise à jour :** 27/04/2026
**Statut :** En développement
