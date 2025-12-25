"""
Chemin pour fermer un popup d'erreur.

Ce chemin a une sortie incertaine car on ne sait pas
sur quel écran on va atterrir après avoir fermé le popup.
"""

from typing import List
from core.chemin import Chemin
from chemins.actions import CliquerBouton, Attendre, Action


class CheminFermerPopupErreur(Chemin):
    """Chemin pour fermer un popup d'erreur (sortie incertaine)."""

    etat_initial = "popup_erreur"
    etat_sortie = "inconnu_ecran_principal"

    def fonction_actions(self) -> List[Action]:
        """Génère les actions pour fermer le popup d'erreur."""
        return [
            CliquerBouton("bouton_fermer"),
            Attendre(0.5)
        ]
