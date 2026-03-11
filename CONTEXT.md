# CONTEXT.md — Je Geek Utile

**Document de référence projet pour IA**
Dernière mise à jour : 2026-02-25

---

## 1. Identité

**Nom** : Je Geek Utile (JGU)
**Type** : Association loi 1901
**Baseline** : "La technologie au service de l'humain"
**Valeurs** : Éco-responsabilité, éthique, transparence, sécurité des données, IA pour les humains
**Cible** : Grand public, tous publics

---

## 2. Architecture du dépôt

```
JeGeekUtile/
├── CONTEXT.md                  # Ce fichier (contexte projet IA)
├── README.md                   # Documentation console agents
├── LANCEMENT.md                # Guide démarrage rapide
├── config.json                 # Configuration globale
├── trace_workflow.py           # Traçage workflows agents
│
├── .claude/
│   ├── CLAUDE.md               # Instructions Claude Code (fr, pro, concis)
│   └── commands/               # Skills Claude Code
│       ├── robert.md           # Orchestrateur
│       ├── halu.md             # Détecteur hallucinations
│       ├── promptparfait.md    # Optimiseur prompts
│       ├── comia.md            # Agent communication
│       ├── rgpd.md             # Agent analyse RGPD
│       ├── imageprompt.md      # Générateur prompts images
│       ├── start.md            # Hook démarrage session
│       └── close.md            # Hook fin session
│
├── console-agents/             # Interface web gestion agents IA
│   ├── index.html
│   ├── app.js                  # Vanilla JS, mono-page
│   ├── eco.css                 # UI éco-responsable
│   ├── config.json
│   └── donnees/
│       ├── agents.json
│       └── sessions.json
│
├── donnees/                    # Données partagées racine
│   ├── agents.json
│   └── sessions.json
│
├── sessions/                   # Archives sessions tests
│   └── {YYYY-MM-DD}/{id}.json
│
├── applis/
│   ├── auto_ia/                # Automatisation souris/clavier via API HTTP
│   ├── stat_usage_ia/          # Tracker usage IA locale vs cloud
│   └── modele_appli/           # Template réutilisable applications
│
├── site internet/              # Site web Flask association
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── instance/jegeekutile.db
│
├── administration/             # Gouvernance association
├── benevolat/                  # Système bénévoles
├── communication/              # Supports com, charte, visuels
├── docs/                       # Documentation
├── plan_d_actions/             # Roadmap et specs
└── tests/runner.py             # Exécuteur tests unifié
```

---

## 3. Système d'agents IA (core)

### Hiérarchie

```
Robert (niveau 0) — Orchestrateur
├── Halu (niveau 1) — Détecteur hallucinations
│   └── PromptParfait (niveau 2) — Optimiseur prompts
├── AdminIA (niveau 1) — Démarches administratives
└── ComIA (niveau 1) — Communication GitHub/Mastodon
```

### Agents détaillés

| ID | Nom | Rôle | Compétences |
|----|-----|------|-------------|
| `robert` | Robert | Orchestrateur workflow | workflow, validation, orchestration |
| `halu` | Halu | Détecteur hallucinations | detection_hallucination, verification_faits |
| `promptparfait` | PromptParfait | Optimiseur prompts | reduction_tokens, clarte, restructuration |
| `adminia` | AdminIA | Démarches admin | rédaction administrative, formulaires officiels |
| `comia` | ComIA | Communication | strategie_communication, github, mastodon |

### Workflow Robert (/robert)

```
1. Réception prompt utilisateur
2. Validation initiale → /halu
3. Optimisation → /promptparfait
4. Validation finale → /halu
5. Demande confirmation utilisateur → Exécution si approuvé
```

### Skills Claude Code disponibles

