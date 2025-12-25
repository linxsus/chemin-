"""
Module core - Contient les classes de base du système de gestion d'états et chemins.
"""

from .exceptions import (
    ErreurConfiguration,
    ErreurValidation,
    EtatInconnuException,
    AucunEtatTrouve
)
from .etat import Etat, SingletonMeta
from .etat_inconnu import EtatInconnu
from .chemin import Chemin
from .gestionnaire_etats import GestionnaireEtats

__all__ = [
    'ErreurConfiguration',
    'ErreurValidation',
    'EtatInconnuException',
    'AucunEtatTrouve',
    'Etat',
    'SingletonMeta',
    'EtatInconnu',
    'Chemin',
    'GestionnaireEtats'
]
