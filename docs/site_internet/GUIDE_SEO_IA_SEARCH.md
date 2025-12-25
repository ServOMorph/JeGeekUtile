# Guide Complet : Concevoir un Site Web Optimise pour le SEO Classique et les Recherches IA

**Version** : 2.1
**Date** : Decembre 2025
**Base sur** : Analyse du site SereniaTech (serenia-tech.fr)

---

## Quick Start : Les 10 Actions Essentielles

> **Pour les devs presses** : Si vous ne faites que 10 choses, faites celles-ci.

### SEO Classique (5 actions)
1. **Title unique** par page (50-60 car.) avec mot-cle principal
2. **Meta description** engageante (150-160 car.)
3. **URL canonique** sur chaque page
4. **Hierarchie H1 > H2 > H3** sans sauter de niveau
5. **Schema.org Organization** + sitemap.xml soumis

### Optimisation IA (3 actions)
6. **Contenu factuel explicite** : prix, zones, durees des le debut de page
7. **FAQ avec questions naturelles** ("Combien coute...", "Comment fonctionne...")
8. **Page A propos** detaillee avec E-E-A-T (experience, certifications, temoignages)

### Performance (2 actions)
9. **Images WebP** avec `width`, `height` et `loading="lazy"`
10. **CSS critique inline** + JS en `defer`

**Resultat attendu** : LCP < 2.5s, PageSpeed > 90, site indexable par moteurs classiques ET agents IA.

---

## Table des Matieres

