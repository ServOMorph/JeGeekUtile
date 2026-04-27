# Checklist SEO et IA - Je Geek Utile

Ce document doit etre consulte avant chaque modification du site.

---

## Checklist Nouvelle Page

### Meta Tags (dans le bloc `{% block %}`)

- [ ] `{% block title %}Titre - Je Geek Utile{% endblock %}` (50-60 car.)
- [ ] `{% block description %}Description{% endblock %}` (150-160 car.)
- [ ] `{% block canonical %}URL complete{% endblock %}`
- [ ] Blocs Open Graph si contenu specifique

### Structure HTML

- [ ] Un seul `<h1>` par page
- [ ] Hierarchie H1 > H2 > H3 sans sauter de niveau
- [ ] Sections avec `aria-labelledby` si pertinent
- [ ] Images avec `alt`, `width`, `height`, `loading="lazy"`

### Contenu pour IA

- [ ] Intro factuelle en debut de page (prix, zones, durees)
- [ ] FAQ avec questions naturelles si pertinent
- [ ] Contenu visible = contenu declare en Schema.org

### Schema.org (bloc `{% block schema_extra %}`)

Ajouter selon le type de page :
```html
{% block schema_extra %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
}
</script>
{% endblock %}
```

Types disponibles : `FAQPage`, `Service`, `ContactPage`, `AboutPage`, `Article`

---

## Checklist Modification

- [ ] Mettre a jour `sitemap.xml` (date `lastmod`)
- [ ] Verifier coherence Schema.org <-> contenu visible
- [ ] Tester avec PageSpeed Insights
- [ ] Tester avec Rich Results Test

---

## Structure de Page Type

```html
{% extends 'base.html' %}

{% block title %}Titre Page - Je Geek Utile{% endblock %}
{% block description %}Description factuelle de la page.{% endblock %}
{% block canonical %}https://jegeekutile.fr/page{% endblock %}

{% block schema_extra %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Titre",
    "description": "Description"
}
</script>
{% endblock %}

{% block content %}
<article>
    <h1>Titre Principal</h1>

    <p class="intro">
        <strong>Resume factuel</strong> : prix, zone, public cible.
    </p>

    <section aria-labelledby="section1-title">
        <h2 id="section1-title">Section 1</h2>
        <p>Contenu...</p>
    </section>

    <section aria-labelledby="faq-title">
        <h2 id="faq-title">Questions frequentes</h2>
        <dl>
            <dt>Question naturelle ?</dt>
            <dd>Reponse factuelle.</dd>
        </dl>
    </section>
</article>
{% endblock %}
```

---

## Images

Format : WebP prefere
```html
<img src="{{ url_for('static', filename='images/image.webp') }}"
     alt="Description de l'image"
     width="800"
     height="600"
     loading="lazy">
```

---

## Classes CSS Disponibles

- `.skip-link` : Lien d'evitement (deja dans base.html)
- `.visually-hidden` : Contenu accessible mais invisible
- `.intro` : Paragraphe d'introduction factuelle

---

## Fichiers a Maintenir

| Fichier | Emplacement | Quand mettre a jour |
|---------|-------------|---------------------|
| robots.txt | static/robots.txt | Si nouvelles pages privees |
| sitemap.xml | static/sitemap.xml | A chaque nouvelle page |
| Schema.org | base.html | Si infos organisation changent |

---

## Performance

Objectifs :
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1
- PageSpeed > 90

Bonnes pratiques :
- JS avec `defer`
- Images en WebP avec dimensions
- CSS minifie en production

---

## Outils de Verification

- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [WAVE Accessibility](https://wave.webaim.org/)
- [Schema Validator](https://validator.schema.org/)
