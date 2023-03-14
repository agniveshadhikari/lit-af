from ..cards import Card, SemiSuit

from dataclasses import dataclass
from enum import Enum

from typing import Dict
from datetime import timedelta


class MoveType(Enum):
    ask = 1
    declare = 2
    # Weird nomencalture coz 'pass' is a keyword
    gift = 3


@dataclass
class AskMove:
    player: int
    card: Card

    @property
    def type(self):
        return MoveType.ask


@dataclass
class DeclareMove:

    semisuit: SemiSuit
    card_player_map: Dict[Card, int]

    @property
    def type(self):
        return MoveType.declare


@dataclass
class GiftMove:
    player: int

    @property
    def type(self):
        return MoveType.gift


Move = AskMove | DeclareMove | GiftMove


@dataclass
class Action:

    player: int
    move: Move

    @property
    def move_type(self):
        return self.move.type