1. [Introduction et Philosophie](#1-introduction-et-philosophie)
2. [Fondamentaux du SEO Classique](#2-fondamentaux-du-seo-classique)
3. [Optimisation pour les Systemes de Recherche IA](#3-optimisation-pour-les-systemes-de-recherche-ia)
4. [Structure HTML Optimale](#4-structure-html-optimale)
5. [Donnees Structurees Schema.org](#5-donnees-structurees-schemaorg)
6. [Fichiers Techniques Essentiels](#6-fichiers-techniques-essentiels)
7. [Performance et Core Web Vitals](#7-performance-et-core-web-vitals)
8. [Accessibilite et UX](#8-accessibilite-et-ux)
9. [Securite et Headers HTTP](#9-securite-et-headers-http)
10. [Gestion Multi-langue](#10-gestion-multi-langue)
11. [Ressources Tierces et RGPD](#11-ressources-tierces-et-rgpd)
12. [Checklists Operationnelles](#12-checklists-operationnelles)
13. [Exemples de Code](#13-exemples-de-code)

---

## 1. Introduction et Philosophie

### 1.1 Contexte 2025

Le paysage de la recherche web evolue avec deux ecosystemes distincts :

**Moteurs de recherche traditionnels :**
- Google, Bing, Yahoo, DuckDuckGo, Lilo, Qwant
- Fonctionnement : crawling, indexation, ranking algorithmique

**Systemes de recherche IA :**
- **Agents IA generatifs** : ChatGPT (OpenAI), Claude (Anthropic), Perplexity, You.com
- **IA integrees aux SERP** : Google SGE (Search Generative Experience), Bing Copilot
- **Assistants vocaux** : Google Assistant, Siri, Alexa
- Fonctionnement : comprehension semantique, extraction d'informations, synthese

### 1.2 Differences Cles entre IA Generatives et IA SERP

| Aspect | IA Generatives (ChatGPT, Claude) | IA SERP (Google SGE, Bing Copilot) |
|--------|----------------------------------|-------------------------------------|
| Source | Crawling propre ou partenariats | Index du moteur de recherche |
| Affichage | Reponse synthetisee | Encart dans les resultats |
| Citation | Variable selon le modele | Lien vers source obligatoire |
| Optimisation | Contenu clair, structure, E-E-A-T | SEO classique + donnees structurees |

### 1.3 Philosophie "IA-First"

```
+------------------+     +-------------------+     +----------------------+
|  CONTENU BRUT    | --> | STRUCTURE HTML5   | --> | DONNEES STRUCTUREES  |
|  (texte, images) |     | (semantique)      |     | (Schema.org JSON-LD) |
+------------------+     +-------------------+     +----------------------+
                                                              |
                                                              v
+------------------+     +-------------------+     +----------------------+
| VERIFICATION     | <-- | ACCESSIBILITE     | <-- | RESUME EXPLICITE     |
| (perf, validite) |     | (ARIA, contrastes)|     | (visible, coherent)  |
+------------------+     +-------------------+     +----------------------+
```

> **Principe fondamental** : Un site optimise pour les agents IA sera naturellement optimise pour le SEO classique. L'inverse n'est pas toujours vrai.

### 1.4 E-E-A-T : Le Signal de Confiance

**E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness) est essentiel pour les deux ecosystemes :

| Signal | Implementation |
|--------|----------------|
| **Experience** | Etudes de cas, temoignages clients, portfolio |
| **Expertise** | Certifications, diplomes, annees d'experience |
| **Autorite** | Mentions presse, liens entrants, profils sociaux pro |
| **Fiabilite** | HTTPS, mentions legales, politique confidentialite |

**Pages essentielles pour E-E-A-T :**
- Page "A propos" detaillee avec parcours
- Page "Auteur" pour les blogs
- Temoignages verifiables
- Liens vers LinkedIn, profils professionnels

> **Note 2025** : Les contenus bases sur une vraie experience humaine et un auteur identifiable se distinguent du contenu genere de maniere generique. Privilegiez les etudes de cas reelles, les chiffres verifiables et les temoignages authentiques.

### 1.5 Principe "People-First Content"

Google et les agents IA privilegient le contenu utile aux utilisateurs, pas le contenu optimise pour les robots :

| A faire | A eviter |
|---------|----------|
| Repondre completement a l'intention de recherche | Creer du contenu juste pour attirer du trafic |
| Donner des infos factuelles (prix, durees, specs) | Rester vague avec du marketing creux |
| Citer ses sources, montrer son expertise | Repeter les memes mots-cles sans valeur ajoutee |
| Intro de 2-3 phrases avec les infos cles | Paragraphes d'intro sans substance |
| Transparence sur l'auteur et l'entreprise | Anonymat ou manque de contexte |

---

## 2. Fondamentaux du SEO Classique

### 2.1 Meta Tags Essentiels

Chaque page doit contenir ces meta tags dans le `<head>` :

```html
<!-- Titre de la page (50-60 caracteres) -->
<title>Titre Principal - Marque | Mot-cle</title>

<!-- Description (150-160 caracteres) -->
<meta name="description" content="Description concise et attractive avec mots-cles principaux.">

<!-- URL Canonique (evite le contenu duplique) -->
<link rel="canonical" href="https://exemple.fr/page-exacte">
```

> **Note sur `meta keywords`** : Cette balise n'est plus utilisee par Google pour le ranking depuis 2009. Elle peut etre conservee pour d'autres moteurs ou comme documentation interne, mais n'a aucun impact SEO sur Google/Bing.

### 2.2 Open Graph (Reseaux Sociaux)

```html
<meta property="og:title" content="Titre pour partage social">
<meta property="og:description" content="Description pour le partage">
<meta property="og:type" content="website">
<meta property="og:url" content="https://exemple.fr/page">
<meta property="og:image" content="https://exemple.fr/image-og.png">
<meta property="og:locale" content="fr_FR">
```

### 2.3 Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Titre Twitter">
<meta name="twitter:description" content="Description Twitter">
```

### 2.4 Hierarchie des Titres

Structure semantique imperative :

```
H1 (unique par page) - Titre principal
+-- H2 - Section principale 1
|   +-- H3 - Sous-section
|   +-- H3 - Sous-section
+-- H2 - Section principale 2
|   +-- H3 - Sous-section
|   |   +-- H4 - Detail
|   +-- H3 - Sous-section
+-- H2 - Section principale 3
```

**Regles :**
- Un seul H1 par page
- Ne jamais sauter de niveau (H1 -> H3 interdit)
- Utiliser les titres pour la structure, pas le style

---

## 3. Optimisation pour les Systemes de Recherche IA

### 3.1 Strategies selon le Type d'IA

#### Pour les Agents IA Generatifs (ChatGPT, Claude, Perplexity)

Ces systemes analysent le contenu pour repondre aux questions des utilisateurs :

- **Contenu factuel explicite** : prix, zones, durees, specifications
- **Structure claire** : listes, tableaux, FAQ
- **Informations de contact** : facilement identifiables
- **E-E-A-T visible** : credentials, experience, temoignages

#### Pour les IA Integrees aux SERP (Google SGE, Bing Copilot)

Ces systemes s'appuient sur l'index existant :

- **SEO classique solide** : toutes les bases doivent etre en place
- **Donnees structurees** : Schema.org impeccable
- **Reponses directes** : sections FAQ, definitions claires
- **Fraicheur du contenu** : dates de mise a jour visibles

### 3.2 Conventions Internes (Non-Standards)

> **AVERTISSEMENT** : Les balises suivantes sont des conventions internes qui ne sont PAS reconnues par les moteurs de recherche (Google, Bing). Elles peuvent etre utiles comme documentation ou pour des outils internes, mais n'ont aucun impact SEO direct.

```html
<!-- Convention interne : variantes de description (NON STANDARD) -->
<!-- Utile pour A/B testing ou documentation, pas pour le SEO -->
<meta name="description-variant-1" content="Variante alternative...">

<!-- Convention interne : resume pour agents IA (NON STANDARD) -->
<!-- Les agents IA lisent le contenu visible, pas ces meta -->
<meta name="ai-summary" content="Resume explicite...">
```

**Recommandation** : Privilegier le contenu visible et structure plutot que ces meta custom.

### 3.3 Resume Accessible pour Agents IA et Lecteurs d'Ecran

Ajouter des blocs de resume qui sont :
- **Invisibles visuellement** mais accessibles aux technologies d'assistance
- **Coherents avec le contenu visible** (pas de mots-cles caches supplementaires)
- **Utiles pour les lecteurs d'ecran** et les agents IA

```html
<!-- Utiliser une classe CSS standard plutot que des styles inline -->
<div class="visually-hidden">
    <h2>Resume de la page</h2>
    <p>Cette page presente [reprise exacte des informations visibles :
    services proposes, tarifs affiches, zone d'intervention, public cible].
    Actions possibles : [CTA visibles sur la page].</p>
</div>
```

**Classe CSS standard (a ajouter dans votre feuille de style) :**

```css
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    border: 0;
    clip: rect(0 0 0 0);
    overflow: hidden;
    white-space: nowrap;
}
```

> **ATTENTION** : Le contenu de ces blocs doit etre IDENTIQUE aux informations visibles sur la page. Tout texte cache contenant des mots-cles supplementaires peut etre considere comme du "hidden text" par Google et penaliser le site.

### 3.4 Intro Factuelle en Debut de Page

Pour aider les agents IA a extraire rapidement l'essentiel, commencez chaque page par un resume factuel de 2-3 phrases :

```html
<article>
    <h1>Formation IA pour Entreprises</h1>

    <!-- Intro factuelle immediate (visible, pas cachee) -->
    <p class="intro">
        <strong>Formations IA professionnelles de 900 EUR a 4 300 EUR</strong>,
        disponibles en intra-entreprise ou inter-entreprises.
        Duree : demi-journee a 3 jours. Zone : France entiere.
        Eligible financement OPCO.
    </p>

    <!-- Suite du contenu... -->
</article>
```

**Regles pour l'intro factuelle :**
- Placer en haut de page, **visible** (pas dans un bloc cache)
- Inclure les infos cles : prix, duree, zone, public cible
- Eviter le marketing vague ("leader du marche", "solution innovante")
- Maximum 3 phrases

### 3.5 Optimisation pour la Recherche Vocale et Conversationnelle

Les assistants vocaux et les agents IA privilegient les reponses directes aux questions naturelles.

**Structure FAQ optimisee :**

```html
<section aria-labelledby="faq-title">
    <h2 id="faq-title">Questions frequentes</h2>

    <dl>
        <!-- Questions naturelles / conversationnelles -->
        <dt>Combien coute une formation IA ?</dt>
        <dd>Nos formations IA coutent entre 900EUR et 4300EUR selon la duree
            (demi-journee a 3 jours) et le format (intra ou inter-entreprise).</dd>

        <dt>En combien de temps obtiendra-t-on des resultats ?</dt>
        <dd>Les premiers resultats sont visibles en 2 a 4 semaines pour
            l'accompagnement, et le ROI des automatisations est generalement
            atteint en 3 a 6 mois.</dd>

        <dt>Qui peut beneficier de vos services ?</dt>
        <dd>Nos services s'adressent aux particuliers, PME, associations et
            collectivites partout en France, en presentiel ou a distance.</dd>
    </dl>
</section>
```

**Types de questions a couvrir :**
- Prix / cout ("Combien coute...")
- Duree ("En combien de temps...")
- Eligibilite ("Qui peut...")
- Localisation ("Ou intervenez-vous...")
- Processus ("Comment fonctionne...")

### 3.6 Liaison Donnees Structurees <-> Contenu Visible

**Regle absolue** : Chaque element declare en Schema.org JSON-LD DOIT correspondre a un contenu visible sur la page.

```html
<!-- CORRECT : Le service est visible sur la page -->
<script type="application/ld+json">
{
    "@type": "Service",
    "name": "Formation IA",           <!-- Visible en H3 -->
    "description": "Formation...",    <!-- Visible en paragraphe -->
    "offers": {
        "priceRange": "900EUR-4300EUR" <!-- Visible dans section tarifs -->
    }
}
</script>

<!-- INCORRECT : Service declare mais non visible -->
<!-- Risque de non-prise en compte par Google -->
```

---

## 4. Structure HTML Optimale

### 4.1 Template de Page Complet

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Theme color mobile -->
    <meta name="theme-color" content="#couleur-principale">

    <!-- URL Canonique -->
    <link rel="canonical" href="https://domaine.fr/page">

    <!-- SEO -->
    <title>Titre Page - Marque</title>
    <meta name="description" content="Description principale optimisee">

    <!-- Open Graph -->
    <meta property="og:title" content="Titre OG">
    <meta property="og:description" content="Description OG">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://domaine.fr/page">
    <meta property="og:image" content="https://domaine.fr/og-image.png">
    <meta property="og:locale" content="fr_FR">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Titre Twitter">
    <meta name="twitter:description" content="Description Twitter">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Nom"
    }
    </script>

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">

    <!-- Preload ressources critiques -->
    <link rel="preload" href="/css/main.min.css" as="style">

    <!-- Polices -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- CSS critique inline + CSS principal -->
    <style>/* CSS critique above-the-fold */</style>
    <link rel="stylesheet" href="/css/main.min.css">
</head>
<body>
    <!-- Lien d'evitement accessibilite -->
    <a href="#main-content" class="skip-link">Aller au contenu principal</a>

    <!-- Navigation -->
    <nav aria-label="Navigation principale">
        <ul>
            <li><a href="/" aria-current="page">Accueil</a></li>
            <li><a href="/services">Services</a></li>
        </ul>
    </nav>

    <!-- Contenu principal -->
    <main id="main-content">
        <article>
            <h1>Titre principal</h1>
            <!-- Contenu structure -->
        </article>
    </main>

    <!-- Footer -->
    <footer>
        <!-- Informations legales, navigation secondaire -->
    </footer>

    <!-- JavaScript (defer) -->
    <script src="/js/main.min.js" defer></script>
</body>
</html>
```

### 4.2 Roles ARIA : Bonnes Pratiques

> **Regle generale** : Ne pas ajouter de `role` sur les elements HTML5 qui ont deja une semantique native.

**A EVITER (redondant) :**
```html
<!-- Ces roles sont implicites sur les elements HTML5 -->
<nav role="navigation">       <!-- nav a deja role=navigation -->
<main role="main">            <!-- main a deja role=main -->
<header role="banner">        <!-- header a deja role=banner -->
<footer role="contentinfo">   <!-- footer a deja role=contentinfo -->
<article role="article">      <!-- article a deja role=article -->
```

**CORRECT :**
```html
<!-- Pas de role redondant -->
<nav aria-label="Navigation principale">
<main id="main-content">
<header>
<footer>
<article>

<!-- Role necessaire uniquement sur div/span generiques -->
<div role="banner">...</div>  <!-- Si vous ne pouvez pas utiliser <header> -->
```

**Cas ou `role` est necessaire :**
```html
<!-- Menu applicatif reel (pas une navigation web simple) -->
<div role="menu" aria-label="Actions">
    <button role="menuitem">Action 1</button>
    <button role="menuitem">Action 2</button>
</div>

<!-- Alert dynamique -->
<div role="alert" aria-live="assertive">Message important</div>
```

### 4.3 Labels et Accessibilite

```html
<!-- Sections avec titres references -->
<section aria-labelledby="services-title">
    <h2 id="services-title">Nos services</h2>
</section>

<!-- Etat courant de navigation -->
<a href="/services" aria-current="page">Services</a>

<!-- Elements decoratifs -->
<img src="decoration.svg" alt="" aria-hidden="true">
<svg aria-hidden="true">...</svg>

<!-- Bouton avec label explicite -->
<button aria-label="Ouvrir le menu de navigation" aria-expanded="false">
    <span></span><span></span><span></span>
</button>
```

---

## 5. Donnees Structurees Schema.org

> **Documentation officielle** : [schema.org](https://schema.org/)
> **Outil de test** : [Rich Results Test](https://search.google.com/test/rich-results)

### 5.1 Organisation / Entreprise

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Nom Entreprise",
  "alternateName": "Nom Alternatif",
  "url": "https://domaine.fr",
  "logo": "https://domaine.fr/logo.png",
  "description": "Description de l'entreprise",
  "slogan": "Slogan accrocheur",
  "foundingDate": "2025",
  "areaServed": {
    "@type": "Country",
    "name": "France"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Service client",
    "areaServed": "FR",
    "availableLanguage": "French"
  },
  "sameAs": [
    "https://www.linkedin.com/company/nom",
    "https://twitter.com/nom"
  ]
}
```

### 5.2 FAQ Page

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Combien coute une formation ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Nos formations coutent entre 900EUR et 4300EUR selon la duree et le format."
      }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous partout en France ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Oui, nous intervenons dans toute la France, en presentiel ou a distance."
      }
    }
  ]
}
```

### 5.3 Services

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Nom du service",
  "description": "Description detaillee visible sur la page",
  "provider": {
    "@type": "Organization",
    "name": "Nom Entreprise"
  },
  "areaServed": {
    "@type": "Country",
    "name": "France"
  },
  "serviceType": "Type de service",
  "offers": {
    "@type": "Offer",
    "priceRange": "100EUR-500EUR",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  }
}
```

### 5.4 Convention pour les Prix

**Dans le contenu visible (HTML)** : Utiliser le format lisible avec symbole
```html
<p>Tarif : 900 EUR a 4 300 EUR</p>
<!-- ou -->
<p>Tarif : de 900 a 4 300 euros</p>
```

**Dans les donnees structurees (JSON-LD)** : Utiliser le format normalise
```json
{
    "offers": {
        "@type": "Offer",
        "priceRange": "900-4300",
        "priceCurrency": "EUR"
    }
}
```

> **Coherence** : Le prix affiche sur la page doit correspondre exactement au `priceRange` declare en Schema.org.

### 5.5 Autres Types Utiles

| Type | Usage |
|------|-------|
| `LocalBusiness` | Entreprise avec adresse physique |
| `Product` | Pages produit e-commerce |
| `Article` | Articles de blog |
| `BreadcrumbList` | Fil d'Ariane |
| `WebSite` | Page d'accueil avec recherche |
| `Person` | Pages de profil / auteur |
| `Review` | Avis clients |

---

## 6. Fichiers Techniques Essentiels

### 6.1 robots.txt

```txt
# robots.txt pour [Nom Site]
# Site web : https://domaine.fr
# Derniere mise a jour : [Date]

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/
Disallow: /.git/
Disallow: /.env

Sitemap: https://domaine.fr/sitemap.xml

# Moteurs de recherche principaux
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot
Allow: /
Crawl-delay: 0

# Agents IA (a adapter selon votre politique)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Pour bloquer les agents IA (si souhaite)
# User-agent: GPTBot
# Disallow: /
```

### 6.2 sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://domaine.fr/</loc>
        <lastmod>2025-12-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://domaine.fr/services</loc>
        <lastmod>2025-12-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
</urlset>
```

**Priorites recommandees :**
| Priorite | Type de page |
|----------|--------------|
| 1.0 | Page d'accueil |
| 0.9 | Pages de conversion (services, contact) |
| 0.8 | Pages importantes (portfolio, temoignages) |
| 0.7 | Pages secondaires (about, blog) |
| 0.3 | Pages legales |

### 6.3 .htaccess (Apache)

```apache
# ============================================
# REDIRECTION HTTPS
# ============================================
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# ============================================
# REDIRECTION WWW (choisir UNE option)
# ============================================
# Option : Supprimer www (recommande)
RewriteCond %{HTTP_HOST} ^www\.domaine\.fr$ [NC]
RewriteRule ^(.*)$ https://domaine.fr/$1 [L,R=301]

# ============================================
# PAGES D'ERREUR
# ============================================
ErrorDocument 404 /404.html
ErrorDocument 403 /403.html
ErrorDocument 500 /500.html

# ============================================
# HEADERS SECURITE
# ============================================
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>

# ============================================
# CACHE
# ============================================
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
</IfModule>

# ============================================
# COMPRESSION GZIP
# ============================================
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>

# ============================================
# SECURITE FICHIERS
# ============================================
<FilesMatch "\.(env|log|sql|bak)$">
    Order allow,deny
    Deny from all
</FilesMatch>

Options -Indexes
AddDefaultCharset UTF-8
```

---

## 7. Performance et Core Web Vitals

### 7.1 Metriques 2025 (avec INP)

> **Note** : FID (First Input Delay) est remplace par INP (Interaction to Next Paint) depuis mars 2024.

| Metrique | Seuil acceptable | Objectif ambitieux | Description |
|----------|------------------|-------------------|-------------|
| **LCP** | < 2.5s | < 2.0s | Largest Contentful Paint - affichage du plus grand element |
| **INP** | < 200ms | < 150ms | Interaction to Next Paint - reactivite aux interactions |
| **CLS** | < 0.1 | < 0.05 | Cumulative Layout Shift - stabilite visuelle |

> **Tendance 2026** : Les seuils "ambitieux" ci-dessus deviendront probablement les nouveaux standards. Visez-les des maintenant pour etre "future-proof".

### 7.2 Optimisation des Images

```html
<!-- Format moderne avec fallback -->
<picture>
    <source srcset="image.webp" type="image/webp">
    <img src="image.png"
         alt="Description"
         width="800"
         height="600"
         loading="lazy">
</picture>
```

**Bonnes pratiques :**
- Toujours specifier `width` et `height` (evite le CLS)
- Utiliser `loading="lazy"` pour images non-critiques
- Format WebP avec qualite 80-85%
- Poids < 100Ko si possible

### 7.3 CSS et JavaScript

```html
<head>
    <!-- CSS critique inline (above-the-fold) -->
    <style>
        :root { --color-primary: #a5c9ca; }
        body { font-family: system-ui, sans-serif; margin: 0; }
    </style>

    <!-- Preload CSS principal -->
    <link rel="preload" href="/css/main.min.css" as="style">
    <link rel="stylesheet" href="/css/main.min.css">
</head>
<body>
    <!-- Contenu -->

    <!-- JS en fin avec defer -->
    <script src="/js/main.min.js" defer></script>
</body>
```

**Minification :**
```bash
# CSS
npx clean-css-cli src/css/main.css -o src/css/main.min.css

# JavaScript
npx terser src/js/main.js -o src/js/main.min.js -c -m
```

### 7.4 Polices

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
      rel="stylesheet">
```

**Bonnes pratiques :**
- Maximum 2 familles de polices
- Maximum 3-4 poids par famille
- Toujours utiliser `display=swap`

---

## 8. Accessibilite et UX

### 8.1 Skip Link

```html
<body>
    <a href="#main-content" class="skip-link">Aller au contenu principal</a>
    <nav>...</nav>
    <main id="main-content">...</main>
</body>
```

```css
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px 16px;
    z-index: 100;
    text-decoration: none;
}

.skip-link:focus {
    top: 0;
}
```

### 8.2 Classe Visually-Hidden

```css
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    border: 0;
    clip: rect(0 0 0 0);
    overflow: hidden;
    white-space: nowrap;
}
```

### 8.3 Navigation Simple

```html
<!-- Navigation web standard (pas de role menu) -->
<nav aria-label="Navigation principale">
    <ul>
        <li><a href="/" aria-current="page">Accueil</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
</nav>

<!-- Bouton menu mobile -->
<button class="nav-toggle"
        aria-label="Menu"
        aria-expanded="false"
        aria-controls="nav-menu">
    <span aria-hidden="true"></span>
    <span aria-hidden="true"></span>
    <span aria-hidden="true"></span>
</button>
```

### 8.4 Formulaires Accessibles

```html
<form action="/api/contact" method="POST">
    <div class="form-group">
        <label for="email">Email <span aria-hidden="true">*</span></label>
        <input type="email"
               id="email"
               name="email"
               required
               aria-required="true"
               aria-describedby="email-help"
               autocomplete="email">
        <span id="email-help" class="help-text">
            Votre email ne sera jamais partage.
        </span>
    </div>

    <button type="submit">Envoyer</button>
</form>
```

### 8.5 Contrastes de Couleurs

**WCAG 2.1 AA (minimum obligatoire) :**
- Texte normal : ratio 4.5:1
- Gros texte (18px+ ou 14px bold) : ratio 3:1

```css
:root {
    --color-text: #1a1a1a;       /* Ratio ~16:1 sur blanc */
    --color-text-light: #2d2d2d; /* Ratio ~12:1 sur blanc */
    --color-text-muted: #595959; /* Ratio ~7:1 sur blanc */
}
```

---

## 9. Securite et Headers HTTP

### 9.1 Headers de Securite

| Header | Valeur | Fonction |
|--------|--------|----------|
| `X-Content-Type-Options` | `nosniff` | Empeche MIME-sniffing |
| `X-Frame-Options` | `SAMEORIGIN` | Protection clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Controle referrer |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | Desactive APIs sensibles |

### 9.2 Content Security Policy (CSP)

```apache
Header always set Content-Security-Policy "
    default-src 'self';
    script-src 'self' https://fonts.googleapis.com;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https:;
    connect-src 'self';
    frame-src https://calendly.com;
"
```

> **Attention aux scripts tiers** : Chaque service externe (analytics, chat, calendrier) doit etre explicitement autorise dans la CSP.

### 9.3 HTTPS et HSTS

```apache
# Redirection HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# HSTS (optionnel mais recommande)
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

---

## 10. Gestion Multi-langue

### 10.1 Attribut lang

```html
<!-- Sur l'element html -->
<html lang="fr">

<!-- Pour un passage dans une autre langue -->
<p>Notre slogan : <span lang="en">Innovation for your serenity</span></p>
```

### 10.2 Hreflang pour Sites Multilingues

```html
<head>
    <!-- Page francaise -->
    <link rel="alternate" hreflang="fr" href="https://domaine.fr/page">

    <!-- Page anglaise -->
    <link rel="alternate" hreflang="en" href="https://domaine.fr/en/page">

    <!-- Page par defaut -->
    <link rel="alternate" hreflang="x-default" href="https://domaine.fr/page">
</head>
```

### 10.3 Structure d'URL Recommandee

| Methode | Exemple | Avantages |
|---------|---------|-----------|
| Sous-repertoire | `/fr/`, `/en/` | Facile a gerer, un seul domaine |
| Sous-domaine | `fr.domaine.com` | Separation claire |
| Domaine separe | `domaine.fr`, `domaine.com` | Ciblage geographique |

---

## 11. Ressources Tierces et RGPD

### 11.1 Impact des Scripts Tiers sur la Performance

| Type | Impact LCP | Impact INP | Recommandation |
|------|------------|------------|----------------|
| Analytics (GA4) | Moyen | Faible | Charger en `defer` |
| Chat en direct | Eleve | Eleve | Charger apres interaction |
| Iframe (Calendly) | Eleve | Moyen | Lazy loading |
| Polices externes | Moyen | Faible | `preconnect` + `swap` |

### 11.2 Chargement Differe des Scripts

```html
<!-- Analytics : charger en defer -->
<script defer src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>

<!-- Chat : charger apres consentement ou interaction -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Charger le chat seulement si consentement donne
    if (hasUserConsent('chat')) {
        loadChatWidget();
    }
});
</script>

<!-- Iframe : lazy loading natif -->
<iframe src="https://calendly.com/..." loading="lazy"></iframe>
```

### 11.3 Conformite RGPD

**Elements obligatoires :**
- Bandeau de consentement cookies (avant tout tracking)
- Page "Politique de confidentialite"
- Page "Mentions legales"
- Possibilite de retirer son consentement

**Bonnes pratiques :**
```html
<!-- Bandeau cookies -->
<div id="cookie-banner" role="dialog" aria-labelledby="cookie-title">
    <h3 id="cookie-title">Gestion des cookies</h3>
    <p>Nous utilisons des cookies pour ameliorer votre experience.</p>
    <button id="accept-all">Tout accepter</button>
    <button id="reject-all">Tout refuser</button>
    <button id="customize">Personnaliser</button>
</div>
```

---

## 12. Checklists Operationnelles

### 12.1 Checklist par Type de Page

#### Page d'Accueil

| Element | Outil de verification | Frequence |
|---------|----------------------|-----------|
| Title unique (50-60 car.) | Search Console | Mise en ligne |
| Meta description (150-160 car.) | Search Console | Mise en ligne |
| Schema Organization | Rich Results Test | Mise en ligne |
| Schema FAQPage (si FAQ) | Rich Results Test | Mise en ligne |
| Open Graph | Facebook Debugger | Mise en ligne |
| H1 unique | Lighthouse | Mise en ligne |
| LCP < 2.5s | PageSpeed Insights | Mensuelle |
| CLS < 0.1 | PageSpeed Insights | Mensuelle |

#### Page Services/Produits

| Element | Outil de verification | Frequence |
|---------|----------------------|-----------|
| Schema Service ou Product | Rich Results Test | Mise en ligne |
| Prix visibles et structures | Manuel | A chaque modif |
| FAQ structuree | Rich Results Test | Mise en ligne |
| CTA clairs | Manuel | Mise en ligne |
| Images optimisees | PageSpeed | Mise en ligne |

#### Page Contact

| Element | Outil de verification | Frequence |
|---------|----------------------|-----------|
| Schema ContactPage | Rich Results Test | Mise en ligne |
| Formulaire accessible | WAVE | Mise en ligne |
| Informations de contact visibles | Manuel | Mise en ligne |
| Horaires (si applicable) | Manuel | Mise en ligne |

#### Page Blog/Article

| Element | Outil de verification | Frequence |
|---------|----------------------|-----------|
| Schema Article | Rich Results Test | Mise en ligne |
| Auteur identifie | Manuel | Mise en ligne |
| Date de publication | Manuel | Mise en ligne |
| Temps de lecture | Manuel | Mise en ligne |
| Images avec alt | WAVE | Mise en ligne |

### 12.2 Checklist SEO Classique

- [ ] `<title>` unique et descriptif (50-60 car.)
- [ ] `<meta name="description">` (150-160 car.)
- [ ] URL canonique sur chaque page
- [ ] Hierarchie H1 > H2 > H3 respectee
- [ ] Un seul H1 par page
- [ ] Attribut `alt` sur toutes les images informatives
- [ ] Open Graph configure
- [ ] Twitter Cards configurees
- [ ] robots.txt present et correct
- [ ] sitemap.xml a jour et soumis
- [ ] Site inscrit sur Google Search Console
- [ ] Site inscrit sur Bing Webmaster Tools

### 12.3 Checklist Optimisation IA

- [ ] Contenu factuel explicite (prix, zones, durees)
- [ ] Structure FAQ avec questions naturelles
- [ ] Schema.org Organization complet
- [ ] Schema.org FAQPage (si pertinent)
- [ ] Schema.org Service/Product (si pertinent)
- [ ] Correspondance Schema <-> contenu visible
- [ ] Page "A propos" avec E-E-A-T
- [ ] Temoignages/avis clients
- [ ] Liens vers profils sociaux professionnels
- [ ] robots.txt configuré pour agents IA

### 12.4 Checklist Performance

- [ ] LCP < 2.5 secondes
- [ ] INP < 200 millisecondes
- [ ] CLS < 0.1
- [ ] CSS critique inline
- [ ] CSS/JS minifies
- [ ] Images en WebP
- [ ] Dimensions images specifiees (width/height)
- [ ] `loading="lazy"` sur images non-critiques
- [ ] Preload ressources critiques
- [ ] Compression GZIP activee
- [ ] Cache navigateur configure
- [ ] Score PageSpeed > 90

### 12.5 Checklist Accessibilite

- [ ] Skip link present
- [ ] Pas de roles ARIA redondants
- [ ] Navigation au clavier possible
- [ ] Contrastes >= 4.5:1 (texte normal)
- [ ] Labels sur tous les champs de formulaire
- [ ] Focus visible sur elements interactifs
- [ ] `aria-hidden="true"` sur elements decoratifs
- [ ] `lang="fr"` sur `<html>`
- [ ] Texte alternatif sur images informatives

### 12.6 Checklist Securite

- [ ] HTTPS actif
- [ ] Redirection HTTP -> HTTPS
- [ ] Headers de securite configures
- [ ] CSP defini et teste
- [ ] Fichiers sensibles bloques
- [ ] Indexation repertoires desactivee

### 12.7 Checklist Mobile

- [ ] Viewport meta correct
- [ ] Design responsive
- [ ] Boutons/liens >= 44x44px
- [ ] Texte lisible sans zoom
- [ ] Theme-color defini
- [ ] Menu mobile accessible

---

## 13. Exemples de Code

### 13.1 Structure de Projet Recommandee

```
project/
+-- index.html
+-- robots.txt
+-- sitemap.xml
+-- .htaccess
+-- 404.html
+-- pages/
|   +-- services.html
|   +-- about.html
|   +-- contact.html
|   +-- legal/
|       +-- mentions-legales.html
|       +-- politique-confidentialite.html
|       +-- cookies.html
+-- src/
|   +-- css/
|   |   +-- main.css
|   |   +-- main.min.css
|   +-- js/
|   |   +-- main.js
|   |   +-- main.min.js
|   +-- images/
|       +-- logo.png
|       +-- logo.webp
+-- assets/
|   +-- og-image.png
+-- docs/
    +-- guides/
```

### 13.2 References du Projet SereniaTech

- **Page d'accueil** : [index.html](../../index.html)
- **Page services** : [pages/services.html](../../pages/services.html)
- **Configuration serveur** : [.htaccess](../../.htaccess)
- **Sitemap** : [sitemap.xml](../../sitemap.xml)

---

## Ressources et Documentation Officielle

### Standards et Specifications

- [Schema.org](https://schema.org/) - Vocabulaire de donnees structurees
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Core Web Vitals](https://web.dev/vitals/)
- [HTML Living Standard](https://html.spec.whatwg.org/)

### Outils de Validation

| Categorie | Outil | URL |
|-----------|-------|-----|
| SEO | Google Search Console | search.google.com/search-console |
| SEO | Bing Webmaster Tools | bing.com/webmasters |
| Schema | Rich Results Test | search.google.com/test/rich-results |
| Schema | Schema Markup Validator | validator.schema.org |
| Performance | PageSpeed Insights | pagespeed.web.dev |
| Performance | GTmetrix | gtmetrix.com |
| Accessibilite | WAVE | wave.webaim.org |
| Accessibilite | axe DevTools | deque.com/axe |
| Securite | SecurityHeaders | securityheaders.com |
| Securite | SSL Labs | ssllabs.com/ssltest |

---

## Conclusion

Un site web moderne doit etre concu pour deux audiences :

1. **Les humains** : UX, accessibilite, performance, confiance
2. **Les machines** : structure semantique, donnees structurees, contenu explicite

**Les 6 principes cles :**

| # | Principe | Implementation |
|---|----------|----------------|
| 1 | **Structure semantique HTML5** | Utiliser `nav`, `main`, `article`, `section` |
| 2 | **Donnees structurees coherentes** | Schema.org = contenu visible (pas de surcharge) |
| 3 | **Contenu "people-first"** | Intro factuelle, prix, zones, durees explicites |
| 4 | **E-E-A-T visible** | Page A propos, auteur, temoignages, certifications |
| 5 | **Performance ambitieuse** | LCP < 2.0s, INP < 150ms, CLS < 0.05 |
| 6 | **Accessibilite native** | Pas de sur-ingenierie ARIA, focus sur les standards |

> **L'approche "IA-First"** garantit une optimisation pour tous les systemes de recherche (classiques et IA) tout en respectant les standards du web et en privilegiant l'experience utilisateur.

### Prochaines etapes

1. **Appliquer le Quick Start** en debut de document sur un nouveau projet
2. **Utiliser les checklists par type de page** pour les revues
3. **Tester regulierement** avec PageSpeed Insights et Rich Results Test
4. **Mettre a jour ce guide** selon les evolutions des standards (Core Web Vitals, E-E-A-T)

---

*Document v2.1 - Decembre 2025*
*Base sur l'analyse du site SereniaTech et les recommandations de l'industrie*
*Conforme aux guidelines Google 2024-2025, Core Web Vitals (INP), et bonnes pratiques WCAG 2.1*
