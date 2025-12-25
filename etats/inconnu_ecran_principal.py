"""
État inconnu pour les écrans principaux.

Représente une incertitude sur l'écran principal affiché.
"""

from core.etat_inconnu import EtatInconnu


class EtatInconnuEcranPrincipal(EtatInconnu):
    """
    État inconnu pour les écrans principaux.

    Utilisé quand on ferme un popup et qu'on ne sait pas
    sur quel écran principal on va atterrir.
    """

    nom = "inconnu_ecran_principal"
    groupes = ["ecran_principal", "inconnu"]

    etats_possibles = [
        "ville",
        "carte",
        "formation_troupe",
        "construction_batiment"
    ]
