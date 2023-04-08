from collections import defaultdict

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from app.connection_manager import ConnectionManager
from app.exceptions import GameError
from app.game import GameState

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True))

manager = ConnectionManager()
games = defaultdict(GameState)


@app.get("/healthz")
async def health():
    return "OK"


@app.websocket("/play/{game_id}")
async def play(websocket: WebSocket, game_id: str, verbose: bool = False):
    connection = await manager.connect(game_id, websocket, verbose)
    if not connection:
        return

    active_game = games[game_id]
    player_id = active_game.get_next_player_id(game_id)
    await manager.broadcast(game_id, f"player {player_id} connected", verbose_only=True)
    await manager.wait_for_connections(game_id)
    await connection.send_message("all players conencted", verbose_only=True)
    try:
        while True:
            if not active_game.live:
                await manager.wait_for_connections(game_id)

            await connection.send_json(active_game.get_state(player_id))
            data = await websocket.receive_text()
            try:
                print(f"got bid of {int(data)} from {player_id=}")
            except ValueError:
                print(f"did not receive int from {player_id=}")
                continue

            try:
                round_end = active_game.queue_bid(player_id, int(data))
            except GameError as e:
                print(f"could not process bid due to error: {repr(e)}")
                continue

            await connection.send_message("waiting for opponent's bid", verbose_only=True)
            await manager.open_lock(game_id, player_id)
            manager.reset_lock(game_id)
            await connection.send_message("received opponent's bid", verbose_only=True)

            if round_end:
                active_game.get_bounty()
                await manager.broadcast(
                    game_id, active_game.last_round_details(), verbose_only=True
                    )

    except WebSocketDisconnect:
        manager.disconnect(game_id, connection)
        active_game.remove_player(player_id)
        await manager.broadcast(game_id, f"info: player {player_id} left", verbose_only=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
