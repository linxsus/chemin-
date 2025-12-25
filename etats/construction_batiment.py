"""
État de l'écran de construction de bâtiment.
"""

from core.etat import Etat


class EtatConstructionBatiment(Etat):
    """État représentant l'écran de construction de bâtiment."""

    nom = "construction_batiment"
    groupes = ["ecran_principal", "construction"]

    def verif(self) -> bool:
        """
        Vérifie si on est sur l'écran de construction de bâtiment.

        TODO: Implémenter la logique de détection réelle
        """
        return False
