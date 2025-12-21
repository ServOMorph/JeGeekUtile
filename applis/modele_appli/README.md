# Modèle Standard Applications - Je Geek Utile

Modèle réutilisable pour toutes les applications du projet.

## Caractéristiques

### Mode Sombre Éco-responsable
- **Pixels blancs** : < 5%
- **Optimisé** : Faible consommation électrique
- **Cohérent** : Même charte graphique partout

### Palette Couleurs Standard

```css
--bg-primary: #1a1a1a       /* Background principal */
--bg-secondary: #2d2d2d     /* Background secondaire */
--bg-tertiary: #4a4a4a      /* Background tertiaire */
--accent-primary: #2d5016   /* Accent vert foncé */
--accent-secondary: #6b8e23 /* Accent vert clair */
--text-primary: #b8b8b8     /* Texte principal */
--text-secondary: #6b8e23   /* Texte secondaire */
--border-color: #6b8e23     /* Bordures */
--alert-color: #8b4513      /* Alertes */
--warning-color: #ff8c00    /* Avertissements */
```

### Typographie Standard

**Police** : `'Consolas', 'Monaco', 'Courier New', monospace`

**Tailles** :
- Body : 14px
- Header h1 : 20px
- Stats : 16px (valeurs), 11px (labels)
- Footer : 11px

### Footer Standard

Position : En bas à droite
Format : `@Je Geek Utile - DD/MM/YYYY - [NOM_APPLI] v[VERSION]`

## Utilisation

### 1. Copier le modèle

```bash
cp -r applis/modele_appli applis/mon_appli
cd applis/mon_appli
```

### 2. Personnaliser

**Dans `index.html` :**
- Remplacer `[NOM_APPLI]` par le nom de votre application
- Remplacer `[VERSION]` par le numéro de version (ex: 1.0)
- Adapter les vues dans `<nav>`

**Dans `app.js` :**
- Ajouter vos données dans `data: {}`
- Implémenter `loadData()`
- Créer vos vues `renderView1()`, etc.
- Ajouter événements dans `attachViewEvents()`

**Dans `style.css` :**
- Ajouter vos styles spécifiques (optionnel)
- Conserver les variables CSS

### 3. Structure fichiers

```
mon_appli/
├── index.html          HTML principal
├── app.js              Logique application
├── style.css           Styles (hérite du modèle)
├── donnees/            Données JSON
│   └── data.json
└── README.md           Documentation
```

## Composants Disponibles

### Boutons

```html
<button class="btn-primary">Action principale</button>
<button class="btn-secondary">Action secondaire</button>
<button class="btn-danger">Supprimer</button>
```

### Cards

```html
<div class="card">
  <h3>Titre</h3>
  <p>Contenu</p>
</div>
```

### Formulaires

```html
<div class="form-group">
  <label>Libellé</label>
  <input type="text" placeholder="...">
</div>
```

### Grilles

```html
<div class="grid-2"><!-- 2 colonnes --></div>
<div class="grid-3"><!-- 3 colonnes --></div>
<div class="grid-4"><!-- 4 colonnes --></div>
```

### Métriques

```html
<div class="metric-card">
  <div class="metric-label">Label</div>
  <div class="metric-value">42</div>
  <div class="metric-detail">Détail</div>
</div>
```

### Tableaux

```html
<table>
  <thead>
    <tr>
      <th>Colonne 1</th>
      <th>Colonne 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Valeur 1</td>
      <td>Valeur 2</td>
    </tr>
  </tbody>
</table>
```

### Notifications

```javascript
App.showNotification('Message succès', 'success');
App.showNotification('Message erreur', 'error');
```

## Structure JavaScript

### Initialisation

```javascript
const App = {
  data: {
    currentView: 'view1',
    items: []
  },

  async init() {
    this.setFooterDate();
    await this.loadData();
    this.setupNavigation();
    this.render('view1');
  }
};
```

### Chargement données

```javascript
async loadData() {
  const res = await fetch('donnees/data.json');
  this.data.items = await res.json();
}
```

### Rendu vues

```javascript
renderView1() {
  return `<div>Mon contenu HTML</div>`;
}
```

### Événements

```javascript
attachViewEvents(view) {
  if (view === 'view1') {
    document.getElementById('btn').addEventListener('click', () => {
      // Action
    });
  }
}
```

## Classes Utilitaires

```css
.text-center      /* Texte centré */
.mt-20           /* Marge top 20px */
.mb-20           /* Marge bottom 20px */
.gap-20          /* Gap 20px */
.hidden          /* Caché */
```

## Checklist Nouvelle Application

- [ ] Copier modèle
- [ ] Remplacer `[NOM_APPLI]` partout
- [ ] Remplacer `[VERSION]`
- [ ] Adapter navigation (vues)
- [ ] Implémenter `loadData()`
- [ ] Créer vues `renderViewX()`
- [ ] Ajouter événements
- [ ] Tester footer (date + version)
- [ ] Vérifier mode sombre
- [ ] Créer README spécifique

## Principes Conception

1. **Éco-responsabilité** : Mode sombre, < 5% pixels blancs
2. **Cohérence** : Même charte partout
3. **Simplicité** : Vanilla JS, pas de framework
4. **Performance** : Lightweight, optimisé
5. **Maintenabilité** : Structure claire, réutilisable

## Support

Toutes les applications du projet `applis/` suivent ce modèle.

---

**Modèle** : v1.0
**Date** : 26/11/2025
**Auteur** : @Je Geek Utile
