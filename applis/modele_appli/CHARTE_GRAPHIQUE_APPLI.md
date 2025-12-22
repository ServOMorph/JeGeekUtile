# Charte Graphique - Je Geek Utile

Charte graphique standardisée pour toutes les applications du projet.

## Palette Couleurs

### Système de Thèmes

Les applications proposent **5 thèmes configurables** représentant les valeurs du projet :

1. **Nuit Forêt** (défaut) - Éco-responsabilité
2. **Terre Éthique** - Éthique et transparence
3. **Cryptage Nocturne** - Sécurité des données
4. **Aurore Humaine** - IA pour les humains
5. **Horizon Progrès** - Innovation et progrès

Tous les thèmes respectent les contraintes OLED (noir profond, couleurs désaturées, > 70% pixels noirs).

### Variables CSS

#### Thème 1 : Nuit Forêt (Éco-responsabilité)

```css
:root[data-theme="nuit-foret"],
:root {
  /* === BACKGROUNDS === */
  --bg-primary: #0a0a0a;        /* Background principal (optimisé OLED) */
  --bg-secondary: #1a1a1a;      /* Background secondaire */
  --bg-tertiary: #2d2d2d;       /* Background tertiaire */
  --bg-elevated: #3a3a3a;       /* Background élevé (cards hover) */

  /* === ACCENTS === */
  --accent-primary: #2d5016;    /* Accent vert foncé */
  --accent-secondary: #6b8e23;  /* Accent vert clair */
  --accent-tertiary: #4a6b1e;   /* Accent vert moyen */

  /* === TEXTE === */
  --text-primary: #b8b8b8;      /* Texte principal (contraste 11:1) */
  --text-secondary: #8a8a8a;    /* Texte secondaire (contraste 6.5:1) */
  --text-accent: #6b8e23;       /* Texte accent */
  --text-muted: #6a6a6a;        /* Texte désactivé (contraste 4.5:1) */

  /* === ÉTATS === */
  --border-color: #6b8e23;      /* Bordures */
  --border-subtle: #3a3a3a;     /* Bordures subtiles */
  --alert-color: #8b4513;       /* Alertes/Erreurs */
  --warning-color: #cc7000;     /* Avertissements (désaturé pour OLED) */
  --success-color: #6b8e23;     /* Succès */
  --info-color: #5a7a8a;        /* Informations (évite bleu pur) */

  /* === INTERACTIONS === */
  --hover-overlay: rgba(107, 142, 35, 0.1);
  --active-overlay: rgba(107, 142, 35, 0.2);
  --focus-ring: #6b8e23;

  /* === ESPACEMENT === */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 20px;
  --space-xl: 30px;
  --space-xxl: 40px;

  /* === TYPOGRAPHIE === */
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 18px;
  --font-size-xxl: 20px;
  --font-size-display: 32px;

  --line-height-tight: 1.2;
  --line-height-base: 1.5;
  --line-height-relaxed: 1.7;

  /* === BORDURES & RAYONS === */
  --radius-sm: 3px;
  --radius-md: 5px;
  --radius-lg: 8px;
  --radius-xl: 12px;

  --border-width-thin: 1px;
  --border-width-base: 2px;
  --border-width-thick: 3px;
  --border-width-heavy: 4px;

  /* === OMBRES (minimales pour économie) === */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 4px 12px rgba(107, 142, 35, 0.15);

  /* === TRANSITIONS (réduites pour économie) === */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

#### Thème 2 : Terre Éthique (Éthique et transparence)

```css
:root[data-theme="terre-ethique"] {
  /* === BACKGROUNDS === */
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1512;
  --bg-tertiary: #2d2419;
  --bg-elevated: #3d3428;

  /* === ACCENTS === */
  --accent-primary: #342a1f;
  --accent-secondary: #7c9d6f;
  --accent-tertiary: #5a6d50;

  /* === TEXTE === */
  --text-primary: #d4c5b0;
  --text-secondary: #9d8b73;
  --text-accent: #7c9d6f;
  --text-muted: #6a5d50;

  /* === ÉTATS === */
  --border-color: #7c9d6f;
  --border-subtle: #3d3428;
  --alert-color: #8b4513;
  --warning-color: #b8956a;
  --success-color: #7c9d6f;
  --info-color: #7a8b7a;

  /* === INTERACTIONS === */
  --hover-overlay: rgba(124, 157, 111, 0.1);
  --active-overlay: rgba(124, 157, 111, 0.2);
  --focus-ring: #7c9d6f;

  /* Héritage des autres variables (espacement, typo, etc.) */
}
```

#### Thème 3 : Cryptage Nocturne (Sécurité des données)

```css
:root[data-theme="cryptage-nocturne"] {
  /* === BACKGROUNDS === */
  --bg-primary: #0a0a0a;
  --bg-secondary: #0f1419;
  --bg-tertiary: #1a2332;
  --bg-elevated: #253142;

  /* === ACCENTS === */
  --accent-primary: #1e2d3d;
  --accent-secondary: #5a7a8a;
  --accent-tertiary: #3f5f6f;

  /* === TEXTE === */
  --text-primary: #c0d0e0;
  --text-secondary: #8a9aaa;
  --text-accent: #5a7a8a;
  --text-muted: #6a7a8a;

  /* === ÉTATS === */
  --border-color: #5a7a8a;
  --border-subtle: #253142;
  --alert-color: #8a5a5a;
  --warning-color: #aa8a6a;
  --success-color: #6a8a7a;
  --info-color: #5a7a8a;

  /* === INTERACTIONS === */
  --hover-overlay: rgba(90, 122, 138, 0.1);
  --active-overlay: rgba(90, 122, 138, 0.2);
  --focus-ring: #5a7a8a;
}
```

#### Thème 4 : Aurore Humaine (IA pour les humains)

```css
:root[data-theme="aurore-humaine"] {
  /* === BACKGROUNDS === */
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a140f;
  --bg-tertiary: #2d2319;
  --bg-elevated: #3d3229;

  /* === ACCENTS === */
  --accent-primary: #3d2a1f;
  --accent-secondary: #b8956a;
  --accent-tertiary: #9a7a55;

  /* === TEXTE === */
  --text-primary: #d4c5b0;
  --text-secondary: #a89680;
  --text-accent: #b8956a;
  --text-muted: #7a6a55;

  /* === ÉTATS === */
  --border-color: #b8956a;
  --border-subtle: #3d3229;
  --alert-color: #aa6a5a;
  --warning-color: #cc8a60;
  --success-color: #8a9a6a;
  --info-color: #7a8a9a;

  /* === INTERACTIONS === */
  --hover-overlay: rgba(184, 149, 106, 0.1);
  --active-overlay: rgba(184, 149, 106, 0.2);
  --focus-ring: #b8956a;
}
```

#### Thème 5 : Horizon Progrès (Innovation et progrès)

```css
:root[data-theme="horizon-progres"] {
  /* === BACKGROUNDS === */
  --bg-primary: #0a0a0a;
  --bg-secondary: #0f0f1a;
  --bg-tertiary: #1a1a2d;
  --bg-elevated: #252540;

  /* === ACCENTS === */
  --accent-primary: #1e1e3d;
  --accent-secondary: #7a6aa8;
  --accent-tertiary: #5a4a88;

  /* === TEXTE === */
  --text-primary: #c8c0d8;
  --text-secondary: #9888b8;
  --text-accent: #7a6aa8;
  --text-muted: #6a5a88;

  /* === ÉTATS === */
  --border-color: #7a6aa8;
  --border-subtle: #252540;
  --alert-color: #a85a6a;
  --warning-color: #b88a70;
  --success-color: #6a9a7a;
  --info-color: #6a7aa8;

  /* === INTERACTIONS === */
  --hover-overlay: rgba(122, 106, 168, 0.1);
  --active-overlay: rgba(122, 106, 168, 0.2);
  --focus-ring: #7a6aa8;
}
```

### Optimisation OLED

**Couleurs évitées pour économie énergie** :
- ❌ Bleu pur (`#0000FF`) : Consommation maximale sur OLED
- ❌ Couleurs saturées vives : Pixels OLED à intensité maximale
- ❌ Blanc pur (`#FFFFFF`) : 100% consommation tous sous-pixels

