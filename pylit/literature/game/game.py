from ..utils import split
from ..cards import Card, SemiSuit, deck
from .move import Action, Move, MoveType

from enum import Enum
from collections import defaultdict
import json

from typing import Dict, List


class SemiSuitState(Enum):
    active: 1
    declared: 2
    discarded: 3


class Game:
    def __init__(self, num_players):
        if num_players not in [4, 6, 8]:
            raise ValueError("num_players has to be in [4, 6, 8]")
        self.num_players = num_players

        self.semisuit_states: Dict[SemiSuit, SemiSuitState] = defaultdict(
            lambda: SemiSuitState.active)
        self.player_hands: List[List[Card]] = list(split(
            deck.random_permutation(), num_players))

        self.turn: int = 0
        self.actions = []
        self.scores = [0, 0]

    # Team belongingness methods

    def team(self, player: int):
        return 0 if player < self.num_players//2 else 1

    def same_team(self, player_a, player_b):
        return self.team(player_a) == self.team(player_b)

    # Players' hands

    def player_has_cards(self, player: int):
        return len(self.player_hands[player]) > 0

    def player_hand(self, player: int):
        return list(self.player_hands[player])

    def player_has(self, player: int, card: Card):
        return card in self.player_hand(player)

    def card_loc(self, card):
        for player, player_hand in enumerate(self.player_hands):
            if card in player_hand:
                return player

        return None

    # Move/Action methods

    def ensure_legal(self, action: Action):

        def ensure_target_player_not_dead():
            if not self.player_has_cards(action.move.player):
                raise Exception(
                    f"Player {action.player} can not play dead player {action.move.player}")

        if self.turn != action.player:
            raise Exception(f"Not player {action.player}'s turn.")

        if action.move_type == MoveType.ask:
            ensure_target_player_not_dead()
            if not action.move.card in nbrs(*self.player_hands[action.player]):
                raise Exception(
                    f"Player {action.player} can not ask for {action.move.card}")
            if self.same_team(action.move.player, action.player):
                raise Exception(
                    f"Player {action.player} can not ask from teammate player {action.move.player}")

        if action.move_type == MoveType.gift:
            ensure_target_player_not_dead()
            if not self.same_team(action.player, action.move.player):
                raise Exception(
                    f"Player {action.player} can not gift opponent player {action.move.player}")

        if action.move_type == MoveType.declare:
            # Ensure card_player_map contains the cards from the semi-suit.
            semisuit_cards = set(Card.get_semisuit(action.move.semisuit))
            mapped_cards = set(action.move.card_player_map.keys())

            unmapped_cards = semisuit_cards - mapped_cards
            extra_mapped_cards = mapped_cards - semisuit_cards

            if len(unmapped_cards) > 0 or len(extra_mapped_cards) > 0:
                unmapped_cards_error = "unmapped cards {" + \
                    ", ".join(unmapped_cards) + "}"
                extra_mapped_cards_error = "extra mapped cards {" + ", ".join(
                    extra_mapped_cards) + "}"
                mapping_errors = " and ".join(
                    [unmapped_cards_error, extra_mapped_cards_error])
                raise Exception(
                    f"Player {action.player} played invalid declare for {action.move.semisuit}, with {mapping_errors}")

            # Ensure opponent players' cards are not being declared.
            for player in action.move.card_player_map.values():
                if not self.same_team(action.player, player):
                    raise Exception(
                        f"Player {action.player} can not declare cards of opponent player {action.move.player}")

    def action(self, action: Action):

        self.ensure_legal(action)
        self.actions.append(action)

        # TODO: Write action result as well

        {
            MoveType.ask: self._ask_action,
            MoveType.gift: self._gift_action,
            MoveType.declare: self._declare_action,
        }.get(action.move_type)(action)

    # Private methods

    def _ask_action(self, action: Action):

        if action.move.card in self.player_hand(action.move.player):
            self._move_card(action.move.card,
                            action.move.player, action.player)

        else:
            self.turn = action.move.player

    def _gift_action(self, action: Action):

        self.turn = action.move.player

    def _declare_action(self, action: Action):
        if not all([self.player_has(player, card) for card, player in action.move.card_player_map.items()]):
            self.scores[self.team(action.player)] -= 1

            for card in Card.get_semisuit(action.move.semisuit):
                card_player = self.card_loc(card)
                if card_player is None:
                    break
                if not self.same_team(action.player, card_player):
                    self.turn = card_player

        else:
            self.scores[self.team(action.player)] += 1

        for card, player in action.move.card_player_map.items():
            self.player_hands[player].remove(card)

    def _move_card(self, card, from_player, to_player):
        self.player_hands[from_player].remove(card)
        self.player_hands[to_player].append(card)

    def serialize(self):
        d = {}
        d["player_hands"] = self.player_hands
        d[""]


def nbrs(*cards: List[Card]):
    return set([related_card for card in cards for related_card in [card.next, card.prev]])
