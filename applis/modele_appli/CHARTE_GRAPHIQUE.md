# Charte Graphique - Je Geek Utile

Charte graphique standardisée pour toutes les applications du projet.

## Palette Couleurs

### Variables CSS

```css
:root {
  --bg-primary: #1a1a1a;        /* Background principal */
  --bg-secondary: #2d2d2d;      /* Background secondaire */
  --bg-tertiary: #4a4a4a;       /* Background tertiaire */
  --accent-primary: #2d5016;    /* Accent vert foncé */
  --accent-secondary: #6b8e23;  /* Accent vert clair */
  --text-primary: #b8b8b8;      /* Texte principal */
  --text-secondary: #6b8e23;    /* Texte secondaire */
  --border-color: #6b8e23;      /* Bordures */
  --alert-color: #8b4513;       /* Alertes */
  --warning-color: #ff8c00;     /* Avertissements */
}
```

### Utilisation

| Élément | Couleur | Variable |
|---------|---------|----------|
| Body background | #1a1a1a | `var(--bg-primary)` |
| Cards, containers | #4a4a4a | `var(--bg-tertiary)` |
| Header | #2d5016 | `var(--accent-primary)` |
| Texte principal | #b8b8b8 | `var(--text-primary)` |
| Texte accent | #6b8e23 | `var(--text-secondary)` |
| Bordures | #6b8e23 | `var(--border-color)` |
| Boutons primaires | #6b8e23 | `var(--accent-secondary)` |
| Erreurs | #8b4513 | `var(--alert-color)` |
| Avertissements | #ff8c00 | `var(--warning-color)` |

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

## Mode Sombre Éco-responsable

### Objectifs

- **Pixels blancs** : < 5%
- **Consommation électrique** : Minimale
- **Confort visuel** : Optimal
- **Cohérence** : Toutes applications

### Métriques

| Métrique | Valeur | Objectif |
|----------|--------|----------|
| Pixels blancs | < 5% | ✓ |
| Luminosité moyenne | < 20% | ✓ |
| Contraste texte | > 4.5:1 | ✓ |
| Backgrounds sombres | 100% | ✓ |

### Avantages

1. **Économie énergie** : Écrans OLED/AMOLED économisent jusqu'à 60%
2. **Confort visuel** : Réduction fatigue oculaire
3. **Esthétique** : Look professionnel
4. **Cohérence** : Identité visuelle forte

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

- [ ] Variables CSS importées
- [ ] Footer avec date + version
- [ ] Police Consolas/Monaco
- [ ] Tous backgrounds sombres
- [ ] Pixels blancs < 5%
- [ ] Bordures #6b8e23
- [ ] Boutons standards
- [ ] Notifications positionnées
- [ ] Responsive (grids auto)
- [ ] Pas de blanc pur (#fff)

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

**Charte Graphique** : v1.0
**Date** : 26/11/2025
**Auteur** : @Je Geek Utile
