# VibeCode Sessions — Landing page V4

Page HTML standalone ciblant les étudiants en informatique, promouvant des sessions hebdomadaires de vibe coding sur Discord.

## Concept

Le développeur de demain maîtrise deux compétences :

1. **Vibecoder** — dialoguer avec l'IA, produire 10× plus vite
2. **Comprendre et modifier le code** — lire, débugger, garantir la qualité

Les études en informatique forment la compétence 2. Ces sessions ajoutent la compétence 1.

## Contenu de la page

| Section | Description |
|---------|-------------|
| Hero | Accroche + chips contextuels + CTA Discord |
| Les 2 compétences | Duo-grid neon/magenta + résultat équation |
| Ta formation | 3 cartes valorisant les fondations académiques |
| IA locale (valeur de base) | Ollama — éthique, éco-responsabilité, autonomie |
| Programme | 6 cartes de contenu hebdomadaire |
| Arsenal | 6 outils : GitHub, VSCode, Claude Code, Codex, Antigravity, Zcode |
| Orchestration multi-agents | Config multi-agents, gestion contexte/tokens, agents parallèles |
| Format | Quand / Où / Durée / Pour qui |
| Comment ça marche | 3 étapes : rejoindre Discord → se connecter le soir J → revenir |
| CTA final | Bouton Discord principal |

## Technique

- **Fichier unique** `index.html` — pas de dépendance externe sauf Google Fonts
- **Charte V3 inline** — tokens CSS, Orbitron / JetBrains Mono / Space Grotesk, CRT scanlines, vignette
- **Responsive** — breakpoints : 1200px / 1024px / 900px / 600px / 480px
- **Flux sans inscription** — 1 clic Discord, pas de formulaire

## À compléter

- Remplacer `https://discord.gg/` par le vrai lien d'invitation Discord
- Définir le jour fixe de la semaine pour les sessions
