# Comment contribuer à Je Geek Utile

Merci de ton intérêt. Ce guide explique comment participer au projet.

---

## Prérequis

- Python 3.8+
- Git
- Navigateur web moderne

---

## Processus de contribution

### 1. Fork et clone

```bash
git clone https://github.com/[ton-user]/JeGeekUtile.git
cd JeGeekUtile
```

### 2. Crée une branche

```bash
git checkout -b feat/ma-contribution
# ou
git checkout -b fix/mon-correctif
```

### 3. Installe les dépendances

```bash
cd "site internet"
pip install -r requirements.txt
```

### 4. Développe et teste

```bash
python tests/runner.py
```

Le seuil de réussite est **80%**. Les contributions doivent maintenir ou améliorer le score.

### 5. Commit

Convention de commit :

```
feat: ajout d'une fonctionnalité
fix: correction d'un bug
docs: mise à jour documentation
style: changement CSS/UI sans impact fonctionnel
refactor: refactorisation sans nouvelle fonctionnalité
test: ajout ou modification de tests
```

### 6. Ouvre une Pull Request

- Décris clairement ce que fait ta PR
- Référence l'issue concernée si applicable (`Closes #123`)
- Les tests doivent passer

---

## Signaler un bug

Ouvre une [issue](https://github.com/ServOMorph/JeGeekUtile/issues) avec :
- Description du comportement observé
- Étapes pour reproduire
- Comportement attendu
- Environnement (OS, Python version)

---

## Proposer une fonctionnalité

Ouvre une [issue](https://github.com/ServOMorph/JeGeekUtile/issues) avec le label `enhancement` et décris le besoin.

---

## Principes à respecter

- **Éco-responsabilité** : thème sombre, zéro dépendance externe superflue, < 5% pixels blancs
- **Simplicité** : pas de sur-ingénierie, Vanilla JS privilégié
- **Traçabilité** : tout échange agent doit être loggé
- **RGPD** : aucune donnée personnelle en clair dans le code

---

## Questions ?

Ouvre une issue avec le label `question`.
