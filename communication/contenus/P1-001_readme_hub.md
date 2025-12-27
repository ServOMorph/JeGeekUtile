# P1-001 - Contenu README repo hub

## Instructions pour la VM

### 1. Créer le repo
```bash
gh repo create jegeekutile/jegeekutile --public --description "Association loi 1901 - IA locale, open source et bénévolat tech"
cd jegeekutile
```

### 2. Créer le README.md
Copier le contenu ci-dessous dans `README.md` :

---

```markdown
# Je Geek Utile

**Association loi 1901 qui met l'IA locale et l'open source au service des associations et du bénévolat.**

[![Licence MIT](https://img.shields.io/badge/Licence-MIT-green.svg)](LICENSE)
[![Open Source Helpers](https://img.shields.io/badge/Open%20Source-Helpers%20Welcome-orange.svg)](CONTRIBUTING.md)
[![Tests](https://img.shields.io/badge/Tests-100%25-brightgreen.svg)]()

## Notre mission

- Développer des outils IA accessibles fonctionnant en local (sans cloud)
- Accompagner les associations dans leur transition numérique responsable
- Valoriser le bénévolat tech via notre système de reconnaissance Geekos

## Projets

| Projet | Description |
|--------|-------------|
| [console-agents](console-agents/) | Console multi-agents IA locale (Ollama, OpenAI, Claude) |
| [site-internet](site-internet/) | Site Flask avec SEO et gestion bénévoles |
| [applis](applis/) | Applications métier (statistiques IA, outils internes) |

## Contribuer

Nous accueillons toutes les contributions : code, documentation, traduction, tests.

Consultez notre [guide de contribution](CONTRIBUTING.md) et nos [issues "good first issue"](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

## Licence

MIT - Voir [LICENSE](LICENSE)

---

**Contact** : [Mastodon @jegeekutile](https://framapiaf.org/@jegeekutile) | [Discussions GitHub](../../discussions)
```

---

### 3. Ajouter les topics
```bash
gh repo edit jegeekutile/jegeekutile --add-topic association --add-topic open-source --add-topic ia --add-topic local-ai --add-topic volunteering --add-topic flask --add-topic mastodon --add-topic eco-design
```

### 4. Créer les fichiers complémentaires

#### LICENSE (MIT)
```bash
curl -o LICENSE https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt
# Modifier avec : Je Geek Utile et l'année 2025
```

#### CONTRIBUTING.md
```markdown
# Contribuer à Je Geek Utile

Merci de votre intérêt pour Je Geek Utile !

## Comment contribuer

1. **Fork** le repo
2. **Créez** une branche (`git checkout -b feature/ma-contribution`)
3. **Commitez** vos changements
4. **Poussez** vers votre fork
5. **Ouvrez** une Pull Request

## Types de contributions

- Code (Python, JavaScript, HTML/CSS)
- Documentation
- Traduction
- Tests
- Signalement de bugs

## Code de conduite

Soyez respectueux et bienveillant. Nous accueillons tous les niveaux d'expérience.

## Questions ?

Ouvrez une [Discussion](../../discussions) ou contactez-nous sur Mastodon.
```

### 5. Push initial
```bash
git add .
git commit -m "Initial commit - README, LICENSE, CONTRIBUTING"
git push -u origin main
```

---

## Checklist validation

- [ ] Repo créé et public
- [ ] README avec mission claire
- [ ] Topics configurés (8 topics)
- [ ] Badges visibles
- [ ] LICENSE MIT présente
- [ ] CONTRIBUTING.md présent
