# Tracker Usage IA

Application web pour monitorer et optimiser l'utilisation des IA locales vs cloud.

## Objectif

Réduire la dépendance aux IA cloud en favorisant l'usage des IA locales.
**Cible : 70% d'utilisation IA locales**

## Fonctionnalités

### 1. Dashboard
- Boutons cliquables par IA
- Compteur temps réel des clics
- Couleur verte (local) / orange (cloud)
- Badge nombre de clics par IA

### 2. Gestion IA
- Formulaire ajout IA (nom + type)
- Liste des IA configurées
- Suppression IA (avec clics associés)

### 3. Statistiques
- Total clics global
- Ratio local/cloud (%)
- Barre de progression objectif 70%
- Tableau détaillé par IA

### 4. Persistance
- Fichier `clics.json` avec horodatage
- Sauvegarde automatique à chaque clic
- Données persistantes entre sessions

## Installation

### Prérequis
- Python 3.8+
- pip

### Installation dépendances

```bash
pip install -r requirements.txt
```

## Lancement

```bash
# Démarrer le serveur
python server.py

# Ouvrir dans le navigateur
# URL: http://localhost:5000
```

## Utilisation

### 1. Ajouter vos IA

1. Cliquer sur onglet "Gestion IA"
2. Remplir formulaire :
   - Nom : Claude, GPT-4, LLaMA, etc.
   - Type : Local ou Cloud
3. Cliquer "Ajouter"

### 2. Tracker vos usages

1. Onglet "Dashboard"
2. Cliquer sur bouton IA à chaque prompt envoyé
3. Compteur s'incrémente automatiquement

### 3. Consulter statistiques

1. Onglet "Statistiques"
2. Voir ratio local/cloud
3. Vérifier objectif 70%
4. Consulter détails par IA

## Structure

```
stat_usage_ia/
├── index.html           # Page principale
├── app.js               # Frontend JavaScript
├── style.css            # Styles mode sombre
├── server.py            # Backend Flask
├── requirements.txt     # Dépendances Python
├── donnees/
│   ├── ias.json        # Liste IA configurées
│   └── clics.json      # Historique clics
└── README.md
```

## Données

### ias.json
```json
{
  "ias": [
    {
      "id": "claude",
      "nom": "Claude",
      "type": "cloud"
    },
    {
      "id": "llama",
      "nom": "LLaMA",
      "type": "local"
    }
  ]
}
```

### clics.json
```json
{
  "clics": [
    {
      "ia_id": "claude",
      "timestamp": "2025-11-26T23:45:12.345678",
      "type": "cloud"
    },
    {
      "ia_id": "llama",
      "timestamp": "2025-11-26T23:46:08.123456",
      "type": "local"
    }
  ]
}
```

## API Endpoints

### GET /api/stats
Retourne statistiques globales

### POST /api/ia
Ajoute une nouvelle IA
```json
{
  "nom": "Claude",
  "type": "cloud"
}
```

### DELETE /api/ia/:id
Supprime une IA et ses clics

### POST /api/clic
Enregistre un clic
```json
{
  "ia_id": "claude"
}
```

## Design Mode Sombre

### Palette couleurs
- Background : `#1a1a1a`
- Primary : `#2d5016`
- Secondary : `#4a4a4a`
- Text : `#b8b8b8`
- Accent : `#6b8e23`
- Cloud : `#ff8c00`

### Principes
- Pixels blancs < 5%
- Contraste optimal
- Cohérence avec console-agents
- Éco-responsable

## Conseils d'usage

1. **Enregistrer systématiquement** : Cliquer à chaque prompt envoyé
2. **Favoriser local** : Privilégier IA locales quand possible
3. **Consulter stats** : Vérifier ratio hebdomadairement
4. **Objectif 70%** : Viser minimum 70% local

## Dépannage

### Serveur ne démarre pas

```bash
# Vérifier Python installé
python --version

# Installer dépendances
pip install -r requirements.txt

# Relancer
python server.py
```

### Interface ne charge pas

- Vérifier serveur démarré
- URL correcte : http://localhost:5000
- Vider cache navigateur (Ctrl+F5)

### Clics non enregistrés

- Vérifier fichier `donnees/clics.json` existe
- Permissions écriture dossier `donnees/`
- Consulter console navigateur (F12)

## Évolutions futures

- Export CSV statistiques
- Graphiques temporels (clics par jour)
- Notifications objectif atteint
- Comparaison périodes (semaine/mois)

---

**Version :** 1.0
**Mode :** Sombre (éco-responsable)
**Objectif :** 70% IA locales
