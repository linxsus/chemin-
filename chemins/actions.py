"""
Actions de base pour les chemins.

Ce module définit les classes d'actions utilisées dans les chemins.
Ces classes sont des placeholders - à remplacer par les vraies
implémentations du framework d'automatisation.
"""

from typing import Any


class Action:
    """Classe de base pour toutes les actions."""

    def executer(self) -> None:
        """Exécute l'action."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class CliquerBouton(Action):
    """Action de clic sur un bouton."""

    def __init__(self, nom_bouton: str):
        self.nom_bouton = nom_bouton

    def executer(self) -> None:
        """TODO: Implémenter le clic réel sur le bouton."""
        pass

    def __repr__(self) -> str:
        return f"CliquerBouton('{self.nom_bouton}')"


class Attendre(Action):
    """Action d'attente."""

    def __init__(self, duree: float):
        """
        Args:
            duree: Durée d'attente en secondes
        """
        self.duree = duree

    def executer(self) -> None:
        """TODO: Implémenter l'attente réelle."""
        import time
        time.sleep(self.duree)

    def __repr__(self) -> str:
        return f"Attendre({self.duree})"


class LancerApplication(Action):
    """Action de lancement d'application."""

    def executer(self) -> None:
        """TODO: Implémenter le lancement réel de l'application."""
        pass

    def __repr__(self) -> str:
        return "LancerApplication()"


class CliquerPosition(Action):
    """Action de clic à une position x, y."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def executer(self) -> None:
        """TODO: Implémenter le clic réel à la position."""
        pass

    def __repr__(self) -> str:
        return f"CliquerPosition({self.x}, {self.y})"


class Glisser(Action):
    """Action de glissement (drag)."""

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def executer(self) -> None:
        """TODO: Implémenter le glissement réel."""
        pass

    def __repr__(self) -> str:
        return f"Glisser(({self.x1}, {self.y1}) → ({self.x2}, {self.y2}))"
