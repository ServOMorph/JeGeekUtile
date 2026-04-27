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


## 🏃 Phase 5 : Core Dashboard + Auth + Reset MDP (ACTIVE)
- [ ] Repository Git initialisé avec structure complète
- [ ] Base de données avec migrations (User, App, AppData, Config, Message, PasswordReset)
- [ ] Système d'authentification (login/logout)
- [ ] **Reset mot de passe par email avec validation obligatoire (10 étapes)**
- [ ] Configuration SMTP fonctionnelle
- [ ] Tests backend ≥ 85% coverage

## 📅 Phase 6 : App "Présentation" + App "Bénévoles"
- [ ] Système de gestion des applications (scan, install, uninstall)
- [ ] **Application "Présentation" (installée par défaut)**
- [ ] **Application "Bénévoles" (modèle jeu vidéo, installable)**
- [ ] Catalogue apps dans dashboard
- [ ] Fenêtres apps indépendantes (popup/modal/iframe)

## 📅 Phase 7 : Système Progression + Placeholder Discussion
- [ ] Tracker temps utilisation par app
- [ ] Compteur contributions (actions utilisateur)
- [ ] Système badges (paliers débloqués)
- [ ] **Placeholder discussion dans UI (zone réservée)**

## 📅 Phase 8 : Panel Admin + Config.py Dynamique
- [ ] Dashboard admin complet
- [ ] **Config.py éditable via UI avec sync temps réel**
- [ ] Logs modifications (audit trail)
- [ ] Reset MDP utilisateur par admin

## 📅 Phase 9 : Charte Graphique + Agencement UI
- [ ] **Intégration complète charte graphique V3**
- [ ] **Respect strict agencement référence V3**
- [ ] Responsive design (mobile/tablet/desktop)

## 📅 Phase 10 : Tests, Optimisation & Déploiement
- [ ] **Coverage global ≥ 85%**
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

*Dernière mise à jour : 27/04/2026*

