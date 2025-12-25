"""
État inconnu pour les popups.

Représente une incertitude sur le type de popup affiché.
"""

from core.etat_inconnu import EtatInconnu


class EtatInconnuPopup(EtatInconnu):
    """
    État inconnu pour les popups.

    Quand un chemin ferme un popup mais qu'on ne sait pas
    quel était le popup affiché ou ce qu'il y a dessous.
    """

    nom = "inconnu_popup"
    groupes = ["popup", "inconnu"]

    etats_possibles = [
        "popup_erreur",
        "popup_confirmation",
        "popup_info"
    ]