| Commande | Fichier | Fonction |
|----------|---------|----------|
| `/start` | start.md | Init session, charge Robert |
| `/close` | close.md | Fin session |
| `/robert` | robert.md | Orchestrateur workflow |
| `/halu` | halu.md | Validation anti-hallucination |
| `/promptparfait` | promptparfait.md | Optimisation prompt |
| `/comia` | comia.md | Agent communication |
| `/rgpd` | rgpd.md | Analyse conformité RGPD |
| `/imageprompt` | imageprompt.md | Génération prompts visuels |

---

## 4. Site internet

**Stack** : Flask + SQLAlchemy + SQLite + Flask-Login
**BDD** : `site internet/instance/jegeekutile.db`

### Modèles de données

**User**
- email, password_hash, nom, prenom
- is_admin, is_benevole
- date_naissance, adresse, motivation, temps_disponible
- missions_realisees, missions_en_cours
- monnaie (Geekos, int)
- appetences (many-to-many → Appetence)

**Appetence** : nom (unique)

**ActivityLog** : timestamp, session_id, user_id, page, event_type, element, details

**Evenement** : titre, description, date_evenement, heure_debut, heure_fin, lieu

### Pages (templates)

| Template | Accès |
|----------|-------|
| accueil.html | Public |
| a_propos.html | Public |
| services.html | Public |
| contact.html | Public |
| mentions_legales.html | Public |
| politique_confidentialite.html | Public |
| politique_cookies.html | Public |
| login.html | Public |
| inscription.html | Public |
| profil.html | Connecté |
| espace_membre.html | Connecté |
| formulaire_benevole.html | Connecté |
| admin.html | Admin |
| admin_stats.html | Admin |
| admin_benevole_detail.html | Admin |
| admin_preview_benevole.html | Admin |
| admin_evenements.html | Admin |
| admin_logs.html | Admin |
| supprimer_compte.html | Connecté |

**Compte admin par défaut** : admin@admin.com / admin123

### Lancement site

```bash
cd "site internet"
pip install -r requirements.txt
python app.py
# URL: http://localhost:5000
```

---

## 5. Applications

### auto_ia

**Objet** : Automatisation souris/clavier via API HTTP REST
**Stack** : Python (FastAPI/Flask), Vanilla JS
**Port** : 8000
**Modules core** : mouse_controller.py, keyboard_clipboard.py, actions.py, zones.py, tutorial.py

```bash
cd applis/auto_ia && pip install -r requirements.txt && python main.py
```

### stat_usage_ia

**Objet** : Tracker usage IA locale vs cloud
**Objectif** : 70% utilisation IA locales
**Stack** : Python Flask (server.py) + Vanilla JS
**Port** : 5000
**Données** : donnees/ias.json, donnees/clics.json

```bash
cd applis/stat_usage_ia && python server.py
```

### modele_appli

Template réutilisable pour toutes les applis JGU. Respecte la charte graphique et les optimisations éco-responsables.

---

## 6. Console agents (interface web)

**Objet** : Gestion, orchestration et benchmark des agents IA
**Stack** : Vanilla JS (zéro dépendance), Python http.server
**Port** : 8000

### Vues disponibles

| Vue | Fonction |
|-----|----------|
| Pyramide | Visualisation hiérarchie agents, scores, création |
| Tests | Dashboard métriques, historique sessions, exécution |
| Config | Édition paramètres temps réel |
| Recherche | Filtres par agent/score, visionneuse session Markdown |

### Lancement

```bash
cd console-agents && python -m http.server 8000
# URL: http://localhost:8000
```

---

## 7. Configuration globale (config.json)

```json
{
  "chemins": {
    "agents": ".claude/commandes",
    "tests": "tests",
    "sessions": "sessions",
    "donnees": "donnees"
  },
  "ui": {
    "theme": { "bg": "#1a1a1a", "primary": "#2d5016", "text": "#b8b8b8", "accent": "#6b8e23" },
    "refresh_ms": 5000,
    "pixels_blancs_max_pct": 5
  },
  "tests": { "auto": true, "seuil_reussite": 80, "timeout_sec": 30, "iterations": 5 },
  "trace": { "active": true, "niveau": "complet", "retention_jours": 365 },
  "performance": { "limite_tokens": 200000, "optimisation_eco": true }
}
```

