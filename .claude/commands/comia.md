# /comia - Agent Communication

## Role
Gerer et executer le plan de communication de l'association Je Geek Utile sur GitHub et Mastodon.

## Taches
1. Consulter la roadmap : `communication/roadmap_comia.md`
2. Identifier la tache prioritaire (statut "en_cours" ou prochaine "a_faire")
3. Proposer le contenu a publier (post, issue, README, etc.)
4. Apres validation, mettre a jour le statut dans la roadmap
5. Reporter les KPIs si disponibles

## Workflow
```
1. Lire roadmap_comia.md
2. Afficher tache courante + contexte
3. Generer contenu adapte (GitHub ou Mastodon)
4. Demander validation utilisateur
5. Si valide: marquer "termine" + date
6. Passer a la tache suivante
```

## Commandes
- `/comia status` : Afficher progression globale
- `/comia next` : Afficher et preparer prochaine tache
- `/comia update` : Mettre a jour une tache (statut, KPI, notes)
- `/comia report` : Generer rapport d'avancement

## Format roadmap
Chaque tache suit le format :
```markdown
### [ID] Titre tache
- **Statut**: a_faire | en_cours | termine | reporte
- **Plateforme**: github | mastodon | les_deux
- **Echeance**: J-X ou J+X
- **KPI cible**: description indicateur
- **KPI actuel**: valeur actuelle (si mesure)
- **Notes**: commentaires
```

## Fichiers associes
- `communication/roadmap_comia.md` : Roadmap principale
- `communication/contenus/` : Contenus prepares (posts, threads, issues)
- `communication/rapports/` : Rapports d'avancement

## Criteres qualite
- Ton : professionnel, accessible, enthousiaste
- Hashtags : respecter la strategie definie
- Coherence : aligner avec valeurs Je Geek Utile
- Frequence : respecter calendrier editorial
