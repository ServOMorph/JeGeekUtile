# Prompts DALL-E — Bannières d'en-tête des pages

Générer les 3 images dans l'ordre ci-dessous.
Valider chaque image avant de passer à la suivante.
Dimensions : **1200x300px** (ratio 4:1) — format bannière d'en-tête de page.

**IMPORTANT : fournir le logo `logo_transparentr_1.png` comme image de référence de style à chaque génération.**

---

## IMAGE 1 — "Notre projet"

```
In the exact same illustration style as the reference image: same characters (elderly grandmother with round glasses and young boy), same color treatment, same soft rounded shapes, same warm glow quality, same background dark tone — wide panoramic banner composition, the duo mascot visible on the right side at smaller scale, left side features the text "Notre projet" written in very large clean rounded sans-serif white font, very bold, highly prominent, soft cloud-blue #A5D8FF glow behind the text, same background dark tone as reference, small floating icons (lightbulb, gear, leaf) scattered around, ultra-wide 4:1 banner format
```

**Prompt négatif :**
```
photorealistic, 3D render, anime, manga, different art style than reference, harsh shadows, neon cyberpunk, serif font, gradients dominant, brown or red tones, white background, square format
```

Paramètres : ratio 4:1 — Style identique à l'image de référence fournie
**Destination :** `site internet/static/images/banners/banner-notre-projet.png`

---

✅ VALIDER IMAGE 1 avant de continuer

---

## IMAGE 2 — "Nos 6 Piliers"

```
In the exact same illustration style and color palette as the reference image: same warm glow quality, same soft rounded shapes, same background dark tone — wide panoramic banner composition, left side features the text "Nos 6 Piliers" written in very large clean rounded sans-serif white font, very bold, highly prominent, soft cloud-blue #A5D8FF glow behind the text, right side shows six small glowing icons arranged in two rows of three: leaf, joined hands, brain+heart, open book, compass, megaphone — each icon in cloud-blue #A5D8FF and leaf green #5CD197, ultra-wide 4:1 banner format
```

**Prompt négatif :**
```
photorealistic, 3D render, anime, manga, different art style than reference, harsh shadows, neon cyberpunk, serif font, gradients dominant, human figures, brown or red tones, white background, square format
```

Paramètres : ratio 4:1 — Style identique à l'image de référence fournie
**Destination :** `site internet/static/images/banners/banner-nos-6-piliers.png`

---

✅ VALIDER IMAGE 2 avant de continuer

---

## IMAGE 3 — "Rejoignez-nous" *(optionnel)*

```
In the exact same illustration style as the reference image: same characters (elderly grandmother with round glasses and young boy), same color treatment, same soft rounded shapes, same warm glow quality, same background dark tone — wide panoramic banner composition, the duo mascot on the right side with arms open in a welcoming gesture, left side features the text "Rejoignez-nous" written in very large clean rounded sans-serif white font, very bold, highly prominent, soft leaf green #5CD197 glow behind the text, ultra-wide 4:1 banner format
```

**Prompt négatif :**
```
photorealistic, 3D render, anime, manga, different art style than reference, harsh shadows, neon cyberpunk, serif font, gradients dominant, brown or red tones, white background, square format
```

Paramètres : ratio 4:1 — Style identique à l'image de référence fournie
**Destination :** `site internet/static/images/banners/banner-rejoignez-nous.png`

---

✅ VALIDER IMAGE 3

---

## IMAGE 4 — "Qui sommes nous ?"

```
In the exact same illustration style as the reference image: same characters (elderly grandmother with round glasses and young boy), same color treatment, same soft rounded shapes, same warm glow quality, same background dark tone — wide panoramic banner composition, the duo mascot visible on the right side at smaller scale, both looking toward the viewer in a welcoming pose, left side features the text "Qui sommes nous ?" written in very large clean rounded sans-serif white font, very bold, highly prominent, soft cloud-blue #A5D8FF glow behind the text, ultra-wide 4:1 banner format
```

**Prompt négatif :**
```
photorealistic, 3D render, anime, manga, different art style than reference, harsh shadows, neon cyberpunk, serif font, gradients dominant, brown or red tones, white background, square format
```

Paramètres : ratio 4:1 — Style identique à l'image de référence fournie
**Destination :** `site internet/static/images/banners/banner-qui-sommes-nous.png`

---

✅ VALIDER IMAGE 4

---

## IMAGE 5 — "Projet d'actions"

```
In the exact same illustration style as the reference image: same characters (elderly grandmother with round glasses and young boy), same color treatment, same soft rounded shapes, same warm glow quality, same background dark tone — wide panoramic banner composition, the duo mascot visible on the right side at smaller scale, the grandmother pointing enthusiastically toward the left, the boy holding a small glowing checklist, left side features the text "Projet d'actions" written in very large clean rounded sans-serif white font, very bold, highly prominent, soft leaf green #5CD197 glow behind the text, small floating icons scattered around (gamepad, brain, microphone) in cloud-blue #A5D8FF and leaf green #5CD197, ultra-wide 4:1 banner format
```

**Prompt négatif :**
```
photorealistic, 3D render, anime, manga, different art style than reference, harsh shadows, neon cyberpunk, serif font, gradients dominant, brown or red tones, white background, square format
```

Paramètres : ratio 4:1 — Style identique à l'image de référence fournie
**Destination :** `site internet/static/images/banners/banner-projet-d-actions.png`

---

✅ VALIDER IMAGE 5

---

## Intégration site

Une fois les images validées, créer le dossier et y placer les fichiers :
```
site internet/static/images/banners/
├── banner-notre-projet.png
├── banner-nos-6-piliers.png
└── banner-rejoignez-nous.png   (optionnel)
```

Dans `notre_projet.html`, remplacer le `<h1>` par :
```html
<img src="{{ url_for('static', filename='images/banners/banner-notre-projet.png') }}" alt="Notre projet" class="page-banner">
```

Ajouter en CSS :
```css
.page-banner { width: 100%; height: auto; border-radius: var(--radius-md); margin-bottom: var(--space-xl); }
```

*Charte de référence : CHARTE_GRAPHIQUE_FamiCLouD.md v2.0*
*Date : 2026-02-25*
