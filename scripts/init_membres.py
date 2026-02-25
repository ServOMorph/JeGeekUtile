"""
Ajoute un membre à la table membre_equipe de façon interactive.
Usage : python scripts/init_membres.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'site internet'))

from app import app, db, MembreEquipe


def ask(label, required=False, default=None):
    hint = f" [{default}]" if default else (" (obligatoire)" if required else " (laisser vide pour ignorer)")
    while True:
        value = input(f"{label}{hint} : ").strip()
        if not value and default:
            return default
        if not value and required:
            print("  Ce champ est obligatoire.")
            continue
        return value or None


def main():
    print("\n=== Ajout d'un membre de l'équipe ===\n")

    prenom   = ask("Prénom",   required=True)
    nom      = ask("Nom",      required=True)
    role     = ask("Rôle / Poste")
    bio      = ask("Bio courte")
    photo    = ask("Nom du fichier photo (ex: raphael.jpg, dans static/images/membres/)")
    github   = ask("URL GitHub")
    linkedin = ask("URL LinkedIn")
    email    = ask("Email public")
    site     = ask("URL site internet")

    membres_existants = []
    with app.app_context():
        membres_existants = [(m.ordre or 0) for m in MembreEquipe.query.all()]
    ordre_defaut = str(max(membres_existants) + 1) if membres_existants else "1"
    ordre_str = ask("Ordre d'affichage", default=ordre_defaut)
    ordre = int(ordre_str) if ordre_str else 1

    print(f"\n--- Récapitulatif ---")
    print(f"  Nom       : {prenom} {nom}")
    print(f"  Rôle      : {role or '-'}")
    print(f"  Bio       : {bio or '-'}")
    print(f"  Photo     : {photo or '-'}")
    print(f"  GitHub    : {github or '-'}")
    print(f"  LinkedIn  : {linkedin or '-'}")
    print(f"  Email     : {email or '-'}")
    print(f"  Site      : {site or '-'}")
    print(f"  Ordre     : {ordre}")

    confirm = input("\nConfirmer l'ajout ? [O/n] : ").strip().lower()
    if confirm == 'n':
        print("Annulé.")
        return

    with app.app_context():
        db.create_all()
        existe = MembreEquipe.query.filter_by(prenom=prenom, nom=nom).first()
        if existe:
            print(f"\n{prenom} {nom} est déjà présent dans la base.")
            return
        membre = MembreEquipe(
            prenom=prenom,
            nom=nom,
            role=role,
            bio=bio,
            photo_filename=photo,
            github_url=github,
            linkedin_url=linkedin,
            email_public=email,
            site_url=site,
            ordre=ordre,
            visible=True,
        )
        db.session.add(membre)
        db.session.commit()
        print(f"\n✓ {prenom} {nom} ajouté avec succès (id={membre.id}).")


if __name__ == "__main__":
    main()
