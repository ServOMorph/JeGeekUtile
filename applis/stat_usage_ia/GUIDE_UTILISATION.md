# Guide Utilisation - Tracker Usage IA

## Démarrage

### 1. Installer dépendances (une seule fois)

```bash
cd applis/stat_usage_ia
pip install -r requirements.txt
```

### 2. Lancer le serveur

```bash
python server.py
```

Le serveur démarre sur http://localhost:5000

### 3. Ouvrir l'application

Ouvrir votre navigateur : http://localhost:5000

## Utilisation

### IAs Pré-configurées

L'application est livrée avec 7 IAs déjà configurées :

**Cloud (5)** :
- ChatGPT
- Claude
- Comet
- Grok
- Gemini

**Locale (2)** :
- VertIA
- Whisper

### Tracker vos usages

1. **Dashboard** → Cliquer sur le bouton de l'IA à chaque prompt envoyé
2. Le compteur s'incrémente automatiquement
3. Les statistiques se mettent à jour en temps réel

### Ajouter une nouvelle IA

Si vous utilisez une IA qui n'est pas dans la liste :

1. Onglet **Gestion IA**
2. Remplir le formulaire :
   - **Nom** : Nom de l'IA (ex: "Mistral", "Ollama")
   - **Type** : Local ou Cloud
3. Cliquer **Ajouter**

**Note** : Si vous voyez l'erreur "IA déjà existante", c'est que cette IA est déjà configurée. Vérifiez la liste dans l'onglet Gestion IA.

### Supprimer une IA

1. Onglet **Gestion IA**
2. Cliquer **Supprimer** sur l'IA souhaitée
3. Confirmer (⚠️ supprime aussi tous les clics associés)

### Consulter statistiques

Onglet **Statistiques** :
- Total clics global
- Nombre clics Local vs Cloud
- Ratio local/cloud (%)
- Barre progression objectif 70%
- Tableau détaillé par IA

## Objectif

**Favoriser l'usage IA locales : minimum 70%**

### Pourquoi ?

- ✓ **Confidentialité** : Données restent sur votre machine
- ✓ **Coût** : Pas d'abonnements cloud
- ✓ **Performance** : Pas de latence réseau
- ✓ **Autonomie** : Pas de dépendance services tiers

### Comment atteindre 70% ?

1. Identifier tâches adaptées IA locales (rédaction, analyse, code)
2. Utiliser IA cloud uniquement quand nécessaire (tâches complexes)
3. Tracker tous vos usages dans l'application
4. Consulter stats chaque semaine
5. Ajuster vos habitudes

## Données

### Localisation

Les données sont stockées dans `applis/stat_usage_ia/donnees/` :

- **ias.json** : Liste des IAs configurées
- **clics.json** : Historique complet avec horodatage

### Format clics.json

```json
{
  "clics": [
    {
      "ia_id": "claude",
      "timestamp": "2025-11-26T23:45:12.345678",
      "type": "cloud"
    }
  ]
}
```

### Sauvegarde

Les données sont sauvegardées automatiquement à chaque clic.

**Backup manuel** :

```bash
cp donnees/clics.json donnees/clics_backup_$(date +%Y%m%d).json
```

## Dépannage

### "Erreur: IA déjà existante"

➜ Cette IA est déjà dans la liste. Allez dans **Gestion IA** pour voir toutes les IAs configurées.

### "Erreur initialisation"

➜ Vérifier que le serveur Python est démarré :

```bash
python server.py
```

### Compteurs ne s'incrémentent pas

➜ Vérifier la console navigateur (F12) pour erreurs JavaScript

➜ Vérifier que le serveur répond :

```bash
curl http://localhost:5000/api/stats
```

### Serveur ne démarre pas

➜ Vérifier dépendances :

```bash
pip install -r requirements.txt
```

➜ Vérifier port 5000 libre :

```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

## Astuces

### Raccourcis clavier

Créez des raccourcis pour cliquer rapidement sur vos IAs favorites.

### Routine quotidienne

1. Matin : Consulter stats de la veille
2. Pendant travail : Cliquer à chaque prompt
3. Soir : Vérifier ratio local/cloud

### Workflow optimal

```
Tâche simple (résumé, rédaction) → IA locale
Tâche moyenne (analyse) → IA locale si possible
Tâche complexe (recherche approfondie) → IA cloud si nécessaire
```

## Statistiques utiles

### Ratio actuel

Header en haut à droite affiche :
- Total clics
- % IA locales
- Objectif 70%

### Évolution

Consultez régulièrement l'onglet Statistiques pour :
- Identifier IAs les plus utilisées
- Vérifier répartition local/cloud
- Ajuster vos habitudes

## Contact

Questions ou bugs : Voir documentation projet principal

---

**Application** : Tracker Usage IA v1.0
**Auteur** : @Je Geek Utile
**Date** : 26/11/2025
