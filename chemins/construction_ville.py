"""
Chemin de la construction de bâtiment vers la ville.
"""

from typing import List
from core.chemin import Chemin
from .actions import CliquerBouton, Attendre, Action


class CheminConstructionVille(Chemin):
    """Chemin pour naviguer de la construction vers la ville."""

    etat_initial = "construction_batiment"
    etat_sortie = "ville"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour retourner de la construction à la ville."""
        return [
            CliquerBouton("bouton_retour"),
            Attendre(0.5)
        ]
