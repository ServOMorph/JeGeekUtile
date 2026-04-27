text
# Plan de développement - JeGeekUtile UI V3

## Vue d'ensemble
**Durée estimée** : 8-10 semaines  
**Méthodologie** : Développement itératif par phases  
**Couverture tests** : 85% minimum obligatoire  
**Déploiement** : Progressif (local → dev → staging → prod)

## Phase 0 - Préparation (Semaine 1)

### 0.1 Setup environnement
- [ ] Initialiser repository Git
- [ ] Créer structure dossiers (voir SSD §11)
- [ ] Setup environnement virtuel Python
- [ ] Installer dépendances de base
- [ ] Configurer pytest + coverage
- [ ] Setup pre-commit hooks

### 0.2 Configuration initiale
- [ ] Créer `config.py.example` avec variables SMTP
- [ ] Créer `requirements.txt`
- [ ] Setup `.gitignore`
- [ ] Documenter README.md basique
- [ ] Copier charte graphique dans `src/static/charte/`
- [ ] Analyser UI référence `D:\ServOMorph\Bot ou pas Bot\UI\V3`
- [ ] Extraire éléments de `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`

### 0.3 Choix technologiques
- [ ] Décider framework backend (Flask recommandé pour simplicité)
- [ ] Choisir ORM (SQLAlchemy)
- [ ] Décider DB dev/prod (SQLite/PostgreSQL)
- [ ] Choisir système templates (Jinja2)
- [ ] Définir structure CSS (respect charte graphique)

**Livrables** :
- Repository initialisé
- Environnement dev fonctionnel
- Documentation setup

---

## Phase 1 - Backend Core & Auth (Semaines 2-3)

### 1.1 Modèles de données
**Fichier** : `backend/models.py`
- [ ] Modèle `User` (id, email, password_hash, role, progress_json, installed_apps, created_at)
- [ ] Modèle `App` (id, name, slug, html_path, is_default, admin_only)
- [ ] Modèle `AppData` (id, user_id, app_id, data_json)
- [ ] Modèle `Config` (key, value)
- [ ] Modèle `Message` (id, chat_id, user_id, content, timestamp)
- [ ] Modèle `PasswordReset` (token, user_id, expires_at, used)
- [ ] Relations entre modèles
- [ ] Migrations DB initiales

### 1.2 Authentification
**Fichier** : `backend/auth.py`
- [ ] Hash passwords (bcrypt/argon2)
- [ ] Fonction login (vérification email/password)
- [ ] Fonction logout
- [ ] Gestion sessions utilisateur
- [ ] Middleware protection routes admin
- [ ] Décorateurs `@login_required` et `@admin_required`

### 1.3 Reset mot de passe (PRIORITÉ ABSOLUE)
**Fichier** : `backend/services/email.py`
- [ ] Configuration SMTP depuis `config.py` (voir SSD §13)
- [ ] Génération token sécurisé (uuid + timestamp)
- [ ] Fonction envoi email avec lien reset
- [ ] Fonction validation token (expiration 1h, usage unique)
- [ ] Endpoint `POST /auth/reset_password {email}`
- [ ] Endpoint `POST /auth/confirm_reset {token, new_password}`
- [ ] Email confirmation après reset
- [ ] **Processus complet selon SSD §15 (10 étapes)**

### 1.4 Tests Phase 1
**Fichiers** : `tests/test_auth.py`, `tests/test_models.py`
- [ ] Tests modèles (création, relations)
- [ ] Tests login/logout
- [ ] Tests reset MDP (token valide/expiré/utilisé)
- [ ] Tests envoi email (mock SMTP)
- [ ] Tests processus complet reset (10 étapes)
- [ ] Coverage ≥ 85%

**Livrables** :
- DB fonctionnelle avec migrations
- Authentification complète
- **Reset MDP par email 100% opérationnel (validation obligatoire)**
- Tests backend core validés

---

## Phase 2 - Frontend Base & Charte Graphique (Semaines 4-5)

