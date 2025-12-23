from .tutorial import Tutorial, TutorialStep, tutorial_manager

def load_default_tutorial():
    steps = [
        TutorialStep(
            id="step_1",
            zone="comet_prompt",
            message="Étape 1/3 - Premier clic automatique :\n\n1️⃣ Cliquez sur le bouton vert '⚡ Pré-remplir' ci-dessous\n2️⃣ Le formulaire va se remplir automatiquement\n3️⃣ Descendez dans la page et cliquez sur le bouton vert 'Exécuter'\n\nC'est tout ! L'action va simuler un clic sur la zone 'comet_prompt'.",
            hint="💡 Astuce : Avant de commencer, assurez-vous d'avoir créé la zone 'comet_prompt' dans le panneau 'Zones' (en haut à droite). Sinon, vous verrez un message d'erreur.",
            required_action="click"
        ),
        TutorialStep(
            id="step_2",
            zone="claude_input",
            message="Étape 2/3 - Deuxième clic :\n\n✅ Bravo pour la première étape !\n\nMaintenant, faites exactement pareil :\n1️⃣ Cliquez sur '⚡ Pré-remplir' (le formulaire va changer)\n2️⃣ Cliquez sur 'Exécuter'\n\nCette fois, l'action va cliquer sur la zone 'claude_input'.",
            hint="💡 La zone 'claude_input' représente l'endroit où vous tapez normalement du texte pour parler à Claude.",
            required_action="click"
        ),
        TutorialStep(
            id="step_3",
            zone="claude_send",
            message="Étape 3/3 - Dernière étape :\n\n🎯 Dernière ligne droite !\n\nEncore une fois :\n1️⃣ Cliquez sur '⚡ Pré-remplir'\n2️⃣ Cliquez sur 'Exécuter'\n\nCette action va cliquer sur le bouton 'Envoyer' de Claude. Vous aurez terminé ! 🎉",
            hint="💡 Cette zone représente le bouton qui envoie votre message à Claude. Après cette étape, vous saurez automatiser toute une conversation !",
            required_action="click"
        )
    ]

    tutorial = Tutorial(
        id="tutorial_comet_claude",
        title="🎓 Tutoriel : Automatiser Claude",
        description="Bienvenue ! 👋\n\nCe tutoriel va vous apprendre à automatiser des clics de souris. C'est très simple :\n\n✨ Vous allez apprendre à créer 3 clics automatiques\n🎯 Chaque clic sera sur une 'zone' que vous aurez définie\n⚡ Utilisez le bouton 'Pré-remplir' pour aller plus vite !\n\nPrêt ? Cliquez sur 'Démarrer le tutoriel' ! 🚀",
        steps=steps
    )

    tutorial_manager.load_tutorial(tutorial)
