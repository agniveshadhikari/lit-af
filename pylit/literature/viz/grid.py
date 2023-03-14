from ..cards import Suit, Rank, Card


def viz(game):
    # Config
    label_width = 10
    bigsep = "  "
    sep = " "

    def to_width(x): return ("{0: <"+str(label_width)+"}").format(x)

    def format_content(els, sep=" ", bigsep="  "):

        assert len(els) == 12
        assert all(map(lambda el: len(str(el)) == 1, els))

        els = list(map(str, els))

        return sep.join(els[:6]) + bigsep + sep.join(els[6:])

    buf = []

    player_hands = game.player_hands
    card_map = {}

    for i, player in enumerate(player_hands):
        for card in player:
            card_map[card] = i

    buf.append(
        bigsep.join([
            to_width(f"Turn: {game.turn}"),
            format_content(['A', '2', '3', '4', '5', '6',
                            '8', '9', 'T', 'J', 'Q', 'K'])
        ])
    )

    for suit in Suit:
        label = to_width(suit.name)
        content = format_content(
            [card_map.get(Card(suit, rank), " ") for rank in Rank])

        buf.append(
            bigsep.join([
                label,
                content
            ])
        )

    return '\n'.join(buf)
