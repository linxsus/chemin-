"""
État de l'écran principal de la ville.
"""

from core.etat import Etat


class EtatVille(Etat):
    """État représentant l'écran de la ville (écran principal)."""

    nom = "ville"
    groupes = ["ecran_principal"]

    def verif(self) -> bool:
        """
        Vérifie si on est sur l'écran de la ville.

        TODO: Implémenter la logique de détection réelle
        (ex: detecter_bouton_carte() and detecter_titre_ville())
        """
        return False
