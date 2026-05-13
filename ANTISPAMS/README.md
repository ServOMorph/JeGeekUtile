# AntiSpams — Analyse RGPD Emails

Module d'analyse locale d'emails pour détecter les violations RGPD et générer des plaidoyers documentés.

## Stack

- **Backend** : Python / Flask (port 8020)
- **Frontend** : Vanilla JS, CSS sombre (charte JGU)
- **Dépendances** : stdlib Python (`imaplib`, `email`, `re`) + Flask
- **Zéro dépendance externe** côté analyse

## Démarrage rapide

### 1. Configurer IMAP

```bash
cp ANTISPAMS/donnees/config.example.json ANTISPAMS/donnees/config.json
```

Éditez `donnees/config.json` :

```json
{
  "imap": {
    "host": "imap.free.fr",
    "port": 993,
    "ssl": true,
    "user": "votre_adresse@free.fr",
    "password": "votre_mot_de_passe"
  }
}
```

> **IMPORTANT** : `config.json` est exclu par `.gitignore`. Ne le commitez jamais.

### 2. Installer les dépendances

```bash
pip install -r ANTISPAMS/requirements.txt
```

### 3. Lancer le serveur

```bash
python ANTISPAMS/main.py
```

Ouvrir : [http://localhost:8020](http://localhost:8020)

## Fonctionnalités

### Scoring RGPD (0-100)

| Critère | Points |
|---------|--------|
| Pixel de tracking (image 1×1) | +20 |
| Pas de lien de désabonnement | +25 |
| Header `List-Unsubscribe` absent | +15 |
| Liens de tracking (domaines connus) | +20 |
| From / Reply-To divergents | +10 |
| Pas de mention RGPD (email en masse) | +10 |

**Niveaux** : `≥60` haut risque | `30-59` modéré | `<30` conforme

### Vues

- **Liste** : Tableau de tous les emails avec score badge
- **Analyse** : Détail des critères + actions [Rapport] [Anonymiser]
- **Rapports** : Historique des plaidoyers exportés
- **Config** : Statut connexion IMAP + guide

### Workflow plaidoyer

1. Vue Liste → Analyser un email
2. Vue Analyse → Vérifier les critères déclenchés
3. Cocher **validation humaine** (obligatoire)
4. Cliquer **Générer Rapport** → export MD + JSON dans `donnees/rapports/`

### Anonymisation

Cliquez **Anonymiser** pour masquer :
- Adresses email (format `j***@e***.fr`)
- Numéros de téléphone (`[TÉLÉPHONE ANONYMISÉ]`)
- Message-ID

## Structure

```
ANTISPAMS/
├── index.html          # Dashboard UI
├── app.js              # Logique frontend
├── style.css           # Thème sombre JGU
├── main.py             # Serveur Flask
├── core/
│   ├── imap_reader.py  # Connexion IMAP (lecture seule)
│   ├── scorer.py       # Scoring heuristique 0-100
│   ├── analyzer.py     # Analyse complète email
│   ├── plaidoyer.py    # Génération MD + JSON
│   └── anonymizer.py   # Anonymisation données
├── donnees/
│   ├── config.example.json
│   └── rapports/       # Plaidoyers générés (gitignored)
└── tests/              # Tests pytest (>80% coverage)
```

## Tests

```bash
cd ANTISPAMS
pytest tests/ -v --cov=core --cov-report=term-missing
```

Seuil requis : **80% coverage**

## Sécurité

- IMAP lecture seule uniquement (`readonly=True`)
- Aucun secret dans le code ou le dépôt
- Pas d'envoi automatique d'emails
- Validation humaine obligatoire avant export

---

**Version** : 1.0  
**Port** : 8020  
**Auteur** : @Je Geek Utile
