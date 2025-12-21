# Console Gestion Agents IA

Système complet de gestion, orchestration et benchmark d'agents IA avec interface web éco-responsable.

## Vue d'ensemble

Ce projet implémente un système hiérarchique d'agents IA spécialisés coordonnés par un orchestrateur central (**Robert**). Chaque agent a des compétences spécifiques et peut être testé, benchmarké et tracé via une interface web minimaliste.

### Agents actuels

- **Robert** (niveau 0) : Orchestrateur principal
- **Halu** (niveau 1) : Détecteur d'hallucinations
- **PromptParfait** (niveau 2) : Optimiseur de prompts
- **AdminIA** (niveau 1) : Spécialiste démarches administratives

## Architecture

```
JeGeekUtile/
├── .claude/
│   ├── CLAUDE.md                    # Instructions conversation
│   └── commands/
│       ├── robert.md                 # Orchestrateur workflow
│       ├── halu.md                   # Détecteur hallucinations
│       ├── promptparfait.md          # Optimiseur prompts
│       ├── close.md                  # Hook fin de session
│       └── start.md                  # Hook démarrage
│
├── console-agents/                   # Interface web
│   ├── index.html                    # Page principale
│   ├── app.js                        # Application Vanilla JS
│   ├── eco.css                       # Styles éco-responsables
│   ├── config.json                   # Config UI
│   └── donnees/
│       ├── agents.json               # Base agents
│       └── sessions.json             # Index sessions
│
├── donnees/                          # Données racine
│   ├── agents.json                   # Configuration agents
│   └── sessions.json                 # Historique sessions
│
├── sessions/                         # Archives sessions
│   └── {date}/
│       └── {id}.json                 # Détails session
│
├── tests/
│   └── runner.py                     # Exécuteur tests
│
├── docs/
│   ├── tracking.md                   # Suivi projet
│   └── plaidoyer/                    # Documentation
│
├── plan_d_actions/
│   ├── plan-optimise.md              # Roadmap
│   └── spec-technique.json           # Specs
│
├── config.json                       # Configuration globale
├── trace_workflow.py                 # Traçage workflows
└── README.md                         # Ce fichier
```

## Installation

### Prérequis

- Python 3.8+
- Navigateur web moderne

### Démarrage rapide

```bash
# 1. Cloner ou télécharger le projet
cd JeGeekUtile

# 2. Lancer l'interface web
cd console-agents
python -m http.server 8000

# 3. Ouvrir dans le navigateur
# URL: http://localhost:8000
```

## Fonctionnalités

### 1. Interface Web (Console Agents)

#### Vue Pyramide
- Visualisation hiérarchique des agents
- Organisation par niveaux (0, 1, 2...)
- Affichage des scores individuels
- Création de nouveaux agents via formulaire

#### Vue Tests
- Dashboard métriques (dernier score, tests totaux)
- Historique complet des sessions
- Exécution tests en un clic
- Détails par agent (nombre de tests configurés)

#### Vue Config
- Édition paramètres interface (refresh, pixels blancs max)
- Paramètres tests (seuil réussite, timeout, itérations)
- Paramètres traçabilité (rétention, niveau détail)
- Sauvegarde temps réel

#### Vue Recherche
- Recherche dans l'historique
- Filtres par agent (robert, halu, promptparfait)
- Filtres par score (≥90%, ≥80%)
- **Clic sur session → Visionneuse Markdown formatée**

### 2. Système de Workflow (/robert)

L'orchestrateur Robert gère un workflow en 5 étapes :

```
1. Réception prompt utilisateur
2. Validation initiale (/halu)
3. Optimisation prompt (/promptparfait)
4. Validation finale (/halu)
5. Demande confirmation → Exécution
```

**Exemple d'utilisation :**

```bash
/robert crée une fonction python qui additionne deux nombres
```

**Résultat :**
1. Halu valide le prompt
2. PromptParfait l'optimise en "Créer fonction Python add(a, b) retournant a+b"
3. Halu revalide
4. Robert demande confirmation
5. Exécution si approuvé

### 3. Traçage des Conversations

Le système enregistre automatiquement tous les échanges entre agents.

