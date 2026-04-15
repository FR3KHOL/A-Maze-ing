"""Components module defining basic data structures for the maze."""
from enum import Enum


class Palette(str, Enum):
    """ANSI color codes for terminal rendering."""
    BLK = "\033[30m"
    R = "\033[31m"
    G = "\033[32m"
    Y = "\033[33m"
    B = "\033[34m"
    M = "\033[35m"
    C = "\033[36m"
    W = "\033[37m"
    BR = "\033[38;5;136m"
    RST = "\033[0m"


class Node:
    """Represents a single cell in the maze grid."""

    __slots__ = ['borders', 'is_locked', 'is_explored']

    def __init__(self, borders: int = 15, is_locked: bool = False) -> None:
        """Initialize the node.

        Args:
            borders (int): Hexadecimal representation of walls.
            is_locked (bool): Whether the cell cannot be modified.
        """
        self.borders: int = borders
        self.is_locked: bool = is_locked
        self.is_explored: bool = False
