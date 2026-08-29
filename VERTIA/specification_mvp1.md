# Spécification — VertIA MVP 1

## Finalité

Présenter VertIA, vérifier l'intérêt pour les IA locales et constituer une liste de personnes à recontacter. Le MVP ne promet ni compte, ni recommandation de matériel, ni tableau de bord.

## Publics prioritaires

Ces segments sont des hypothèses de lancement à valider par les retours recueillis :

1. Personnes curieuses d'utiliser une IA sur leur ordinateur sans dépendre d'un service distant.
2. Utilisateurs techniques ou créatifs qui recherchent davantage de maîtrise sur leurs outils et leurs données.
3. Membres d'associations, collectifs ou petites structures qui souhaitent découvrir les usages et limites des IA locales.

## Promesse

VertIA aide à comprendre, explorer et, à terme, utiliser des IA locales sur son propre ordinateur, dans une approche transparente, sobre et respectueuse des données.

La landing page ne doit pas suggérer que tous les ordinateurs sont compatibles ni que l'usage local garantit une sécurité absolue.

## Valeurs

VertIA porte une vision où les humains et les IA cohabitent de manière apaisée, au service de choix éclairés et d'usages utiles.

- **Écologie et écoresponsabilité** : privilégier la sobriété, expliciter les besoins matériels et éviter les usages ou renouvellements inutiles.
- **Éthique** : présenter les bénéfices, les limites et les impacts des outils sans promesse trompeuse.
- **Durabilité** : valoriser des pratiques maintenables, des outils ouverts lorsqu'ils sont adaptés et une autonomie qui s'inscrit dans le temps.
- **Respect humain** : faire de l'IA un outil qui assiste les personnes, sans déresponsabiliser ni effacer leur jugement.

## Parcours de la landing page

| Étape | Objectif | Contenu / action |
| --- | --- | --- |
| Découverte | Comprendre le sujet en quelques secondes. | Titre, promesse et appel à l'action « Je souhaite suivre le lancement ». |
| Compréhension | Expliquer ce qu'est une IA locale. | Définition simple, exécution sur l'ordinateur personnel, limites de compatibilité et exemples d'usages à venir. |
| Réassurance | Rendre la démarche crédible. | Principes : transparence, maîtrise des données, sobriété numérique et logiciels open source quand ils sont adaptés. |
| Inscription | Recueillir un moyen de recontact. | Formulaire, information sur le traitement et confirmation de l'inscription. |

## Structure et contenu proposé

### En-tête

- Logo ou nom VertIA.
- Navigation d'ancrage : « Le projet », « Pourquoi local ? », « Être informé ».

### Hero

- Titre : « Explorer l'IA locale, sur votre ordinateur. »
- Texte : « VertIA prépare un espace pour comprendre et expérimenter des intelligences artificielles exécutées localement, avec une approche transparente et sobre. »
- Bouton : « Je souhaite suivre le lancement ».

### Section « Pourquoi une IA locale ? »

- « Garder davantage de maîtrise sur ses usages et ses données. »
- « Comprendre les possibilités comme les limites selon son ordinateur. »
- « Découvrir des outils ouverts et des pratiques responsables. »

### Section « Ce que VertIA prépare »

- Information et ressources pour débuter.
- Mise en relation de personnes intéressées.
- À venir après validation de l'intérêt : aide au choix de projets open source et tableau de bord local.

### Section « Nos repères »

- Une IA qui aide les personnes à décider, sans se substituer à elles.
- Des usages plus sobres, plus transparents et pensés pour durer.
- Une exploration des limites techniques, sociales et environnementales de l'IA.

### Section « Participer au lancement »

- Texte : « Laissez votre adresse pour être informé des prochaines étapes de VertIA. »
- Formulaire décrit ci-dessous.

### Pied de page

- Porteur : Je Geek Utile, projet associatif en cours de constitution (association non encore declaree).
- Lien ou coordonnées vers les mentions légales et la politique de confidentialité.
- Année de publication.

## Recueil d'intérêt

### Mécanisme retenu

Le formulaire est intégré à la landing page et traité par Netlify Forms. Ce choix permet un déploiement statique du MVP 1 sur Netlify, mais introduit Netlify comme sous-traitant de la collecte.

Avant publication, il faudra définir la boîte de contact, la durée de conservation et la personne ou entité responsable du traitement. Ces informations ne sont pas disponibles dans le projet à ce stade.

### Données collectées

| Donnée | Caractère | Finalité |
| --- | --- | --- |
| Adresse e-mail | Obligatoire | Informer des suites du lancement et recontacter la personne intéressée. |
| Centre d'intérêt principal | Facultatif | Comprendre l'intérêt initial : découverte, usages créatifs, usages techniques, vie privée, autre. |
| Consentement à être recontacté | Obligatoire | Confirmer que l'adresse peut être utilisée pour le suivi du lancement. |

Ne pas demander de configuration matérielle, de nom complet, de téléphone ni de données d'usage au MVP 1.

### Règles de traitement attendues

- Afficher la finalité, le responsable, le moyen de contact, la durée de conservation et le droit de retrait avant l'envoi.
- Utiliser une protection anti-abus sans traceur tiers si nécessaire.
- Restreindre l'accès aux soumissions Netlify aux seules personnes autorisées.
- Prévoir une désinscription ou suppression sur simple demande.

## Mesure du lancement

Sans outil d'analyse tiers, produire des indicateurs agrégés depuis les journaux applicatifs :

| Indicateur | Définition | But initial |
| --- | --- | --- |
| Visites de la landing page | Chargements de la page, agrégés par jour. | Mesurer la portée des messages de lancement. |
| Inscriptions validées | Adresses enregistrées sans doublon. | Mesurer l'intérêt qualifié. |
| Taux de conversion | Inscriptions validées / visites. | Comparer les canaux de lancement. |
| Centres d'intérêt | Répartition des choix facultatifs. | Orienter la suite du projet. |

Les seuils de succès ne peuvent pas être fixés sans hypothèse de diffusion, de durée et de volume de trafic. Ils doivent être arrêtés avant le lancement public.

## Critères d'acceptation de la phase 2

- La page est utilisable sur mobile et ordinateur, sans dépendance externe non validée.
- Le rendu respecte le thème sombre et la contrainte de pixels blancs du projet parent.
- Le contenu explique les bénéfices et les limites de l'IA locale sans promesse trompeuse.
- Le bouton principal mène au formulaire et le formulaire signale clairement les erreurs et la confirmation d'envoi.
- L'adresse e-mail est validée par le navigateur et les données sont envoyées par Netlify Forms. Les doublons ne sont pas gérés par ce MVP statique.
- Les informations de confidentialité obligatoires sont présentes avant activation du formulaire en production.
- Des tests couvrent la soumission valide, les entrées invalides, le doublon et l'affichage de la page.

## Décisions requises avant publication

1. Coordonnées de contact et responsable du traitement.
2. Durée de conservation des inscriptions.
3. Objectif chiffré, durée de la campagne et canaux de diffusion.
4. Configuration du site Netlify et des accès aux soumissions.
