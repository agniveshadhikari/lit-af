from .card import Card
from .suit import Suit
from .rank import Rank

from random import shuffle
from itertools import product


def deck():
    return [Card(suit, rank) for suit, rank in product(Suit, Rank)]


def random_permutation():
    d = deck()
    shuffle(d)
    return d
