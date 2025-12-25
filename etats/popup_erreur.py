"""
État du popup d'erreur.
"""

from core.etat import Etat


class EtatPopupErreur(Etat):
    """État représentant un popup d'erreur."""

    nom = "popup_erreur"
    groupes = ["popup"]

    def verif(self) -> bool:
        """
        Vérifie si un popup d'erreur est affiché.

        TODO: Implémenter la logique de détection réelle
        """
        return False