### 2.1 Intégration charte graphique (PRIORITÉ)
**Source** : `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`
- [ ] Extraire CSS complet de la charte
- [ ] Créer `static/css/charte.css`
- [ ] Définir classes réutilisables (boutons, cartes, formulaires)
- [ ] Créer palette couleurs
- [ ] Définir typographie
- [ ] Créer composants UI selon charte
- [ ] **Respecter strictement la charte (SSD §10)**

### 2.2 Agencement UI de référence
**Source** : `D:\ServOMorph\Bot ou pas Bot\UI\V3`
- [ ] Analyser disposition éléments
- [ ] Créer grille layout principal
- [ ] Définir zones (apps, discussion, infos, logos)
- [ ] **Respecter strictement l'agencement (SSD §10)**
- [ ] Responsive design (mobile/tablet/desktop)

### 2.3 Templates de base
**Dossier** : `src/templates/`
- [ ] `base.html` (layout global, charte graphique)
- [ ] `login.html` (formulaire connexion)
- [ ] `forgot_password.html` (saisie email)
- [ ] `reset_password.html` (nouveau MDP + token)
- [ ] `dashboard.html` (vue utilisateur selon agencement V3)
- [ ] `admin.html` (vue admin)

### 2.4 Navigation et routing
**Fichier** : `backend/routes.py`
- [ ] Route `/` (redirect login ou dashboard)
- [ ] Route `/login` (GET + POST)
- [ ] Route `/logout`
- [ ] Route `/forgot-password` (GET + POST)
- [ ] Route `/reset-password/<token>` (GET + POST)
- [ ] Route `/dashboard` (user)
- [ ] Route `/admin` (admin only)
- [ ] Gestion erreurs 404/403/500

### 2.5 Tests Phase 2
**Fichiers** : `tests/test_routes.py`, `tests/test_ui.py`
- [ ] Tests routes publiques (login, forgot password)
- [ ] Tests redirection non-authentifié
- [ ] Tests accès admin protégé
- [ ] Tests affichage templates
- [ ] Tests respect charte graphique
- [ ] Coverage ≥ 85%

**Livrables** :
- Interface login/reset fonctionnelle
- **Charte graphique strictement respectée**
- **Agencement V3 strictement respecté**
- Navigation de base opérationnelle

---

## Phase 3 - Système Applications (Semaines 6-7)

### 3.1 Infrastructure apps
**Fichier** : `backend/apps_manager.py`
- [ ] Fonction scan dossier `src/apps/`
- [ ] Chargement `metadata.json` par app
- [ ] Enregistrement apps en DB au démarrage
- [ ] Fonction installation app pour user
- [ ] Fonction désinstallation app
- [ ] Fonction récupération apps installées par user
- [ ] Gestion apps par défaut (auto-install "Présentation")

### 3.2 Application "Présentation" (SSD §8.1)
**Dossier** : `src/apps/presentation/`
- [ ] Créer `metadata.json` (is_default: true)
- [ ] Créer `index.html` (contenu projet association)
- [ ] Intégrer charte graphique
- [ ] **Fenêtre indépendante** (popup/modal/iframe)
- [ ] Données statiques/dynamiques depuis config
- [ ] Icon application
- [ ] Tests affichage

### 3.3 Application "Bénévoles" (SSD §8.2)
**Dossier** : `src/apps/benevoles/`
- [ ] Créer `metadata.json` (is_default: false)
- [ ] Créer `index.html` (interface type jeu vidéo)
- [ ] Interface gestion bénévoles (liste, ajout, édition)
- [ ] **Système progression ludique** (XP, niveaux, badges)
- [ ] Sauvegarde données dans `AppData` (JSON)
- [ ] **Fenêtre indépendante**
- [ ] Design inspiré jeu vidéo
- [ ] Tests CRUD bénévoles

### 3.4 Système fenêtres indépendantes
**Fichier** : `static/js/window_manager.js`
- [ ] Ouverture app en popup/modal
- [ ] Gestion multiples fenêtres simultanées
- [ ] État fenêtres (minimiser, maximiser, fermer)
- [ ] Isolation contexte par app
- [ ] Communication app ↔ dashboard (si nécessaire)

