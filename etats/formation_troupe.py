"""
État de l'écran de formation de troupes.
"""

from core.etat import Etat


class EtatFormationTroupe(Etat):
    """État représentant l'écran de formation de troupes."""

    nom = "formation_troupe"
    groupes = ["ecran_principal", "militaire"]

    def verif(self) -> bool:
        """
        Vérifie si on est sur l'écran de formation de troupes.

        TODO: Implémenter la logique de détection réelle
        """
        return False