---

## 8. Charte graphique

### Couleurs (charte officielle JGU)

| Token | HEX | Usage |
|-------|-----|-------|
| `--bg-primary` | `#12100E` | Fond principal |
| `--bg-secondary` | `#1F1A15` | Fond secondaire |
| `--text-primary` | `#E8DCC8` | Texte principal |
| `--accent-gold` | `#C9A227` | Accent principal, CTA |
| `--accent-orange` | `E07B39` | Liens, accent secondaire |
| `--success` | `#5A9A5A` | Validation |
| `--error` | `#B54A4A` | Erreurs |

### Couleurs console/apps (éco-responsable)

| Usage | HEX |
|-------|-----|
| Background | `#1a1a1a` |
| Accent vert foncé | `#2d5016` |
| Accent vert clair | `#6b8e23` |
| Texte | `#b8b8b8` |

**Contrainte** : pixels blancs < 5%, thème sombre obligatoire

### Typographie

- **Principale** : Poppins (Google Fonts)
- **Secondaire** : Nunito
- **Code** : JetBrains Mono
- **Console/apps** : monospace système

---

## 9. Monnaie virtuelle — Geekos

Monnaie interne récompensant les bénévoles. Gérée via l'admin du site.

| Action | Geekos |
|--------|--------|
| Mission courte (< 2h) | 10–30 |
| Mission moyenne (2–5h) | 30–80 |
| Mission longue (> 5h) | 80–200 |
| Participation événement | 20 |
| Formation suivie | 50 |
| Formation animée | 100 |
| Parrainage actif | 50 |

**Règles** : non convertibles en argent, personnels, non transférables, pas d'expiration.

---

## 10. Tests

**Runner** : `tests/runner.py`
**Seuil réussite** : 80%
**Déclencheur** : fin de session (hook /close)

```bash
python tests/runner.py
```

**Types de tests** :
- Tests agents (définis dans agents.json)
- Test structure dossiers
- Test archivage sessions
- Test indexation recherche
- Test présence UI
- Test configuration valide

**Résultats** : sauvegardés dans `sessions/{date}/{id}.json`, indexés dans `donnees/sessions.json`

---

## 11. Principes de conception

1. **Simplicité** : architecture minimale, pas de sur-ingénierie
2. **Performance** : Vanilla JS, zéro dépendance externe
3. **Éco-responsabilité** : pixels blancs < 5%, thème sombre, optimisations
4. **Traçabilité** : tous échanges enregistrés et consultables
5. **Autonomie** : système complet, auto-suffisant
6. **Modularité** : agents indépendants, ajout facile

---

## 12. Instructions Claude Code (.claude/CLAUDE.md)

- Langue : **français exclusivement**
- Ton : professionnel, synthétique, direct
- Exécuter uniquement les tâches demandées explicitement
- Pas d'initiatives non sollicitées
- Pas d'emojis dans le code
- Code fonctionnel uniquement

---

## 13. État du projet (au 2026-02-25)

### Composants opérationnels
- Console agents IA : fonctionnelle (score tests 100%)
- Site internet Flask : opérationnel (inscription, auth, admin, événements, RGPD)
- Tracker usage IA : opérationnel
- Auto IA : opérationnel (v1.6.3)
- Système agents Claude Code : 5 agents configurés

### Fichiers de données actifs
- `donnees/agents.json` — 5 agents
- `donnees/sessions.json` — index sessions
- `site internet/instance/jegeekutile.db` — BDD SQLite site
- `applis/stat_usage_ia/donnees/ias.json` — liste IA configurées
- `applis/stat_usage_ia/donnees/clics.json` — historique clics

### Branches / Commits récents
- Ajout système gestion événements site internet
- Ajout conformité RGPD complète
- Ajout agent communication (/comia) et roadmap
- Ajout aperçu tableau de bord bénévole pour admin