### 3.5 API Apps
**Fichier** : `backend/api.py`
- [ ] `GET /apps/catalog` (liste apps disponibles)
- [ ] `GET /user/apps` (apps installées)
- [ ] `POST /apps/install {app_id}` (installer app)
- [ ] `DELETE /apps/uninstall {app_id}` (désinstaller)
- [ ] `GET /apps/{app_id}/data` (récupérer données app)
- [ ] `PUT /apps/{app_id}/data` (sauvegarder données app)
- [ ] Validation permissions (pas désinstall app défaut)

### 3.6 Dashboard - Catalogue apps
**Template** : `dashboard.html`
- [ ] Grille apps installées (cards avec icône, nom)
- [ ] Bouton ouverture app (fenêtre indépendante)
- [ ] Section catalogue apps disponibles
- [ ] Bouton installation (+ animation)
- [ ] Badge "installée par défaut"
- [ ] Gestion ouverture multiples apps

### 3.7 Tests Phase 3
**Fichiers** : `tests/test_apps.py`
- [ ] Tests scan apps
- [ ] Tests installation/désinstallation
- [ ] Tests apps par défaut (Présentation auto-installée)
- [ ] Tests données apps (CRUD)
- [ ] Tests API apps
- [ ] Tests fenêtres indépendantes
- [ ] Coverage ≥ 85%

**Livrables** :
- Système apps modulaire fonctionnel
- **App "Présentation" installée par défaut**
- **App "Bénévoles" avec modèle jeu vidéo**
- Fenêtres indépendantes opérationnelles
- Catalogue apps dans dashboard

---

## Phase 4 - Progression & Discussion Placeholder (Semaines 8)

### 4.1 Système progression (SSD §17)
**Fichier** : `backend/progress.py`
- [ ] Tracker temps utilisation par app
- [ ] Compteur contributions (actions dans apps)
- [ ] Calcul progression (formule XP)
- [ ] Système badges (paliers débloqués)
- [ ] Classement utilisateurs (optionnel)
- [ ] Sauvegarde dans `User.progress_json`
- [ ] API `GET /user/progress`
- [ ] API `POST /user/progress/update {app_id, time, actions}`

### 4.2 UI Progression
**Template** : `dashboard.html` (section progression)
- [ ] Barre progression globale
- [ ] Liste badges débloqués
- [ ] Statistiques temps par app
- [ ] Animation déblocage badge
- [ ] Intégration selon agencement V3

### 4.3 Espace discussion - PLACEHOLDER UNIQUEMENT (SSD §16)
**Template** : `components/chat_placeholder.html`
- [ ] **Réserver espace dans UI selon agencement V3**
- [ ] Placeholder visuel "Discussion (à venir)"
- [ ] Zone grisée/désactivée
- [ ] Préparer structure HTML future
- [ ] **NE PAS développer fonctionnalités**
- [ ] Note admin : activation future possible

### 4.4 Tests Phase 4
**Fichiers** : `tests/test_progress.py`
- [ ] Tests calcul progression
- [ ] Tests déblocage badges
- [ ] Tests tracker temps
- [ ] Tests API progression
- [ ] Coverage ≥ 85%

**Livrables** :
- Système progression fonctionnel avec badges
- **Placeholder discussion visible dans UI**
- Dashboard enrichi avec progression

---

## Phase 5 - Panel Admin (Semaines 9-10)

### 5.1 Dashboard admin
**Template** : `admin.html`
- [ ] Vue toutes apps (y compris admin-only)
- [ ] Statistiques globales (users, apps, messages)
- [ ] Accès rapide config/données
- [ ] Logs activité récente
- [ ] Respect charte graphique

