from literature import Game, Action
from literature.viz.grid import viz
from literature.parser import parse_move

from traceback import print_exc


g = Game(4)


while True:
    print(viz(g))

    try:
        action = Action(player=g.turn, move=parse_move(input()))
        print(f"taking action {action}")
        g.action(action)
    except Exception as e:
        print(f"Failed: {e}")
        print_exc()
