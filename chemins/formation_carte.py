"""
Chemin de la formation de troupes vers la carte.
"""

from typing import List
from core.chemin import Chemin
from .actions import CliquerBouton, Attendre, Action


class CheminFormationCarte(Chemin):
    """Chemin pour naviguer de la formation de troupes vers la carte."""

    etat_initial = "formation_troupe"
    etat_sortie = "carte"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour retourner de la formation à la carte."""
        return [
            CliquerBouton("bouton_retour"),
            Attendre(0.5)
        ]
