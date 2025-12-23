# auto_ia - Automatisation Souris et Presse-papiers

Application d'automatisation de clics souris et copier-coller via API HTTP.

## Fonctionnalités

### Souris
- Déplacement curseur
- Clic gauche/droit/milieu
- Double-clic
- Scroll

### Clavier et Presse-papiers
- Copier texte
- Coller texte
- Écrire texte
- Raccourcis clavier

## Installation

```bash
cd applis/auto_ia
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

Serveur démarré : `http://127.0.0.1:8000`

**Mode développement** : Le serveur redémarre automatiquement à chaque modification de fichier Python (debug mode activé).

## API

### GET /status
État serveur

**Réponse**
```json
{
  "status": "idle",
  "message": "Serveur actif"
}
```

### POST /action
Exécuter action

**Body**
```json
{
  "type": "mouse_click",
  "params": {
    "x": 100,
    "y": 100,
    "button": "left"
  }
}
```

**Réponse**
```json
{
  "status": "ok",
  "message": "Clic left à (100, 100)"
}
```

## Types d'actions

### mouse_click
```json
{
  "type": "mouse_click",
  "params": {"x": 100, "y": 200, "button": "left"}
}
```

### mouse_move
```json
{
  "type": "mouse_move",
  "params": {"x": 500, "y": 300, "duration": 0.5}
}
```

### mouse_scroll
```json
{
  "type": "mouse_scroll",
  "params": {"amount": 10}
}
```

### clipboard_copy
```json
{
  "type": "clipboard_copy",
  "params": {"text": "Texte à copier"}
}
```

### clipboard_paste
```json
{
  "type": "clipboard_paste",
  "params": {}
}
```

### keyboard_write
```json
{
  "type": "keyboard_write",
  "params": {"text": "Hello World"}
}
```

### keyboard_press
```json
{
  "type": "keyboard_press",
  "params": {"keys": ["ctrl", "c"]}
}
```

## Interface web auto_ia

### Architecture
- Backend Flask exposant API HTTP
- Frontend HTML/CSS/JS vanilla (mode sombre éco-responsable)

### URL par défaut
- Backend : `http://127.0.0.1:8000`
- Interface : Ouvrir `web/index.html` dans navigateur

### Panneaux interface
1. **Contrôle** : Indicateur santé serveur (`/health`), boutons Pause/Stop, configuration URL API
2. **File d'actions** : Visualisation actions en attente (simulation locale JS v1)
3. **Historique** : Actions exécutées avec résultats en temps réel
4. **Test rapide** : Formulaire pour envoyer actions manuellement (type + params JSON)

