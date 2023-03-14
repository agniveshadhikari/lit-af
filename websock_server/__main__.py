import asyncio
import websockets
import logging
import os
import json

from pylit.literature import Game, Action
from pylit.literature.parser import parse_move


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class LitAF:

    def __init__(self):
        self.conns = list()
        self.is_gaming = False

    def get_player_id(self, ws):
        return self.conns.index(ws)

    async def handle_connection(self, ws):
        logger.info("New connection")
        self.conns.append(ws)
        await self._broadcast_raw(f"{len(self.conns)} players joined")
        async for message in ws:
            try:
                await self._handle_message(ws, message)
            except Exception as e:
                logger.exception(e)
                await ws.send(f"Bhai {e}")
        logger.info("Disconnected")
        await self._handle_disconnection(ws)

    async def _handle_message(self, ws, message):

        message = json.loads(message)
        logger.info("Received message", message)
        if message["type"] == "control" and message["action"] == "start" and self.get_player_id(ws) == 0 and not self.is_gaming:
            await self._handle_game_start()
            return

        if message["type"] == "game" and self.game.turn == self.get_player_id(ws):
            move = parse_move(message["action"])
            self.game.action(Action(self.get_player_id(ws), move))

            # if self.game.ended:
            #     await self._broadcast_win()
            #     await self._terminate_connections()
            #     self._reinit()
            #     return

            await self._send_player_hands()
            await self._broadcast_raw(f"Player {self.game.turn}'s turn")
            return

        raise Exception("Invalid message")

    async def _handle_game_start(self):
        self.game = Game(len(self.conns))
        self.is_gaming = True
        await self._broadcast_raw("Game started")
        await self._send_player_hands()
        await self._broadcast_raw(f"Player {self.game.turn}'s turn")

    async def _send_player_hands(self):
        """
        Sends the current hand for all the players.
        """
        for player_idx, ws in enumerate(self.conns):
            hand = self.game.player_hand(player_idx)

            await ws.send(", ".join(map(lambda card: str(card), hand)))

    async def _handle_disconnection(self, ws):

        player_idx = self.conns.index(ws)
        del self.conns[ws]
        await self._broadcast_raw(f"Player {player_idx} disconnected")

    async def _broadcast_raw(self, message):
        for conn in self.conns.copy():
            try:
                await conn.send(message)
            except Exception as e:
                logger.exception(
                    f"Failed broadcasting to connection {conn}", e)


async def main():

    logger.debug("start of script")
    room = LitAF()
    server = None
    if False:
        server = await websockets.unix_serve(room.handle_connection,
                                             "lit_af.sock")
        os.chmod("lit_af.sock", 0o660)
    else:
        server = await websockets.serve(room.handle_connection,
                                        "localhost",
                                        8088)

    await server.serve_forever()

asyncio.run(main())
