# SSD - Nouvelle UI JeGeekUtile

## 1. Introduction
**Projet** : JeGeekUtile - Nouvelle interface utilisateur (V3)  
**Objectif** : Créer un tableau de bord personnel et un panel d'administration modulaire pour l'association, avec applications installables, système de progression et gestion sécurisée.  
**Portée** : Refonte UI complète, architecture modulaire, scalable, avec charte graphique existante.  
**Public cible** : Utilisateurs finaux (bénévoles, membres) + Administrateurs association.

**Fichiers de référence** :
- Charte graphique : `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`
- Agencement UI de référence : `D:\ServOMorph\Bot ou pas Bot\UI\V3`

## 2. Résumé fonctionnel
**Dashboard personnel** : Interface personnalisée avec applications installables ("Présentation" par défaut, "Bénévoles"), progression/récompenses basée sur temps et contributions.  
**Panel admin** : Accès total, config dynamique via `config.py`, gestion données (sauf mots de passe), reset MDP par email.  
**Système global** : Applications HTML indépendantes, plugins modulaires, espace discussion WhatsApp-like, 85% tests.

## 3. Périmètre
### Inclus
- Dashboard utilisateur + admin
- Installation/suppression apps (catalogue)
- Système progression (temps usage, contributions)
- Config dynamique (`config.py`)
- Gestion données scalable via UI admin
- Reset MDP par email + validation
- Espace discussion
- Charte graphique + disposition V3
- **2 applications à développer** : "Présentation" (par défaut) et "Bénévoles"

### Exclus
- Nouvelles apps au-delà des 2 spécifiées
- Hébergement externe
- Paiements
- Apps mobiles natives

### Évolutions futures
- Système de plugins pour nouvelles apps
- IA pour recommandations progression

## 4. Architecture système
┌─────────────────┐ ┌──────────────────┐
│ Frontend UI │◄──►│ Backend API │
│ (HTML/Modulaire)│ │ (Python) │
└─────────┬───────┘ └──────┬───────────┘
│ │
▼ ▼
┌─────────┼──────┐ ┌───────┼──────────┐
│ Apps │ DB │ │ Config│ Services │
│(2 apps) │Scalable│ │.py │ (Email) │
└─────────┴──────┘ └───────┴──────────┘

text
- **Frontend** : Apps HTML en fenêtres séparées, indépendantes
- **Backend** : Gestion auth, config dynamique, données scalable
- **DB** : Modèles réutilisables, exportables
- **Services** : Email pour reset MDP

## 5. Composants détaillés

### 5.1 Dashboard utilisateur
- **Apps installées** : Grille/liste, bouton install depuis catalogue
- **Apps disponibles** : "Présentation" (installée par défaut), "Bénévoles" (installable)
- **Progression** : Barre compétences, badges (basé temps + contributions)
- **Espace discussion** : Chat-like, persistant

### 5.2 Panel admin
- **Apps totales** : Toutes apps + admin-only
- **Gestion données** : CRUD toutes données sauf MDP (via UI)
- **Config** : Éditeur `config.py` → sync immédiat UI
- **Sécurité** : Reset MDP → email lien → nouveau MDP

### 5.3 Système applications
app/
├── presentation/ # Installée par défaut
│ ├── index.html
│ └── metadata.json
└── benevoles/ # Modèle jeu vidéo
├── index.html
└── metadata.json

text
- Chaque app : HTML auto-suffisante + metadata JSON
- **App Présentation** : Informations sur le projet de l'association
- **App Bénévoles** : Gestion bénévoles avec modèle type jeu vidéo

## 6. Flux utilisateurs

### 6.1 Utilisateur standard
Login → Dashboard perso
↓
Catalogue apps → Install "Bénévoles"
↓
Apps installées → Ouverture fenêtre séparée
↓
Progression auto (temps + contribs)

text

### 6.2 Admin
Login admin → Dashboard admin
↓
Gestion apps/données/config
↓
Reset MDP utilisateur → Email lien

text

### 6.3 Reset MDP
"Mot de passe oublié" → Email saisi
↓
Email envoyé (lien temp) → Clic lien
↓
Nouveau MDP → Login

text
**Sécurité** : Lien à usage unique, expiration 1h, validation par email obligatoire

## 7. Interfaces et données

### 7.1 API principales
POST /auth/login {email, password}
POST /auth/reset_password {email}
POST /auth/confirm_reset {token, new_password}
GET /user/dashboard
POST /apps/install {app_id}
DELETE /apps/uninstall {app_id}
GET /user/progress
GET /apps/catalog
GET /admin/config
PUT /admin/config
PUT /admin/data/{model}/{id}

text

### 7.2 Modèles DB
User:
- id (int, PK)
- email (str, unique)
- password_hash (str)
- role (str: user|admin)
- progress_json (json)
- installed_apps (list[int])
- created_at (datetime)

App:
- id (int, PK)
- name (str)
- slug (str, unique)
- html_path (str)
- is_default (bool)
- admin_only (bool)

AppData:
- id (int, PK)
- user_id (int, FK)
- app_id (int, FK)
- data_json (json)

Config:
- key (str, PK)
- value (str)

Message:
- id (int, PK)
- chat_id (int)
- user_id (int, FK)
- content (str)
- timestamp (datetime)

PasswordReset:
- token (str, PK)
- user_id (int, FK)
- expires_at (datetime)
- used (bool)

text

## 8. Applications à développer

### 8.1 Application "Présentation"
- **Objectif** : Présenter le projet de l'association
- **Statut** : Installée par défaut pour tous les utilisateurs
- **Contenu** : Informations statiques/dynamiques sur l'association
- **Fichiers** :
  - `apps/presentation/index.html`
  - `apps/presentation/metadata.json`

