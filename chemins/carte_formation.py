"""
Chemin de la carte vers la formation de troupes.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminCarteFormation(Chemin):
    """Chemin pour naviguer de la carte vers la formation de troupes."""

    etat_initial = "carte"
    etat_sortie = "formation_troupe"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour aller de la carte à la formation."""
        return [
            CliquerBouton("bouton_formation"),
            Attendre(0.5)
        ]
