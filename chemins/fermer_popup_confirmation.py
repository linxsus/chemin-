"""
Chemin pour fermer un popup de confirmation.

Ce chemin a une sortie incertaine car on ne sait pas
sur quel écran on va atterrir après avoir confirmé.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminFermerPopupConfirmation(Chemin):
    """Chemin pour fermer un popup de confirmation (sortie incertaine)."""

    etat_initial = "popup_confirmation"
    etat_sortie = "inconnu_ecran_principal"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour confirmer et fermer le popup."""
        return [
            CliquerBouton("bouton_confirmer"),
            Attendre(0.5)
        ]