**Utilisation :**

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
tracer.afficher_trace_complete()
tracer.sauvegarder()
```

**Consultation :**
- Console web → Recherche → Clic sur session → Voir trace Markdown

### 4. Système de Tests

**Exécution manuelle :**

```bash
python tests/runner.py
```

**Tests effectués :**
- Tests agents (définis dans `agents.json`)
- Tests système :
  - Structure dossiers
  - Archivage sessions
  - Indexation recherche
  - Présence UI
  - Configuration valide

**Résultat :**
- Score global (%)
- Détails par test (OK/ERR)
- Sauvegarde automatique dans `sessions/`

## Configuration

### config.json

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
    "timeout_sec": 30,
    "iterations": 5
  },
  "trace": {
    "active": true,
    "niveau": "complet",
    "retention_jours": 365
  }
}
```

## Format des Données

### agents.json

```json
{
  "agents": [
    {
      "id": "robert",
      "nom": "Robert",
      "role": "Orchestrateur",
      "niveau": 0,
      "parent": null,
      "competences": ["workflow", "validation", "orchestration"],
      "score": 0,
      "tests": [
        {
          "nom": "orchestration-simple",
          "input": "Optimise ce texte: Lorem ipsum...",
          "attendu": {
            "appel_promptparfait": true,
            "demande_confirmation": true
          }
        }
      ]
    }
  ]
}
```

### sessions.json

```json
{
  "sessions": [
    {
      "id": "20251126-2235",
      "date": "2025-11-26T22:35:54.172283",
      "score": 100.0,
      "reussis": 11,
      "total": 11,
      "agents": ["robert", "halu", "promptparfait"],
      "trace_complete": [
        {
          "timestamp": "...",
          "agent": "robert",
          "type": "reception_prompt",
          "contenu": "...",
          "resultat": "..."
        }
      ]
    }
  ],
  "index": {
    "dates": {"2025-11-26": ["20251126-2235"]},
    "agents": {"robert": ["20251126-2235"]},
    "scores": {"90-100": ["20251126-2235"]}
  },
  "stats": {
    "total_sessions": 1,
    "score_moyen": 100.0
  }
}
```

## Créer un Nouvel Agent

### Via Interface Web

1. Ouvrir console → Vue Pyramide
2. Cliquer "Créer nouvel agent"
3. Remplir : nom, rôle, compétences
4. Sauvegarder

### Via Workflow /robert

```bash
/robert crée un agent spécialisé dans [description], appelle le [NomAgent]
```

### Manuellement

**1. Créer fichier `.claude/commands/monagent.md` :**

```markdown
# /monagent - Mon Agent

## Rôle
Description du rôle

## Tâche
1. Tâche 1
2. Tâche 2

## Critères
- Critère 1
- Critère 2
```

**2. Ajouter dans `donnees/agents.json` :**

```json
{
  "id": "monagent",
  "nom": "MonAgent",
  "role": "Description courte",
  "niveau": 1,
  "parent": "robert",
  "competences": ["compétence1", "compétence2"],
  "score": 0,
  "tests": [
    {"nom": "test-1", "type": "validation"}
  ]
}
```

## Commandes Claude Code

### /robert
Orchestrateur principal. Gère le workflow complet :
- Validation initiale
- Optimisation
- Validation finale
- Demande confirmation
- Exécution

**Usage :** `/robert [votre demande]`

### /halu
Détecteur d'hallucinations. Analyse les prompts pour :
- Détecter contradictions
- Identifier extrapolations
- Valider faisabilité technique

**Usage :** `/halu [prompt à valider]`

### /promptparfait
Optimiseur de prompts. Réécriture pour :
- Concision maximale
- Clarté absolue
- Tokens minimums

**Usage :** `/promptparfait [prompt brut]`

## Optimisations Éco-responsables