### 5.2 Gestion données (SSD §18)
**Fichier** : `backend/admin_data.py`
- [ ] Interface CRUD générique pour modèles
- [ ] Liste users (filtres, recherche)
- [ ] Édition user (sauf password_hash)
- [ ] Liste apps
- [ ] Liste messages
- [ ] Export CSV/JSON
- [ ] **Logs modifications (audit trail)**
- [ ] API `GET /admin/data/{model}`
- [ ] API `PUT /admin/data/{model}/{id}`
- [ ] API `DELETE /admin/data/{model}/{id}`

### 5.3 UI Gestion données
**Template** : `admin/data_manager.html`
- [ ] Tables dynamiques (tri, filtres)
- [ ] Formulaires édition inline
- [ ] Boutons export
- [ ] Confirmation suppression
- [ ] Pagination
- [ ] **Exclusion champs password_hash**

### 5.4 Config.py dynamique (SSD §19)
**Fichier** : `backend/config_manager.py`
- [ ] Lecture `config.py` (parsing variables)
- [ ] Affichage variables en formulaire
- [ ] Validation types (str, int, bool, etc.)
- [ ] Sauvegarde modifications dans `config.py`
- [ ] **Backup automatique avant modif**
- [ ] **Synchronisation immédiate avec app**
- [ ] API `GET /admin/config`
- [ ] API `PUT /admin/config`

### 5.5 UI Config
**Template** : `admin/config.html`
- [ ] Formulaire variables config
- [ ] Types adaptés (input, checkbox, select)
- [ ] Bouton sauvegarde
- [ ] Confirmation modification
- [ ] Indication sync réussie
- [ ] Historique backups

### 5.6 Gestion discussion par admin (SSD §16)
**Fichier** : `backend/admin_chat.py`
- [ ] Interface activation/désactivation discussion par user
- [ ] Liste users avec statut discussion (activé/désactivé)
- [ ] Toggle activation global/individuel

### 5.7 Reset MDP utilisateur (admin)
**Fichier** : `backend/admin_users.py`
- [ ] Fonction admin reset MDP pour user
- [ ] Envoi email lien reset au user
- [ ] Log action admin (audit trail)

### 5.8 Tests Phase 5
**Fichiers** : `tests/test_admin.py`
- [ ] Tests accès admin protégé
- [ ] Tests CRUD données
- [ ] Tests exclusion password_hash
- [ ] Tests édition config.py
- [ ] Tests backup config.py
- [ ] Tests sync temps réel config
- [ ] Tests reset MDP par admin
- [ ] Tests gestion discussion
- [ ] Coverage ≥ 85%

**Livrables** :
- Panel admin complet
- Gestion données CRUD opérationnelle
- **Config.py éditable avec sync temps réel**
- Audit trail fonctionnel
- Gestion activation discussion

---

## Phase 6 - Optimisation & Tests (Semaine 11)

### 6.1 Performance
- [ ] Optimisation requêtes DB (indexes, eager loading)
- [ ] Compression assets (CSS/JS minification)
- [ ] Cache stratégique (apps metadata, config)
- [ ] Lazy loading apps HTML
- [ ] Tests charge (100+ users simultanés)
- [ ] **Temps chargement <2s validé (SSD §10)**

### 6.2 Sécurité
- [ ] Audit dépendances (snyk, safety)
- [ ] Protection CSRF sur formulaires
- [ ] Validation inputs côté serveur
- [ ] Rate limiting (login, reset MDP)
- [ ] Sanitization données users
- [ ] Headers sécurité (CSP, HSTS)
- [ ] Tests pénétration basiques

### 6.3 Tests finaux
- [ ] Tests end-to-end (Selenium/Playwright)
- [ ] Tests compatibilité navigateurs
- [ ] Tests responsive (mobile/tablet/desktop)
- [ ] Tests accessibilité (WCAG basique)
- [ ] **Vérification coverage global ≥ 85% (SSD §10)**
- [ ] Tests respect charte graphique
- [ ] Tests respect agencement V3
- [ ] Correction bugs identifiés

