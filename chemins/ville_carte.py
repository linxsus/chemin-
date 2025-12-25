"""
Chemin de la ville vers la carte.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminVilleCarte(Chemin):
    """Chemin pour naviguer de la ville vers la carte."""

    etat_initial = "ville"
    etat_sortie = "carte"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour aller de la ville à la carte."""
        return [
            CliquerBouton("bouton_carte"),
            Attendre(1.0)
        ]
