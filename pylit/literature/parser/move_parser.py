import re
from ..cards import *
from ..game import *

def parse_card(description: str):
    m = re.match(r"^\s*(\w+)\s+of\s+(\w+)\s*$", description)
    if m is None:
        raise Exception(f"'{description}' can not be parsed as a card")

    rank_description = m.group(1)
    suit_description = m.group(2)

    try:
        return Card(Suit[suit_description.lower()], Rank[rank_description.lower()])
    except:
        raise Exception(f"'{description}' can not be parsed as a card")


def parse_semisuit(description: str):
    m = re.match(r"^\s*(\w+)\s+of\s+(\w+)\s*$", description)
    if m is None:
        raise Exception(f"'{description}' can not be parsed as a semisuit")

    suit_half_description = m.group(1)
    suit_description = m.group(2)

    try:
        return SemiSuit(Suit[suit_description.lower()], SuitHalf[suit_half_description.lower()])
    except:
        raise Exception(f"'{description}' can not be parsed as a semisuit")


def parse_move(description: str):

    # Try to parse as ask move
    m = re.match(r"^\s*ask\s+(\d)\s+for(.*)$", description)
    if m is not None:

        player = int(m.group(1))
        card_description = m.group(2)
        card = parse_card(card_description)

        return AskMove(player=player, card=card)

    # Try to parse as declare move
    m = re.match(
        r"^\s*declare\s+((?:\w+)\s+of\s+(?:\w+))\s*:?\s*((?:\s*\d)*)\s*$", description)

    if m is not None:
        semisuit = parse_semisuit(m.group(1))
        players = map(int, m.group(2).split())
        declare_map = {}
        for card, player in zip(Card.get_semisuit(semisuit), players, strict=True):
            declare_map[card] = player

        return DeclareMove(semisuit, declare_map)

    # Try to parse as gift move
    m = re.match(r"\s*gift\s*(\d)\s*", description)

    if m is not None:
        player = int(m.group(1))

        return GiftMove(player)

    raise Exception(f"\"{description}\" can not be parsed as a move")
