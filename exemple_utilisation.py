#!/usr/bin/env python3
"""
Exemple d'utilisation du système de gestion d'états et chemins.

Ce script montre comment utiliser le GestionnaireEtats pour :
- Déterminer l'état actuel du système
- Trouver un chemin entre deux états
- Exécuter les actions d'un chemin
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from core import GestionnaireEtats, AucunEtatTrouve, EtatInconnuException


def main():
    """Exemple d'utilisation du gestionnaire d'états."""

    # Initialisation du gestionnaire
    print("=" * 60)
    print("Initialisation du gestionnaire d'états...")
    print("=" * 60)

    gestionnaire = GestionnaireEtats("config/etat-chemin.toml")

    # Afficher les états enregistrés
    print(f"\nÉtats enregistrés: {len(gestionnaire.etats)}")
    for nom, etat in gestionnaire.etats.items():
        print(f"  - {nom}: {etat}")

    # Afficher les chemins enregistrés
    print(f"\nChemins enregistrés: {len(gestionnaire.chemins)}")
    for chemin in gestionnaire.chemins:
        certain = "✓" if chemin.est_certain() else "?"
        print(f"  [{certain}] {chemin}")

    # Exemple 1: Trouver un chemin direct
    print("\n" + "=" * 60)
    print("Exemple 1: Trouver un chemin de ville → carte")
    print("=" * 60)

    chemins, complet = gestionnaire.trouver_chemin("ville", "carte")

    if chemins:
        print(f"Chemin trouvé: {len(chemins)} étape(s)")
        print(f"Chemin complet: {complet}")
        for i, chemin in enumerate(chemins, 1):
            print(f"  {i}. {chemin}")
            actions = chemin.generer_actions()
            for action in actions:
                print(f"       → {action}")
    else:
        print("Aucun chemin trouvé!")

    # Exemple 2: Trouver un chemin multi-étapes
    print("\n" + "=" * 60)
    print("Exemple 2: Trouver un chemin de ville → formation_troupe")
    print("=" * 60)

    chemins, complet = gestionnaire.trouver_chemin("ville", "formation_troupe")

    if chemins:
        print(f"Chemin trouvé: {len(chemins)} étape(s)")
        print(f"Chemin complet: {complet}")
        for i, chemin in enumerate(chemins, 1):
            print(f"  {i}. {chemin}")
    else:
        print("Aucun chemin trouvé!")

    # Exemple 3: Chemin avec incertitude
    print("\n" + "=" * 60)
    print("Exemple 3: Fermer un popup d'erreur")
    print("=" * 60)

    chemins, complet = gestionnaire.trouver_chemin("popup_erreur", "ville")

    if chemins:
        print(f"Chemin trouvé: {len(chemins)} étape(s)")
        print(f"Chemin complet: {complet}")
        if not complet:
            print("⚠ Ce chemin contient une incertitude - nécessite redétermination d'état après exécution")
        for i, chemin in enumerate(chemins, 1):
            print(f"  {i}. {chemin}")
    else:
        print("Aucun chemin trouvé!")

    # Exemple 4: Chemins depuis/vers un état
    print("\n" + "=" * 60)
    print("Exemple 4: Explorer les connexions de 'carte'")
    print("=" * 60)

    chemins_depuis = gestionnaire.obtenir_chemins_depuis("carte")
    print(f"Chemins partant de 'carte': {len(chemins_depuis)}")
    for chemin in chemins_depuis:
        print(f"  → {chemin}")

    chemins_vers = gestionnaire.obtenir_chemins_vers("carte")
    print(f"Chemins arrivant à 'carte': {len(chemins_vers)}")
    for chemin in chemins_vers:
        print(f"  ← {chemin}")

    print("\n" + "=" * 60)
    print("Fin de l'exemple")
    print("=" * 60)


if __name__ == "__main__":
    main()