**Couleurs privilégiées** :
- ✅ Noir pur (`#000000`) : 0% consommation (pixels éteints)
- ✅ Gris sombres (`#0a0a0a`, `#1a1a1a`) : <5% consommation
- ✅ Couleurs désaturées (`#cc7000` vs `#ff8c00`) : -30% consommation
- ✅ Verts terrestres (`#6b8e23`, `#2d5016`) : Consommation optimale

### Valeurs et Signification des Thèmes

| Thème | Valeur | Couleurs dominantes | Symbolisme |
|-------|--------|---------------------|------------|
| **Nuit Forêt** | Éco-responsabilité | Verts terrestres (#6b8e23) | Nature, durabilité, économie d'énergie OLED |
| **Terre Éthique** | Éthique et transparence | Bruns et verts doux (#7c9d6f, #d4c5b0) | Ancrage moral, solidité, authenticité |
| **Cryptage Nocturne** | Sécurité des données | Gris-bleus acier (#5a7a8a) | Protection, confidentialité, cryptographie |
| **Aurore Humaine** | IA pour les humains | Oranges chauds doux (#b8956a) | Humanité, empathie, chaleur |
| **Horizon Progrès** | Innovation et progrès | Violets profonds (#7a6aa8) | Futur, innovation, vision |

### Implémentation du Sélecteur de Thèmes

#### HTML - Boutons de sélection (dans le header)

```html
<div class="theme-selector">
  <span class="theme-selector-label">Thème:</span>
  <button class="theme-btn active" data-theme="nuit-foret" title="Nuit Forêt"></button>
  <button class="theme-btn" data-theme="terre-ethique" title="Terre Éthique"></button>
  <button class="theme-btn" data-theme="cryptage-nocturne" title="Cryptage Nocturne"></button>
  <button class="theme-btn" data-theme="aurore-humaine" title="Aurore Humaine"></button>
  <button class="theme-btn" data-theme="horizon-progres" title="Horizon Progrès"></button>
</div>
```

#### CSS - Styles des boutons de thèmes

```css
.theme-selector {
  display: flex;
  gap: 8px;
  align-items: center;
}

.theme-selector-label {
  color: var(--text-secondary);
  font-size: 11px;
  margin-right: 5px;
}

.theme-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.theme-btn:hover {
  transform: scale(1.1);
  border-color: var(--text-primary);
}

.theme-btn.active {
  border-color: var(--text-primary);
  box-shadow: 0 0 8px var(--border-color);
}

.theme-btn[data-theme="nuit-foret"] {
  background: linear-gradient(135deg, #0a0a0a 0%, #6b8e23 100%);
}

.theme-btn[data-theme="terre-ethique"] {
  background: linear-gradient(135deg, #1a1512 0%, #7c9d6f 100%);
}

.theme-btn[data-theme="cryptage-nocturne"] {
  background: linear-gradient(135deg, #0f1419 0%, #5a7a8a 100%);
}

.theme-btn[data-theme="aurore-humaine"] {
  background: linear-gradient(135deg, #1a140f 0%, #b8956a 100%);
}

.theme-btn[data-theme="horizon-progres"] {
  background: linear-gradient(135deg, #0f0f1a 0%, #7a6aa8 100%);
}
```

#### JavaScript - Gestion des thèmes

```javascript
// Charger thème sauvegardé au démarrage
loadTheme() {
  const savedTheme = localStorage.getItem('theme') || 'nuit-foret';
  document.documentElement.setAttribute('data-theme', savedTheme);

  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.theme === savedTheme);
  });
}

// Changer de thème
setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);

  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });

  // Si graphiques Chart.js présents, les mettre à jour
  if (typeof this.updateChartsColors === 'function') {
    this.updateChartsColors();
  }
}

// Configurer les événements
setupThemeSelector() {
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      this.setTheme(btn.dataset.theme);
    });
  });
}
```

### Utilisation

| Élément | Couleur | Variable |
|---------|---------|----------|
| Body background | #0a0a0a | `var(--bg-primary)` |
| Containers | #1a1a1a | `var(--bg-secondary)` |
| Cards | #2d2d2d | `var(--bg-tertiary)` |
| Cards hover | #3a3a3a | `var(--bg-elevated)` |
| Header | #2d5016 | `var(--accent-primary)` |
| Texte principal | #b8b8b8 | `var(--text-primary)` |
| Texte secondaire | #8a8a8a | `var(--text-secondary)` |
| Texte accent | #6b8e23 | `var(--text-accent)` |
| Texte désactivé | #6a6a6a | `var(--text-muted)` |
| Bordures principales | #6b8e23 | `var(--border-color)` |
| Bordures subtiles | #3a3a3a | `var(--border-subtle)` |
| Boutons primaires | #6b8e23 | `var(--accent-secondary)` |
| Erreurs | #8b4513 | `var(--alert-color)` |
| Avertissements | #cc7000 | `var(--warning-color)` |
| Succès | #6b8e23 | `var(--success-color)` |
| Informations | #5a7a8a | `var(--info-color)` |

## Typographie

### Police

**Famille** : `'Consolas', 'Monaco', 'Courier New', monospace`

**Raison** : Police monospace système, disponible partout, excellente lisibilité

### Tailles

| Élément | Taille | Usage |
|---------|--------|-------|
| Body | 14px | Texte standard |
| Header h1 | 20px | Titre principal |
| h2 | 18px | Titres sections |
| h3 | 16px | Sous-titres |
| Stats label | 11px | Labels statistiques |
| Stats value | 16px | Valeurs statistiques |
| Metric value | 32px | Grandes valeurs |
| Footer | 11px | Footer fixe |
| Boutons | 14px | Tous boutons |
| Tableaux th | 12px | En-têtes tableaux |

## Composants Standards

### Header

```
├── Background: #2d5016
├── Border bottom: 2px solid #6b8e23
├── Padding: 15px 20px
└── Layout: flex, space-between
```

### Navigation

```
├── Background: #4a4a4a
├── Border bottom: 1px solid #6b8e23
├── Padding: 10px 20px
└── Buttons:
    ├── Hover: #2d5016
    └── Active: #2d5016 + border-bottom #6b8e23
```

### Main

```
├── Flex: 1
├── Padding: 30px
├── Padding-bottom: 60px (pour footer)
└── Overflow-y: auto
```

### Footer

```
├── Position: fixed bottom right
├── Background: #2d2d2d
├── Color: #6b8e23
├── Font-size: 11px
├── Padding: 10px 20px
├── Border-top-left-radius: 5px
├── Border: 1px solid #6b8e23 (top + left)
└── Format: "@Je Geek Utile - DD/MM/YYYY - [NOM] v[VERSION]"
```

### Cards

```
├── Background: #4a4a4a
├── Padding: 20px
├── Border-radius: 8px
├── Border: 2px solid #6b8e23
└── Hover:
    ├── Border-color: #6b8e23
    └── Box-shadow: 0 4px 12px rgba(107, 142, 35, 0.2)
```

### Boutons

**Primaire**
```
├── Background: #6b8e23
├── Color: #1a1a1a
├── Padding: 12px 30px
├── Border-radius: 5px
└── Hover: background #2d5016, color #b8b8b8
```

**Secondaire**
```
├── Background: #4a4a4a
├── Color: #b8b8b8
├── Border: 1px solid #6b8e23
├── Padding: 8px 20px
└── Hover: background #2d5016
```

**Danger**
```
├── Background: #8b4513
├── Color: #b8b8b8
├── Padding: 6px 15px
└── Hover: background #a0522d
```

### Formulaires

**Input/Select**
```
├── Background: #2d2d2d
├── Color: #b8b8b8
├── Border: 1px solid #6b8e23
├── Padding: 10px
└── Focus: border-color #b8b8b8
```

**Label**
```
├── Color: #6b8e23
├── Font-size: 13px
└── Margin-bottom: 8px
```

### Tableaux

**Thead**
```
├── Background: #2d5016
├── Color: #6b8e23
├── Padding: 12px
├── Font-size: 12px
└── Text-transform: uppercase
```

**Tbody td**
```
├── Padding: 12px
├── Border-bottom: 1px solid #2d2d2d
└── Hover row: background #2d2d2d
```

### Notifications

```
├── Position: fixed bottom 60px, right 20px
├── Background: #2d5016
├── Color: #b8b8b8
├── Padding: 15px 25px
├── Border: 2px solid #6b8e23
├── Border-radius: 5px
├── Z-index: 1000
└── Types:
    ├── Success: border #6b8e23
    └── Error: border #8b4513, background #4a4a4a
```

## Grilles

### Grid 2 colonnes
```css
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
gap: 20px;
```

### Grid 3 colonnes
```css
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 20px;
```

### Grid 4 colonnes
```css
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
gap: 20px;
```

## Accessibilité (WCAG 2.1)

### Ratios de Contraste

| Combinaison | Ratio | Niveau |
|-------------|-------|--------|
| `#b8b8b8` sur `#0a0a0a` | 11.2:1 | AAA |
| `#8a8a8a` sur `#0a0a0a` | 6.8:1 | AA |
| `#6a6a6a` sur `#0a0a0a` | 4.7:1 | AA (large) |
| `#6b8e23` sur `#0a0a0a` | 5.1:1 | AA |
| `#6b8e23` sur `#2d2d2d` | 3.2:1 | AA (large uniquement) |

**Règle** : Minimum 4.5:1 pour texte standard, 3:1 pour texte large (≥18px)

### Focus Visible

**Obligatoire** : Indicateur focus de 2px minimum
```css
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

### Zones Tactiles

**Minimum** : 44×44px pour éléments cliquables (boutons, liens)

## Mode Sombre Éco-responsable

### Objectifs

- **Pixels noirs** : > 70% (pixels éteints sur OLED)
- **Pixels blancs** : < 3% (réduit de 5% → 3%)
- **Consommation électrique** : -40% vs mode clair
- **Confort visuel** : Contraste optimal sans éblouissement
- **Cohérence** : Toutes applications identiques

### Métriques Énergétiques

| Métrique | Valeur | Gain vs Clair |
|----------|--------|---------------|
| Pixels noirs (OLED éteints) | > 70% | -70% consommation |
| Pixels blancs | < 3% | -97% pixels énergivores |
| Luminosité moyenne | < 15% | -85% luminosité |
| Contraste texte | > 4.5:1 | WCAG AA minimum |
| Backgrounds sombres | 100% | Optimal OLED |
| Couleurs saturées évitées | 100% | -30% consommation couleurs |

### Économies Mesurables

1. **OLED/AMOLED** : -60% à -70% consommation écran
2. **LCD** : -20% à -30% consommation rétroéclairage
3. **Fatigue oculaire** : -40% en environnement sombre
4. **Autonomie batterie** : +2h à +4h sur appareil mobile

### Avantages

1. **Économie énergie** : Jusqu'à 70% sur OLED
2. **Confort visuel** : Réduction fatigue oculaire significative
3. **Esthétique** : Design professionnel moderne
4. **Cohérence** : Identité visuelle forte
5. **Environnement** : Réduction empreinte carbone globale

## Performance et Animations

### Règles Animations

**À ÉVITER** (consommation CPU/GPU inutile) :
- ❌ Animations perpétuelles (spinners continus)
- ❌ Transitions > 300ms
- ❌ Animations sur `width`, `height`, `top`, `left`
- ❌ `box-shadow` animées
- ❌ Effets de parallaxe complexes

**PRÉFÉRER** (optimisé GPU) :
- ✅ `transform` et `opacity` uniquement
- ✅ Transitions ≤ 200ms
- ✅ `will-change` sur éléments animés uniquement
- ✅ Animations déclenchées par interaction (pas auto)
- ✅ `prefers-reduced-motion` respecté

### Exemple Optimisé

```css
/* ✅ BIEN */
.bouton {
  transition: transform var(--transition-fast),
              opacity var(--transition-fast);
}

.bouton:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

/* ❌ MAL */
.bouton {
  transition: all 500ms;
  animation: pulse 2s infinite;
}

/* ✅ Respecter préférences utilisateur */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Lazy Loading

**Images** : Charger uniquement visibles
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

**JavaScript** : Modules chargés à la demande
```javascript
// Charger uniquement si nécessaire
if (condition) {
  import('./module-lourd.js').then(module => {
    module.init();
  });
}
```

## Règles d'Application

### À FAIRE

✓ Toujours utiliser les variables CSS
✓ Respecter la palette exacte
✓ Footer obligatoire en bas à droite
✓ Police monospace système
✓ Mode sombre partout
✓ Pixels blancs < 5%

### À NE PAS FAIRE

✗ Utiliser des couleurs hors palette
✗ Changer la police
✗ Mode clair
✗ Footer ailleurs qu'en bas à droite
✗ Pixels blancs > 5%
✗ Frameworks CSS externes

## Validation

### Checklist Application

**Design** :
- [ ] Variables CSS complètes importées
- [ ] Système de 5 thèmes configurés (Nuit Forêt, Terre Éthique, Cryptage Nocturne, Aurore Humaine, Horizon Progrès)
- [ ] Sélecteur de thèmes dans le header avec boutons visuels
- [ ] Persistance du thème via localStorage
- [ ] Footer avec format `@Je Geek Utile - DD/MM/YYYY - Nom v1.0`
- [ ] Police système monospace (Consolas/Monaco)
- [ ] Background principal `#0a0a0a` minimum
- [ ] Pixels noirs > 70%
- [ ] Pixels blancs < 3%
- [ ] Pas de blanc pur (`#fff`), bleu pur (`#00f`), couleurs saturées

**Accessibilité** :
- [ ] Contraste texte ≥ 4.5:1 (AA minimum)
- [ ] Focus visible 2px sur tous éléments interactifs
- [ ] Zones cliquables ≥ 44×44px
- [ ] `alt` sur toutes images
- [ ] Labels sur tous inputs

**Performance** :
- [ ] Transitions ≤ 200ms
- [ ] Animations `transform`/`opacity` uniquement
- [ ] `@media (prefers-reduced-motion)` implémenté
- [ ] Images en `loading="lazy"`
- [ ] Pas d'animations infinies
- [ ] JavaScript modules chargés à la demande

**Responsive** :
- [ ] Grids `auto-fit`/`auto-fill`
- [ ] Mobile-first (breakpoints si nécessaire)
- [ ] Pas de scroll horizontal

**Code** :
- [ ] Pas de frameworks CSS externes
- [ ] CSS vanilla avec variables
- [ ] JavaScript vanilla (pas de jQuery/React/etc)
- [ ] Fichiers séparés (HTML/CSS/JS)

## Exemples Visuels

### Combinaisons Valides

```
✓ Background #1a1a1a + Texte #b8b8b8
✓ Background #4a4a4a + Texte #6b8e23
✓ Background #2d5016 + Texte #b8b8b8
✓ Border #6b8e23 sur background #4a4a4a
```

### Combinaisons Invalides

```
✗ Background blanc
✗ Texte noir pur
✗ Couleurs arc-en-ciel
✗ Dégradés complexes
```

## Contact

Questions ou suggestions sur la charte : Voir documentation projet

---

**Charte Graphique** : v2.0
**Date** : 22/12/2025
**Auteur** : @Je Geek Utile
**Nouveautés v2.0** : Système de 5 thèmes configurables représentant les valeurs du projet
