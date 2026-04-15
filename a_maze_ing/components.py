from enum import Enum

class Palette(str, Enum):
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
    __slots__ = ['borders', 'is_locked', 'is_explored']
    
    def __init__(self, borders: int = 15, is_locked: bool = False):
        self.borders: int = borders
        self.is_locked: bool = is_locked
        self.is_explored: bool = False