### 6.4 Documentation
- [ ] README.md complet (install, config, usage)
- [ ] Documentation API (Swagger/OpenAPI)
- [ ] Guide admin (gestion données, config)
- [ ] Guide développeur (ajouter nouvelle app)
- [ ] Changelog
- [ ] Diagrammes architecture
- [ ] Documentation charte graphique
- [ ] Documentation agencement V3

### 6.5 Préparation déploiement
- [ ] Dockerfile
- [ ] docker-compose.yml (app + DB)
- [ ] Variables environnement (.env.example)
- [ ] Script migration DB prod
- [ ] Configuration Nginx/Apache (optionnel)
- [ ] CI/CD pipeline (GitHub Actions/GitLab CI)
- [ ] Tests déploiement automatisés

**Livrables** :
- Application optimisée et sécurisée
- **Coverage tests 85%+ (obligatoire)**
- Documentation complète
- **Performance <2s validée**
- Prêt pour déploiement

---

## Phase 7 - Déploiement (Post-développement)

### 7.1 Environnement staging
- [ ] Déployer sur serveur staging
- [ ] Tests utilisateurs internes
- [ ] Collecte feedback
- [ ] Corrections bugs critiques

### 7.2 Environnement production
- [ ] Configuration serveur prod
- [ ] Migration données initiales
- [ ] Déploiement progressif
- [ ] Monitoring (logs, erreurs, performances)
- [ ] Backup automatique DB

### 7.3 Formation & support
- [ ] Formation admins
- [ ] Formation utilisateurs
- [ ] Documentation support
- [ ] Process remontée bugs

---

## Checklist critique par phase

### Phase 1 ✓ (BLOQUANT)
- [ ] **Reset MDP par email fonctionne (10 étapes SSD §15)**
- [ ] **Tokens expiration 1h validée**
- [ ] **Email validation obligatoire**
- [ ] Tests auth ≥ 85%

### Phase 2 ✓ (BLOQUANT)
- [ ] **Charte graphique strictement respectée**
- [ ] **Agencement V3 strictement respecté**
- [ ] Login/logout fonctionnels

### Phase 3 ✓
- [ ] **App "Présentation" installée par défaut**
- [ ] **App "Bénévoles" avec modèle jeu vidéo**
- [ ] **Fenêtres indépendantes opérationnelles**

### Phase 4 ✓
- [ ] Progression temps réel trackée
- [ ] **Placeholder discussion visible dans UI**

### Phase 5 ✓
- [ ] Admin CRUD données (sauf MDP)
- [ ] **Config.py sync temps réel**
- [ ] Activation/désactivation discussion par user

### Phase 6 ✓ (BLOQUANT)
- [ ] **Coverage global ≥ 85%**
- [ ] **Performance <2s validée**

---

## Stack finale

### Backend
- Python 3.10+
- Flask 3.x
- SQLAlchemy 2.x
- Flask-Login (sessions)
- Flask-Mail (SMTP)
- Pytest + pytest-cov

### Frontend
- HTML5 + CSS3 (charte graphique stricte)
- JavaScript Vanilla (pas de framework)
- Jinja2 templates

### Database
- SQLite (dev)
- PostgreSQL 15+ (prod)

### Déploiement
- Docker + docker-compose
- Nginx (reverse proxy)
- Gunicorn (WSGI)

---

## Estimation efforts

| Phase | Durée | Complexité | Risques |
|-------|-------|------------|---------|
| Phase 0 | 1 sem | Faible | Setup env |
| Phase 1 | 2 sem | Haute | **Email SMTP (BLOQUANT)** |
| Phase 2 | 2 sem | Haute | **Charte graphique stricte** |
| Phase 3 | 2 sem | Haute | **Fenêtres indépendantes** |
| Phase 4 | 1 sem | Moyenne | Placeholder simple |
| Phase 5 | 2 sem | Haute | **Config sync temps réel** |
| Phase 6 | 1 sem | Moyenne | **Coverage 85%** |

**Total** : 11 semaines (peut être réduit à 8 avec équipe expérimentée)

---

