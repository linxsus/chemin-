"""
État de l'écran de la carte.
"""

from core.etat import Etat


class EtatCarte(Etat):
    """État représentant l'écran de la carte du monde."""

    nom = "carte"
    groupes = ["ecran_principal"]

    def verif(self) -> bool:
        """
        Vérifie si on est sur l'écran de la carte.

        TODO: Implémenter la logique de détection réelle
        """
        return False