### 8.2 Application "Bénévoles"
- **Objectif** : Gestion des bénévoles avec modèle type jeu vidéo
- **Statut** : Installable par les utilisateurs
- **Contenu** : Interface ludique pour gérer contributions, progression, rôles
- **Fichiers** :
  - `apps/benevoles/index.html`
  - `apps/benevoles/metadata.json`

### 8.3 Format metadata.json
```json
{
  "id": 1,
  "name": "Présentation",
  "slug": "presentation",
  "description": "Découvrez le projet JeGeekUtile",
  "version": "1.0.0",
  "is_default": true,
  "admin_only": false,
  "icon": "icon.png"
}
```

## 9. Stack technique
- **Frontend** : HTML/CSS/JS pur, charte graphique fournie
- **Backend** : Python (Flask ou Django)
- **DB** : SQLite (dev) / PostgreSQL (prod) scalable
- **Tests** : pytest, 85% coverage obligatoire
- **Déploiement** : Local/dev/prod, Docker-ready
- **Email** : SMTP pour reset MDP

## 10. Contraintes et règles
- **Graphique** : Respecter strictement `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`
- **Agencement** : Suivre la disposition de `D:\ServOMorph\Bot ou pas Bot\UI\V3`
- **Sécurité** : Reset MDP uniquement par email validation
- **Scalabilité** : DB + architecture prêts pour +100 users
- **Performance** : Apps légères, chargement <2s
- **Tests** : Backend/frontend critiques à 85%
- **Développement** : **En cas de doute → ne pas implémenter**

## 11. Structure dépôt
jegeekutile-ui-v3/
├── src/
│ ├── apps/
│ │ ├── presentation/
│ │ │ ├── index.html
│ │ │ └── metadata.json
│ │ └── benevoles/
│ │ ├── index.html
│ │ └── metadata.json
│ ├── static/
│ │ └── charte/ # Copie de Charte Graphique v3.html
│ └── templates/
│ ├── dashboard.html
│ └── admin.html
├── backend/
│ ├── config.py
│ ├── models.py
│ ├── api.py
│ └── services/
│ └── email.py
├── tests/
│ ├── test_auth.py
│ ├── test_apps.py
│ └── test_admin.py
├── docs/
│ └── SSD.md # Ce document
├── requirements.txt
└── README.md

text

## 12. Installation & Lancement
```bash
# Clone
git clone [URL_REPO]
cd jegeekutile-ui-v3

# Installation
pip install -r requirements.txt

# Configuration
cp config.py.example config.py
# Éditer config.py avec paramètres SMTP

# Migration DB
python manage.py migrate

# Lancement
python app.py
# Accès : http://localhost:5000

# Tests
pytest --cov=backend --cov-report=html
# Coverage requis : 85%
```

## 13. Configuration SMTP (config.py)
```python
# Email pour reset MDP
EMAIL_SMTP_HOST = "smtp.example.com"
EMAIL_SMTP_PORT = 587
EMAIL_SMTP_USER = "noreply@jegeekutile.fr"
EMAIL_SMTP_PASSWORD = "***"
EMAIL_FROM = "JeGeekUtile <noreply@jegeekutile.fr>"
RESET_TOKEN_EXPIRY = 3600  # 1 heure
```

## 14. Roadmap
- **Phase 1** : Core dashboard + auth + reset MDP par email
- **Phase 2** : App "Présentation" (défaut) + App "Bénévoles" installable
- **Phase 3** : Système progression + espace discussion
- **Phase 4** : Panel admin + config.py dynamique
- **Phase 5** : Tests 85% + déploiement

## 15. Sécurité - Processus reset MDP
1. Utilisateur clique "Mot de passe oublié"
2. Saisit son email
3. Backend génère token unique + expiration 1h
4. Email envoyé avec lien `https://app.com/reset?token={token}`
5. Utilisateur clique lien
6. Vérifie token (valide + non expiré + non utilisé)
7. Formulaire nouveau MDP
8. MDP mis à jour + token marqué utilisé
9. Email confirmation envoyé
10. Login avec nouveau MDP

**Important** : Pas de MDP temporaire, uniquement lien validation.

## 16. Espace discussion
- Interface type WhatsApp
- Messages persistants en DB
- Temps réel (WebSocket ou polling)
- Émojis supportés
- Historique scrollable

## 17. Système progression
- Temps d'utilisation par app tracké
- Contributions comptabilisées (actions, données ajoutées)
- Barre de progression visuelle
- Badges débloqués selon paliers
- Classement optionnel entre utilisateurs

## 18. Panel admin - Gestion données
- Interface CRUD pour tous les modèles
- Filtres et recherche
- Export CSV/JSON
- **Exclusion** : Champs `password_hash` non modifiables via UI
- Logs modifications (audit trail)

## 19. Config.py dynamique
- Interface éditeur dans panel admin
- Variables affichées en formulaire
- Validation côté backend
- Synchronisation immédiate avec UI
- Backup automatique avant modif

## 20. Notes pour l'IA dev
- **Priorité absolue** : Reset MDP par email avec validation obligatoire
- **Applications** : Développer uniquement "Présentation" et "Bénévoles"
- **Ne pas toucher** : Charte graphique, agencement V3
- **Scalabilité** : Conception pour 100+ users dès le début
- **Tests** : 85% coverage obligatoire avant merge
- **Doute** : Ne pas implémenter si incertain
- **Fenêtres apps** : Chaque app HTML s'ouvre dans fenêtre séparée indépendante
- **Config.py** : Sync temps réel UI ↔ fichier