## Risques & mitigations

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| **Config SMTP invalide** | **BLOQUANT** | Moyenne | Tests avec Mailtrap/MailHog dès Phase 1 |
| **Charte graphique ambiguë** | **BLOQUANT** | Faible | Valider mockups Phase 2 avec référent |
| **Fenêtres séparées complexes** | Haute | Haute | POC iframe/popup dès début Phase 3 |
| **Config.py sync instable** | Haute | Moyenne | Tests intensifs backup + rollback |
| **Coverage 85% difficile** | **BLOQUANT** | Moyenne | TDD strict dès Phase 1 |
| **Performance <2s non atteinte** | Haute | Faible | Optimisation Phase 6 + cache |

---

## Règles de développement

### Git workflow
- Branch `main` protégée
- Feature branches `feature/nom`
- PR obligatoires avec review
- Tests passants avant merge
- Commits conventionnels (feat, fix, docs, etc.)

### Code quality
- Linting : flake8 / black (Python)
- Type hints Python 3.10+
- Docstrings fonctions
- Commentaires uniquement si nécessaire
- Pas de code mort

### Tests
- **TDD obligatoire**
- Tests unitaires + intégration
- Mocks services externes (email)
- Fixtures réutilisables
- **Coverage rapport HTML ≥ 85%**

### Règle EN CAS DE DOUTE (SSD §10)
- **NE PAS IMPLÉMENTER**
- Documenter le doute
- Demander validation
- Pas d'interprétation libre

### Review checklist
- [ ] Tests passants (≥ 85%)
- [ ] Code linté
- [ ] Documentation mise à jour
- [ ] Pas de credentials hardcodés
- [ ] **Charte graphique respectée**
- [ ] **Agencement V3 respecté**
- [ ] Performance validée

---

## Points de validation

### V0.1 - MVP Auth (Fin Phase 1)
- Login/logout fonctionnels
- **Reset MDP email opérationnel (10 étapes)**
- Dashboard vide affiché

### V0.5 - MVP Apps (Fin Phase 3)
- **2 apps installables (Présentation, Bénévoles)**
- Catalogue apps
- **Fenêtres indépendantes**

### V0.7 - Progression (Fin Phase 4)
- Progression + badges
- **Placeholder discussion visible**

### V0.9 - Admin complet (Fin Phase 5)
- Panel admin opérationnel
- **Config.py dynamique avec sync**
- Gestion activation discussion

### V1.0 - Production ready (Fin Phase 6)
- **Tests 85%+**
- **Performance <2s**
- Documentation complète
- Déployable

---

## Prochaines étapes immédiates

1. **Valider ce plan** avec parties prenantes
2. **Setup repository** (Phase 0.1)
3. **Analyser charte graphique** `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`
4. **Analyser agencement** `D:\ServOMorph\Bot ou pas Bot\UI\V3`
5. **Choisir framework** (Flask recommandé)
6. **Créer structure** fichiers/dossiers
7. **Démarrer Phase 1** (modèles DB + reset MDP)

---

## Priorités absolues (SSD §20)

1. **Reset MDP par email avec validation** (Phase 1 - BLOQUANT)
2. **Respect strict charte graphique** (Phase 2 - BLOQUANT)
3. **Respect strict agencement V3** (Phase 2 - BLOQUANT)
4. **Développer uniquement 2 apps** : Présentation + Bénévoles (Phase 3)
5. **Fenêtres apps indépendantes** (Phase 3)
6. **Config.py sync temps réel** (Phase 5)
7. **Coverage 85%** (Phase 6 - BLOQUANT)
8. **Performance <2s** (Phase 6 - BLOQUANT)
9. **En cas de doute → NE PAS IMPLÉMENTER** (toutes phases)

---

## Contact & support

**Chef de projet** : [À définir]  
**Lead dev** : [À définir]  
**Repository** : [URL à définir]  
**Documentation** : [URL à définir]  
**Charte graphique** : `D:\ServOMorph\Bot ou pas Bot\UI\V3\Charte Graphique v3.html`  
**Agencement référence** : `D:\ServOMorph\Bot ou pas Bot\UI\V3`
