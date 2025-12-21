# Démarrage Rapide - Tracker Usage IA

## Méthode Simple (Windows)

1. Aller dans le dossier `applis/stat_usage_ia`
2. Double-cliquer sur **start.bat**
3. Ouvrir navigateur : http://localhost:5000

**Le script fait tout automatiquement** :
- Installe les dépendances si nécessaire
- Démarre le serveur
- Affiche l'URL

## Méthode Manuelle

### Windows

```bash
cd applis\stat_usage_ia
python server.py
```

### Linux/Mac

```bash
cd applis/stat_usage_ia
python server.py
```

Puis ouvrir : http://localhost:5000

## Vérification

Si vous voyez **"Aucune IA configurée"**, vérifiez :

### 1. Le serveur démarre depuis le bon dossier

✓ **CORRECT** :
```bash
cd applis/stat_usage_ia
python server.py
```

✗ **INCORRECT** :
```bash
# Depuis la racine du projet
python applis/stat_usage_ia/server.py  # Ne fonctionnera pas !
```

### 2. Console navigateur (F12)

Regardez les erreurs JavaScript :
- Si vous voyez `404` pour `donnees/ias.json` → Serveur mal démarré
- Si vous voyez `CORS error` → Problème CORS (ne devrait pas arriver)
- Vous devriez voir : `"IAs chargées: 7"`

### 3. Fichier ias.json existe

Vérifier que le fichier existe :
```bash
dir applis\stat_usage_ia\donnees\ias.json        # Windows
ls applis/stat_usage_ia/donnees/ias.json         # Linux/Mac
```

## Les 7 IAs Pré-configurées

Au premier démarrage, vous devriez voir :

**Cloud (5)** :
- ChatGPT
- Claude
- Comet
- Grok
- Gemini

**Local (2)** :
- VertIA
- Whisper

## Dépannage

### Problème : "Aucune IA configurée"

**Cause** : Serveur lancé depuis mauvais dossier OU fichier ias.json non trouvé

**Solution** :
1. Fermer le serveur (Ctrl+C)
2. Se placer dans le bon dossier : `cd applis/stat_usage_ia`
3. Relancer : `python server.py` OU double-clic sur `start.bat`
4. Rafraîchir le navigateur (F5)

### Problème : "Module 'flask' not found"

**Solution** :
```bash
pip install -r requirements.txt
```

### Problème : Port 5000 déjà utilisé

**Solution** :
```bash
# Trouver le processus
netstat -ano | findstr :5000     # Windows
lsof -i :5000                    # Linux/Mac

# Tuer le processus OU changer le port dans server.py (ligne finale)
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Problème : Console montre "IAs chargées: 0"

**Solution** :
1. Vérifier que `donnees/ias.json` contient bien les 7 IAs
2. Vérifier les permissions du fichier (lecture autorisée)
3. Regarder la console serveur pour erreurs Python

## Test Complet

Pour vérifier que tout fonctionne :

1. **Démarrer** : `start.bat` (Windows) OU `python server.py`
2. **Ouvrir** : http://localhost:5000
3. **Dashboard** : Doit afficher 7 boutons IA
4. **Cliquer** : Sur un bouton → Compteur s'incrémente
5. **Stats** : Total clics = 1, Ratio local selon IA cliquée

Si tout fonctionne → ✓ Installation OK !

## Arrêter le Serveur

Dans le terminal où le serveur tourne : **Ctrl+C**

---

**En cas de problème persistant**, vérifier :
- [ ] Bon dossier de démarrage
- [ ] Fichier `donnees/ias.json` existe
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Port 5000 libre
- [ ] Console navigateur (F12) pour erreurs JS
