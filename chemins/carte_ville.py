"""
Chemin de la carte vers la ville.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminCarteVille(Chemin):
    """Chemin pour naviguer de la carte vers la ville."""

    etat_initial = "carte"
    etat_sortie = "ville"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour aller de la carte à la ville."""
        return [
            CliquerBouton("bouton_ville"),
            Attendre(1.0)
        ]
