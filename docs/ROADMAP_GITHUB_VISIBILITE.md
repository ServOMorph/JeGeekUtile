# Roadmap — Visibilité GitHub & Buzz

Objectif : rendre le repo public, attractif et contributif.

Dernière mise à jour : 2026-03-11

---

## Statut global

| Phase | Intitulé | Statut |
|-------|----------|--------|
| 1 | Fondations légales et sécurité | [x] Terminé |
| 2 | README visuel et percutant | [~] En cours (2.4/2.5 manuels) |
| 3 | Fichiers communautaires GitHub | [x] Terminé |
| 4 | CI/CD et automatisation | [ ] En attente |
| 5 | Référencement et diffusion | [ ] En attente |

---

## Phase 1 — Fondations légales et sécurité

Priorité absolue. Sans ces bases, le repo ne peut pas buzzer légalement ni en toute sécurité.

| # | Tâche | Fichier | Statut | Notes |
|---|-------|---------|--------|-------|
| 1.1 | Choisir une licence open source | `LICENSE` | [x] | MIT |
| 1.2 | Créer le fichier `LICENSE` à la racine | `LICENSE` | [x] | Créé le 2026-03-11 |
| 1.3 | Mettre à jour la section Licence du README | `README.md` | [x] | MIT — voir LICENSE |
| 1.4 | Supprimer les credentials du README | `README.md` | [x] | Retiré le 2026-03-11 |
| 1.5 | Vérifier `.gitignore` — exclure `.env`, BDD, données sensibles | `.gitignore` | [x] | OK — `*.db`, `.env`, données sensibles exclus |

---

## Phase 2 — README visuel et percutant

Le README est la vitrine. Il doit convaincre en 10 secondes.

| # | Tâche | Statut | Notes |
|---|-------|--------|-------|
| 2.1 | Ajouter le logo JGU en haut du README | [x] | `ASSETS/IMAGES/LOGOS/logo_titre_transparent_1.png` — centré |
| 2.2 | Ajouter les badges en dessous du logo | [x] | 6 badges shields.io — ServOMorph/JeGeekUtile |
| 2.3 | Réécrire l'accroche (proposition de valeur) | [x] | Angle : outil humain, bénévoles, éco, open source |
| 2.4 | Ajouter une section screenshots | [ ] | Capturer : accueil, admin, console agents |
| 2.5 | Ajouter un GIF de démo (optionnel) | [ ] | Outil : Licecap ou ShareX |
| 2.6 | Ajouter section "Pourquoi ce projet ?" | [x] | 3 bullets : IA contrôlée, éco, autonomie bénévoles |
| 2.7 | Ajouter section "Roadmap" avec lien vers ce fichier | [x] | Lien vers docs/ROADMAP_GITHUB_VISIBILITE.md |
| 2.8 | Ajouter section "Comment contribuer ?" | [x] | Fork → branche → PR + lien issues GitHub |

### Badges à intégrer

```markdown
![Licence](https://img.shields.io/github/license/[user]/[repo])
![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Version](https://img.shields.io/badge/version-2.0-informational)
![Statut](https://img.shields.io/badge/statut-production--ready-success)
![Éco](https://img.shields.io/badge/pixels--blancs-%3C5%25-2d5016)
```

### Accroche proposée

```
Je Geek Utile — La technologie au service de l'humain.

Système open source pour associations : site web Flask, agents IA Claude Code
orchestrés, console de gestion, et outils satellites. Éco-responsable,
traçable, auto-suffisant.
```

---

## Phase 3 — Fichiers communautaires GitHub

Ces fichiers déclenchent des badges automatiques sur GitHub et signalent un projet sérieux.

| # | Fichier | Statut | Contenu |
|---|---------|--------|---------|
| 3.1 | `.github/CONTRIBUTING.md` | [x] | Convention commits, process PR, principes JGU |
| 3.2 | `.github/CODE_OF_CONDUCT.md` | [x] | Contributor Covenant v2.1 |
| 3.3 | `.github/SECURITY.md` | [x] | Security Advisories GitHub |
| 3.4 | `.github/ISSUE_TEMPLATE/bug_report.md` | [x] | Template bug avec OS/Python/version |
| 3.5 | `.github/ISSUE_TEMPLATE/feature_request.md` | [x] | Template demande fonctionnalité |
| 3.6 | `.github/PULL_REQUEST_TEMPLATE.md` | [x] | Checklist éco + tests + données sensibles |

---

## Phase 4 — CI/CD et automatisation

Un badge vert "tests passés" inspire confiance et attire les contributeurs.

| # | Tâche | Fichier | Statut | Notes |
|---|-------|---------|--------|-------|
| 4.1 | Créer workflow GitHub Actions pour les tests | `.github/workflows/tests.yml` | [ ] | Déclencher sur push + PR |
| 4.2 | Ajouter badge CI dans le README | `README.md` | [ ] | Après création du workflow |
| 4.3 | Vérifier compatibilité `tests/runner.py` avec GitHub Actions | `tests/runner.py` | [ ] | Exit code 0/1 selon résultat |

### Workflow tests.yml minimal

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r "site internet/requirements.txt"
      - run: python tests/runner.py
```

---

## Phase 5 — Référencement et diffusion

| # | Tâche | Statut | Notes |
|---|-------|--------|-------|
| 5.1 | Ajouter les topics sur le repo GitHub | [ ] | `flask`, `claude-code`, `ai-agents`, `python`, `association`, `eco-responsible`, `vanilla-js`, `french` |
| 5.2 | Remplir la description du repo GitHub | [ ] | 1 phrase + URL site si disponible |
| 5.3 | Épingler le repo sur le profil GitHub | [ ] | Profil → Customize pinned |
| 5.4 | Post Mastodon d'annonce | [ ] | Utiliser `/comia` pour générer le post |
| 5.5 | Soumettre sur awesome-claude-code (si liste existe) | [ ] | Chercher awesome-lists pertinentes |
| 5.6 | Partager sur forums francophones | [ ] | dev.to (FR), Zeste de Savoir, LinkedIn |

---

## Métriques de suivi

À remplir après chaque mise à jour :

| Date | Stars | Forks | Issues ouvertes | PRs | Vues (14j) |
|------|-------|-------|-----------------|-----|------------|
| 2026-03-11 | 0 | 0 | 0 | 0 | - |

---

## Décisions prises

| Date | Décision | Raison |
|------|----------|--------|
| - | - | - |

---

## Références

- [choosealicense.com](https://choosealicense.com) — Choisir une licence
- [Contributor Covenant](https://www.contributor-covenant.org) — Code de conduite standard
- [Shields.io](https://shields.io) — Générateur de badges
- [GitHub Docs — Community files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