### Interface
- Thème sombre (#1a1a1a)
- Pixels blancs < 5%
- Palette couleurs réduite (6 couleurs)
- Police monospace système

### Code
- Vanilla JS (zéro dépendance)
- CSS natif (pas de framework)
- Fetch API native
- Grid/Flexbox natifs

### Performance
- Fichiers minimaux (12 fichiers core)
- Latence réduite (-90%)
- Tests unifiés (1 runner)
- Cache actif

## Workflow Typique

### Scénario 1 : Optimiser un texte

```bash
/robert optimise ce texte : "Je voudrais que tu m'aides à améliorer..."
```

**Résultat :**
1. Halu valide → OK
2. PromptParfait optimise → "Optimiser texte : améliorer [aspects]"
3. Halu revalide → OK
4. Robert demande confirmation → Attente user

### Scénario 2 : Créer un agent

```bash
/robert crée un agent spécialisé dans la rédaction d'emails, appelle le EmailIA
```

**Résultat :**
1. Workflow validation/optimisation
2. Création fichier `.claude/commands/emailia.md`
3. Ajout dans `agents.json`
4. Agent disponible dans pyramide

### Scénario 3 : Exécuter tests

```bash
python tests/runner.py
```

**Résultat :**
- Exécution tous tests agents + système
- Affichage résultats console
- Sauvegarde session dans `sessions/{date}/{id}.json`
- Mise à jour index recherche

## Maintenance

### Consulter historique

**Interface web :**
- Vue Recherche
- Filtrer par agent/score
- Cliquer session pour trace complète

**Ligne de commande :**

```bash
# Lister sessions récentes
ls sessions/$(date +%Y-%m-%d)/

# Lire session
cat sessions/2025-11-26/20251126-2235.json
```

### Nettoyer anciennes sessions

```python
# Selon config.json → trace.retention_jours = 365
# Supprimer manuellement sessions/ ou créer script cleanup
```

### Exporter données

```bash
# Exporter tous agents
cat donnees/agents.json > backup_agents.json

# Exporter toutes sessions
cat donnees/sessions.json > backup_sessions.json
```

## Développement

### Ajouter une vue dans l'interface

**1. Ajouter bouton dans `index.html` :**

```html
<button data-view="mavue">Ma Vue</button>
```

**2. Ajouter fonction render dans `app.js` :**

```javascript
renderMaVue() {
  return `<div class="ma-vue">Contenu</div>`;
}
```

**3. Enregistrer dans le router :**

```javascript
render(view) {
  const views = {
    pyramide: this.renderPyramide,
    mavue: this.renderMaVue  // Ajouter ici
  };
}
```

### Ajouter un test système

**Dans `tests/runner.py` :**

```python
def test_mon_test(self):
    """Description du test"""
    try:
        # Logique test
        ok = True
        return {'type': 'systeme', 'test': 'mon_test', 'statut': 'ok' if ok else 'erreur'}
    except Exception as e:
        return {'type': 'systeme', 'test': 'mon_test', 'statut': 'erreur', 'erreur': str(e)}
```

**Enregistrer dans `run_all()` :**

```python
tests_systeme = [
    self.test_structure(),
    self.test_mon_test()  # Ajouter ici
]
```

## Dépannage

### L'interface ne charge pas

```bash
# Vérifier le serveur
cd console-agents
python -m http.server 8000

# Vérifier fichiers présents
ls index.html app.js eco.css
```

### Tests échouent

```bash
# Vérifier structure
ls -R

# Vérifier config
cat config.json

# Exécuter avec debug
python -u tests/runner.py
```

### Agent ne s'affiche pas

**Vérifier `donnees/agents.json` :**
- Agent bien présent
- Syntaxe JSON valide
- Champs obligatoires : id, nom, role, niveau, parent, competences, score, tests

**Recharger interface :**
- F5 dans le navigateur
- Vider cache si nécessaire

## Statistiques Projet

- **Fichiers core :** 12
- **Lignes code JS :** ~550
- **Lignes code Python :** ~220
- **Lignes CSS :** ~650
- **Agents configurés :** 4
- **Score tests actuel :** 100% (4/4 sessions)
- **Optimisation tokens plan :** -77%
- **Réduction latence :** -90%

## Principes de Conception

1. **Simplicité** : Architecture minimale, pas de sur-ingénierie
2. **Performance** : Vanilla JS, pas de dépendances externes
3. **Éco-responsabilité** : Pixels blancs <5%, thème sombre, optimisations
4. **Traçabilité** : Tous échanges enregistrés et consultables
5. **Autonomie** : Système complet, auto-suffisant
6. **Modularité** : Agents indépendants, ajout facile

## Ressources

- **Documentation Claude Code :** `.claude/CLAUDE.md`
- **Plan projet :** `plan_d_actions/plan-optimise.md`
- **Specs techniques :** `plan_d_actions/spec-technique.json`
- **Suivi développement :** `docs/tracking.md`
- **Guide lancement :** `LANCEMENT.md`

## Licence

Projet interne - Tous droits réservés

## Contact / Support

Pour questions ou suggestions, consulter la documentation dans `docs/`

---

**Version :** 1.0
**Dernière mise à jour :** 26/11/2025
**Statut :** Production ready ✓
