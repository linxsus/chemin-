"""
Chemin de démarrage de l'application.

Ce chemin a une sortie inconnue complète car on ne sait pas
où on va atterrir après le lancement de l'application.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import LancerApplication, Attendre, Action


class CheminDemarrage(Chemin):
    """Chemin de démarrage - sortie complètement inconnue."""

    etat_initial = "demarrage"
    etat_sortie = None  # Sortie complètement inconnue

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour démarrer l'application."""
        return [
            LancerApplication(),
            Attendre(5.0)  # Attendre que l'application démarre
        ]
