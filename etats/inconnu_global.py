"""
État inconnu global.

Représente une incertitude totale sur l'état du système.
"""

from core.etat_inconnu import EtatInconnu


class EtatInconnuGlobal(EtatInconnu):
    """
    État inconnu global (fallback).

    Quand aucun état ne correspond et qu'on ne sait vraiment pas
    où on est. La liste etats_possibles vide signifie que tous
    les états enregistrés seront testés.
    """

    nom = "inconnu_global"
    groupes = ["inconnu"]

    etats_possibles = []
