"""
Chemin de la ville vers la construction de bâtiment.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminVilleConstruction(Chemin):
    """Chemin pour naviguer de la ville vers la construction de bâtiment."""

    etat_initial = "ville"
    etat_sortie = "construction_batiment"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour aller de la ville à la construction."""
        return [
            CliquerBouton("bouton_construire"),
            Attendre(0.5)
        ]