### Charte graphique
Mode sombre éco-responsable Je Geek Utile :
- Gris très foncés (#101215, #181b20) pour réduire fatigue visuelle
- Texte cassé (#e5e7eb) pour meilleur confort
- Accents verts (#4caf50) pour interactivité
- Contraste optimisé, bordures fines, lisibilité maximale

## File d'actions et worker

### Modèle d'action
Chaque action possède :
- `id` : Identifiant unique (UUID)
- `type` : Type d'action (mouse_click, clipboard_copy, etc.)
- `params` : Paramètres JSON spécifiques
- `status` : État (pending, running, done, error)
- `created_at` : Timestamp création
- `started_at` : Timestamp démarrage (optionnel)
- `finished_at` : Timestamp fin (optionnel)
- `error` : Message erreur (optionnel)

### Deux modes d'exécution

**1. Exécution directe** (`POST /action`)
- Action exécutée immédiatement
- Réponse synchrone avec résultat
- Usage : tests rapides, actions isolées

**2. Enfilement** (`POST /queue/actions`)
- Action ajoutée à la file FIFO
- Worker traite séquentiellement
- Usage : automatisation, séquences d'actions

### Contrôle du worker

**Commandes** via `POST /queue/control` :
- `start` : Démarrer le worker (thread daemon)
- `pause` : Mettre en pause sans vider la file
- `resume` : Reprendre après pause
- `stop` : Arrêter complètement le worker

**États** :
- `stopped` : Worker arrêté
- `paused` : En pause, file préservée
- `running` : Actif, traite les actions

### Guide rapide

1. Démarrer serveur : `python main.py`
2. Ouvrir interface : `web/index.html`
3. Cliquer "Start" pour démarrer worker
4. Mode "Enfiler" : Ajouter actions dans la file
5. Observer file + historique en temps réel (polling 3s)

### Implémentation v1
- File in-memory (non persistée)
- Thread-safe avec verrous simples
- Délai 0.2s entre actions
- Polling 0.5s pour nouvelles actions
- Conçu pour évoluer vers système avancé si besoin

## Test

```bash
python test_api.py
```

## Structure

```
auto_ia/
├── core/
│   ├── mouse_controller.py
│   ├── keyboard_clipboard.py
│   └── actions.py
├── api/
│   └── http_server.py
├── web/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── main.py
├── test_api.py
├── requirements.txt
└── README.md
```

## Sécurité

**FAILSAFE activé** : Déplacer souris en coin supérieur gauche pour arrêt d'urgence.

## UX avancée et préparation multi-IA

### Métadonnées d'action
Champs ajoutés au modèle `Action` :
- `source` : Origine de l'action (web, comet, cli, preset, etc.)
- `priority` : Niveau de priorité (0=normal, >0=prioritaire)
- `label` : Nom humain lisible (ex: preset_copy_zone, scenario_automation_x)

**Usage** :
- Tracer l'origine des actions dans un contexte multi-agent
- Préparer future politique de scheduling avancée
- Faciliter debug et monitoring orchestrateur

**Note** : En v1.3, `priority` est informatif uniquement, la file reste FIFO.

### Codes couleur statuts (UI)
Interface affiche badges colorés mode sombre :
- **pending** : Gris/bleu doux - Action en attente
- **running** : Vert foncé/accent - En cours d'exécution
- **done** : Vert doux - Terminée avec succès
- **error** : Rouge doux - Erreur lors de l'exécution

Métadonnées affichées : ID court, source, priority, timestamps création/maj.

### Presets de scénarios
Section dédiée dans l'interface avec 3 presets prédéfinis :
1. **Copier zone texte** : clipboard_copy automatique
2. **Double-clic standard** : mouse_click coordonnées prédéfinies
3. **Coller séquence** : clipboard_paste

**Avantages** :
- Utilisation simplifiée pour agents IA (Comet)
- Réduction prompt engineering côté appelant
- Enfilement automatique en mode queue avec label tracé

## API Endpoints

### Endpoints existants
- `POST /action` : Exécution directe
- `GET /status` : État serveur
- `GET /health` : Health check

### Endpoints file d'actions
- `POST /queue/actions` : Ajouter action (accepte source, priority, label facultatifs)
- `GET /queue/actions` : Lister actions (optionnel ?status=pending)
- `POST /queue/control` : Contrôler worker (start/stop/pause/resume)
- `GET /queue/status` : État worker + compte actions

## Sécurité, garde-fous et logs

### Logger structuré
Événements enregistrés (format compact, token-efficient) :
- **ACTION_ADDED** : id, type, source, priority, label
- **STATUS_CHANGE** : id, transition statut, type
- **WORKER_STARTED/STOPPED/PAUSED/RESUMED** : Commandes worker
- **RATE_LIMITED** : Warnings dépassement limites
- **Erreurs** : Niveau ERROR avec détails

Format : `YYYY-MM-DD HH:MM:SS [LEVEL] EVENT`

### Garde-fous d'exécution

**Délai minimal entre actions** : 0.15s par défaut (configurable)
- Évite comportements instables UI
- Respecte bonnes pratiques automatisation 2025

**Limite max_actions_per_minute** : 200 par défaut
- Compteur glissant 60s
- Statut `rate_limited` si dépassement
- Pause 1s avant retry

**Statut spéciaux** :
- `rate_limited` : Action refusée, dépassement limite
- Affiché avec badge jaune/orange dans UI

**Intérêt multi-IA** :
- Prévient spam agents mal configurés
- Trace visible dans logs + UI
- Protection environnement production

### Safe mode

**Variable environnement** : `AUTO_IA_SAFE_MODE=true|false`
- Défaut : `true` (activé)
- Permet restrictions futures (zones écran, types actions)

**Endpoint** : `GET /config/status`
```json
{
  "status": "ok",
  "safe_mode": true,
  "min_delay_seconds": 0.15,
  "max_actions_per_minute": 200
}
```

**UI** : Panneau "Sécurité" affiche :
- Safe Mode : ON (vert) / OFF (orange)
- Délai minimal
- Max actions/minute

### Recommandations

1. **Environnement test** : Toujours tester scénarios sur système non-production
2. **Garde-fous actifs** : Vérifier safe_mode=true avant automatisation longue
3. **Logs monitoring** : Surveiller RATE_LIMITED, STATUS_CHANGE→error
4. **Progressive** : Commencer petit (quelques actions), augmenter graduellement

## Zones nommées

### Abstraction de coordonnées
Système de zones nommées pour remplacer coordonnées brutes :
- `Zone` : nom, x, y, largeur (opt), hauteur (opt)
- Thread-safe avec verrous
- Calcul automatique centre si dimensions fournies

### API Zones
- `POST /zones` : Créer/modifier zone
  ```json
  {
    "name": "comet_prompt",
    "x": 100,
    "y": 200,
    "width": 300,
    "height": 50
  }
  ```
- `GET /zones` : Lister toutes les zones
- `DELETE /zones/{name}` : Supprimer zone

### Action click_zone
```json
{
  "type": "click_zone",
  "params": {
    "zone": "comet_prompt",
    "button": "left"
  }
}
```

**Avantages** :
- Configuration portable entre environnements
- Noms sémantiques (claude_send, zone_validation)
- Adaptation dynamique sans modifier scripts

### UI Zones
Panneau dédié interface web :
- Liste zones définies avec coordonnées
- Formulaire ajout/édition
- Bouton suppression par zone
- Intégration selector action (click_zone disponible)

## Mode Tutoriel Gamifié

### Concept
Overlay interactif guidant utilisateur pas-à-pas dans configuration multi-IA.
Détection automatique progression via zones cliquées.

### Architecture
- **Modèle Tutorial** : id, titre, description, étapes, progression
- **Modèle TutorialStep** : id, zone cible, message, hint, action requise, statut
- **TutorialManager** : Gestion état, détection actions, tracking progression

### Endpoints API
- `POST /tutorial/start` : Démarrer tutoriel chargé
- `POST /tutorial/stop` : Arrêter tutoriel actif
- `GET /tutorial/status` : État + progression courante

### UI Overlay
**Style cartoon joyeux** :
- Dégradé fond semi-transparent + bordure accent verte 3px
- Animation slideIn depuis la droite + backdrop-filter blur
- Barre progression animée
- Message étape + hints optionnels (jaune, style italique)
- Bouton fermer avec rotation 90° au hover
- Positionné en bas à droite, non-bloquant (pointer-events)

**Affichage dynamique** :
- Caché si aucun tutoriel
- Écran démarrage (bouton "Démarrer")
- Écran étape active (message + hint + progression + bouton pré-remplissage)
- Écran terminé (félicitations)
- Polling 1s pour mise à jour temps réel

**Fonctionnalités UX** :
- Overlay non-bloquant : L'utilisateur peut interagir avec l'interface pendant le tutoriel
- Bouton "⚡ Pré-remplir le formulaire" : Remplit automatiquement le formulaire d'action avec les paramètres corrects pour l'étape en cours
- Scroll automatique vers le formulaire lors du pré-remplissage

### Tutoriel preset "Automatiser Claude"
Chargé automatiquement au démarrage serveur. Conçu pour débutants avec instructions pas-à-pas.

**Écran d'accueil** :
- Titre : "🎓 Tutoriel : Automatiser Claude"
- Description accueillante expliquant le concept de zones et clics automatiques
- Emojis et formatage pour rendre l'interface plus accessible

**Étape 1** : Cliquer zone `comet_prompt`
- Instructions numérotées : 1️⃣ Cliquer sur "⚡ Pré-remplir" → 2️⃣ Le formulaire se remplit → 3️⃣ Cliquer sur "Exécuter"
- Hint : Rappel de créer la zone dans le panneau Zones avant de commencer
- Langage simplifié pour débutants

**Étape 2** : Cliquer zone `claude_input`
- Message de félicitation pour encourager l'utilisateur
- Instructions identiques avec rappel du workflow
- Hint : Explication concrète de ce que représente la zone

**Étape 3** : Cliquer zone `claude_send`
- Indication "Dernière ligne droite" pour motiver
- Instructions cohérentes avec les étapes précédentes
- Message de succès avec emoji 🎉 à la fin
- Hint : Mise en perspective de l'utilité (automatiser une conversation complète)

**Fonctionnement** :
1. Créer zones via API ou UI : comet_prompt, claude_input, claude_send
2. Overlay s'affiche automatiquement au chargement interface (bas à droite, non-bloquant)
3. Utilisateur clique "Démarrer le tutoriel"
4. Pour chaque étape :
   - Lire le message et le hint affichés
   - Cliquer sur "⚡ Pré-remplir le formulaire" pour auto-complétion
   - Ou remplir manuellement : type=click_zone, params={"zone": "nom_zone", "button": "left"}
   - Exécuter l'action (mode direct ou queue)
5. Détection automatique dans `execute_action` (hook click_zone)
6. Logging détaillé : TUTORIAL_STEP_CHECKED, TUTORIAL_STEP_COMPLETED, TUTORIAL_STEP_MISMATCH
7. Progression affichée visuellement (barre + compteur)

**Avantages** :
- Onboarding utilisateur gamifié accessible aux débutants
- Messages clairs avec instructions numérotées étape par étape
- Encouragements et feedback positif pour maintenir la motivation
- UX non-intrusive avec overlay positionné en bas à droite
- Pré-remplissage automatique du formulaire pour faciliter l'utilisation
- Emojis et formatage pour rendre l'interface plus engageante
- Logging détaillé pour debug et monitoring

## Version

v1.6.3 - Auto-reload activé en mode développement (serveur redémarre automatiquement)
