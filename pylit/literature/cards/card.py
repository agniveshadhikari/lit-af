from dataclasses import dataclass

from .rank import Rank
from .suit import Suit, SemiSuit


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    @property
    def next(self):
        return Card(self.suit, self.rank.next)

    @property
    def prev(self):
        return Card(self.suit, self.rank.prev)

    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name}"

    @classmethod
    def get_suit(cls, suit: Suit):
        return [Card(suit, rank) for rank in Rank]

    @classmethod
    def get_semisuit(cls, semisuit: SemiSuit):
        return [Card(semisuit.suit, rank) for rank in Rank.get_half(semisuit.half)]
