from enum import Enum

from .suit import SuitHalf
from ..utils import split


class Rank(Enum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    # seven is not part of this game
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13

    @property
    def next(self):
        return {
            Rank.ace: Rank.two,
            Rank.two: Rank.three,
            Rank.three: Rank.four,
            Rank.four: Rank.five,
            Rank.five: Rank.six,
            Rank.six: Rank.eight,
            Rank.eight: Rank.nine,
            Rank.nine: Rank.ten,
            Rank.ten: Rank.jack,
            Rank.jack: Rank.queen,
            Rank.queen: Rank.king,
            Rank.king: Rank.ace,
        }.get(self)

    @property
    def prev(self):
        return {
            Rank.two: Rank.ace,
            Rank.three: Rank.two,
            Rank.four: Rank.three,
            Rank.five: Rank.four,
            Rank.six: Rank.five,
            Rank.eight: Rank.six,
            Rank.nine: Rank.eight,
            Rank.ten: Rank.nine,
            Rank.jack: Rank.ten,
            Rank.queen: Rank.jack,
            Rank.king: Rank.queen,
            Rank.ace: Rank.king,
        }.get(self)

    @classmethod
    def get_half(cls, suit_half: SuitHalf):
        lower, upper = split([rank for rank in Rank], 2)
        if suit_half == SuitHalf.lower:
            return lower
        elif suit_half == SuitHalf.upper:
            return upper
        else:
            raise ValueError(f"Unsupported suit-half: {suit_half}")
