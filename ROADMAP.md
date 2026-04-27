# Roadmap — JeGeekUtile

Ce fichier centralise la progression globale du projet JeGeekUtile.

## État Global : Version 3.0 (En développement)

---

## ✅ Phase 1 : Cœur du Système (V1/V2)
- [x] Application Flask de base (Site internet)
- [x] Structure de la base de données SQLite
- [x] Système de membres et espace bénévole
- [x] Monnaie virtuelle (Geekos)

## ✅ Phase 2 : Orchestration IA (V1/V2)
- [x] Mise en place de Claude Code
- [x] Création de l'orchestrateur **Robert**
- [x] Agents spécialisés (Halu, PromptParfait, ComIA, AdminIA)
- [x] Système de détection d'hallucinations

## ✅ Phase 3 : Applications Satellites (V1/V2)
- [x] API d'automatisation **auto_ia**
- [x] Tracker d'usage **stat_usage_ia**
- [x] Console de gestion des agents (Console Agents)

## ✅ Phase 4 : Consolidation & Visibilité (V2)
- [x] Finalisation de la documentation des partenariats
- [x] Optimisation du référencement GitHub
- [x] Mise en place du CI/CD (GitHub Actions)
- [x] Campagne de diffusion (Mastodon, Forums)

---

# 🚀 Version 3.0 - JeGeekUtile UI V3 (ACTIVE)

> [!IMPORTANT]
> **Règle de développement** : À chaque lancement de phase concernant le développement du nouveau site internet, il est **obligatoire** de relire les documents de conception contenus dans `site internet/V2` (SSD, Plan de développement).

**Vision** : Créer un tableau de bord personnel et un panel d'administration modulaire pour l'association JeGeekUtile, avec applications installables, système de progression et gestion sécurisée.


## ✅ Phase 5 : Core Dashboard + Auth + Reset MDP (COMPLÉTÉE)
- [x] Repository Git initialisé avec structure complète
- [x] Base de données avec migrations (User, App, AppData, Config, Message, PasswordReset)
- [x] Système d'authentification (login/logout)
- [x] **Reset mot de passe par email avec validation obligatoire (10 étapes)**
- [x] Configuration SMTP fonctionnelle
- [x] Tests backend ≥ 85% coverage (90.27% atteint)

## 🏃 Phase 6 : App "Présentation" + App "Bénévoles" (EN COURS)
- [x] Système de gestion des applications (auto-création + installation)
- [x] **Application "Présentation" (installée par défaut)**
- [ ] **Application "Bénévoles" (modèle jeu vidéo, installable)**
- [x] Catalogue apps dans dashboard
- [ ] Fenêtres apps indépendantes (popup/modal/iframe)

## 📅 Phase 7 : Dashboard UI + Navigation (COMPLÉTÉE)
- [x] Navigation horizontale en haut (refonte sidenav)
- [x] Titre "JeGeekUtile" centré et lumineux
- [x] Pseudo utilisateur neon à droite
- [x] Module Info avec carrousel images (20 images)
- [x] Suppression zone discussion
- [x] Réduction taille apps installées (moitié)

## 📅 Phase 8 : Système Progression + Dashboard
- [ ] Tracker temps utilisation par app
- [ ] Compteur contributions (actions utilisateur)
- [ ] Système badges (paliers débloqués)
- [x] Indicateur progression visible

## 📅 Phase 9 : Panel Admin + Config Dynamique
- [ ] Dashboard admin complet
- [x] Config.py éditable (port configurable)
- [ ] Logs modifications (audit trail)
- [ ] Reset MDP utilisateur par admin

## ✅ Phase 10 : Charte Graphique + Agencement UI (COMPLÉTÉE)
- [x] **Intégration complète charte graphique V3**
- [x] **Respect strict agencement référence V3**
- [x] Navigation horizontale conforme
- [x] Responsive grid layout
- [ ] Responsive design (mobile/tablet/desktop)

## 📅 Phase 11 : Tests & Optimisation
- [x] **Coverage global ≥ 85%**
- [ ] **Performance <2s validée**
- [ ] Sécurité auditée
- [ ] Déploiement staging + production

---

### Roadmaps détaillées
- [Roadmap Visibilité GitHub](docs/ROADMAP_GITHUB_VISIBILITE.md)
- [Proposition Roadmap V3 détaillée](site internet/V2/Proposition_ROADMAP.md)

---

## ✅ Tâches Accomplies

- **(2026-04-27)** : Lancement de la version 3.0. Intégration de la roadmap UI V3 dans le fichier central. Mise en place de la règle de développement pour la relecture obligatoire des documents de conception V2.
- **(2026-04-27)** : Refonte du dashboard - Navigation horizontale en haut, titre "JeGeekUtile" géant centré, pseudo utilisateur neon à droite. Suppression zone discussion, réduction apps de moitié.
- **(2026-04-27)** : Module Info avec carrousel d'images (20 images PNG/JPG depuis Bot ou pas Bot), changement port configurable via config.py.
- **(2026-04-27)** : Auto-création utilisateurs de test et app Présentation au démarrage. Endpoint /assets/ pour servir images externes.
- **(2026-04-27)** : Phases 5 (Auth), 2 (Frontend V3), et 10 (Charte graphique) complétées. Phase 6 (Apps) initiée avec Présentation.

*Dernière mise à jour : 27/04/2026*

