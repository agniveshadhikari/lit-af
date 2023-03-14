from enum import Enum
from dataclasses import dataclass


class Suit(Enum):
    hearts = 1
    spades = 2
    clubs = 3
    diamonds = 4


class SuitHalf(Enum):
    lower = 0
    upper = 1


@dataclass
class SemiSuit:
    suit: Suit
    half: SuitHalf
