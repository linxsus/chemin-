"""
État du popup de confirmation.
"""

from core.etat import Etat


class EtatPopupConfirmation(Etat):
    """État représentant un popup de confirmation."""

    nom = "popup_confirmation"
    groupes = ["popup"]

    def verif(self) -> bool:
        """
        Vérifie si un popup de confirmation est affiché.

        TODO: Implémenter la logique de détection réelle
        """
        return False
