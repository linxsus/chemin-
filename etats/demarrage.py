"""
État de démarrage de l'application.
"""

from core.etat import Etat


class EtatDemarrage(Etat):
    """État représentant l'écran de démarrage/chargement."""

    nom = "demarrage"
    groupes = ["systeme"]

    def verif(self) -> bool:
        """
        Vérifie si on est sur l'écran de démarrage.

        TODO: Implémenter la logique de détection réelle
        (ex: OCR, image matching, etc.)
        """
        return False
