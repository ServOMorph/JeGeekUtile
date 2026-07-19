# JeGeekUtile V3 — UI Dashboard

Application web modulaire pour l'association JeGeekUtile. Tableau de bord personnel avec applications installables, système de progression et authentification sécurisée.

## Installation

### Prérequis
- Python 3.8+
- pip

### Setup environnement

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Éditer `.env` et configurer :
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SECRET_KEY` (générer une clé aléatoire)
- `PASSWORD_RESET_SALT`

## Démarrage

### Application web (port 5000)

```bash
python app.py
```

Puis accédez à `http://localhost:5000`

### Tests

```bash
pytest
```

Cela exécutera tous les tests et générera un rapport de couverture ≥85%.

### Tests spécifiques

```bash
pytest tests/test_auth.py -v
pytest tests/test_auth.py::TestPasswordResetFlow10Steps -v
```

## Architecture

### Structure

```
v3/
├── backend/
│   ├── models.py          # Modèles SQLAlchemy
│   ├── auth.py            # Endpoints authentification
│   └── services/
│       └── email.py       # Service email reset MDP
├── config.py              # Configuration (SMTP, DB, etc.)
├── app.py                 # Application Flask
├── requirements.txt       # Dépendances
├── tests/
│   ├── conftest.py        # Configuration pytest
│   └── test_auth.py       # Tests authentification + reset MDP
└── .env                   # Secrets (à ne pas versionner)
```

## Modèles de données

### User
- `id` : Identifiant unique
- `email` : Email unique
- `password_hash` : Hash mot de passe (bcrypt)
- `role` : `user` ou `admin`
- `progress_json` : JSON progression utilisateur
- `installed_apps` : JSON liste apps installées
- `created_at`, `last_login`

### PasswordReset
- `token` : Token unique UUID
- `user_id` : Référence User
- `expires_at` : Expiration (1h par défaut)
- `used` : Booléen (à usage unique)

### App, AppData, Config, Message
(Voir `backend/models.py` pour détails)

## Endpoints API

### Authentification

#### POST `/auth/register`
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

#### POST `/auth/login`
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

#### POST `/auth/logout`
Requiert session active.

#### POST `/auth/reset_password`
Étape 1-3 : Demande réinitialisation
```json
{
  "email": "user@example.com"
}
```

#### GET `/auth/verify_token/<token>`
Étape 4 : Vérification token (formulaire)

#### POST `/auth/confirm_reset`
Étape 6-10 : Soumettre nouveau mot de passe
```json
{
  "token": "uuid-token",
  "password": "NewPassword123"
}
```

#### GET `/auth/me`
Récupère l'utilisateur connecté. Requiert session active.

## Reset Mot de Passe — 10 Étapes

1. **Utilisateur clique** "Mot de passe oublié" (frontend)
2. **Saisit email** et soumet
3. **Email reçu** avec lien sécurisé (token UUID, expiration 1h)
4. **Clic lien** → Vérification token via `GET /auth/verify_token/<token>`
5. **Affichage formulaire** nouveau MDP
6. **Saisie + soumission** nouveau MDP avec token
7. **Validation token** (non expiré, non utilisé)
8. **Update `password_hash`** en DB (bcrypt)
9. **Marquer token `used=True`** (à usage unique)
10. **Confirmation email** + Redirection login

## Tests

### Couverture

- ✅ Registration (succès, email dupliqué, password faible)
- ✅ Login (succès, email invalide, password invalide)
- ✅ Logout
- ✅ Password reset request
- ✅ Token generation, expiration, usage unique
- ✅ Confirm reset (token valide, expiré, utilisé, password faible)
- ✅ Flux complet 10 étapes

**Cible** : ≥85% coverage (actuellement XX%)

```bash
pytest --cov=backend --cov-report=term-missing
```

## Sécurité

- ✅ Passwords hashés (bcrypt)
- ✅ Reset tokens UUID sécurisés
- ✅ Expiration tokens 1h
- ✅ Tokens à usage unique
- ✅ SMTP TLS
- ✅ CSRF protection
- ✅ Session security

## Déploiement

### Production

1. Générer `SECRET_KEY` aléatoire
2. Configurer `PASSWORD_RESET_SALT`
3. Configurer SMTP (Gmail, SendGrid, etc.)
4. Configurer `SQLALCHEMY_DATABASE_URI` (PostgreSQL recommandé)
5. Lancer avec serveur WSGI (Gunicorn)

```bash
gunicorn app:create_app
```

## Prochaines phases

- **Phase 2** : Frontend (charte graphique V3, templates HTML)
- **Phase 3** : Système applications (install/uninstall)
- **Phase 4** : Progression & récompenses
- **Phase 5** : Panel admin
- **Phase 6+** : Frontend dashboard, apps "Présentation" et "Bénévoles"

## Licence

MIT

## Support

Pour issues ou questions : [GitHub Issues](https://github.com/ServOMorph/JeGeekUtile/issues)
