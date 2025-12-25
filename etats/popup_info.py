"""
État du popup d'information.
"""

from core.etat import Etat


class EtatPopupInfo(Etat):
    """État représentant un popup d'information."""

    nom = "popup_info"
    groupes = ["popup"]

    def verif(self) -> bool:
        """
        Vérifie si un popup d'information est affiché.

        TODO: Implémenter la logique de détection réelle
        """
        return False
