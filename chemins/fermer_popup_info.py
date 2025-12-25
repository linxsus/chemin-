"""
Chemin pour fermer un popup d'information.

Ce chemin a une sortie incertaine car on ne sait pas
sur quel écran on va atterrir après avoir fermé le popup.
"""

from typing import List
from core.chemin import Chemin
from .actions import CliquerBouton, Attendre, Action


class CheminFermerPopupInfo(Chemin):
    """Chemin pour fermer un popup d'information (sortie incertaine)."""

    etat_initial = "popup_info"
    etat_sortie = "inconnu_ecran_principal"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour fermer le popup d'information."""
        return [
            CliquerBouton("bouton_ok"),
            Attendre(0.5)
        ]
