"""
Système de logging pour le gestionnaire d'états et chemins.
"""

import logging
from typing import Optional


def get_module_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Obtient un logger configuré pour un module spécifique.

    Args:
        name: Nom du module (ex: 'GestionnaireEtats')
        level: Niveau de log optionnel (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configuré pour le module
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(levelname)s] %(name)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if level:
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        logger.setLevel(level_map.get(level.upper(), logging.INFO))
    else:
        logger.setLevel(logging.INFO)

    return logger
