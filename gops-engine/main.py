from collections import defaultdict

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from app.connection_manager import ConnectionManager
from app.game import GameState

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True))

manager = ConnectionManager()
games = defaultdict(GameState)


@app.get("/healthz")
async def health():
    return "OK"


@app.websocket("/play/{game_id}")
async def play(websocket: WebSocket, game_id):
    if not await manager.connect(game_id, websocket):
        return

    active_game = games[game_id]
    player_id = active_game.get_next_player_id(game_id)
    await manager.broadcast(game_id, f"info: player {player_id} connected")
    await manager.wait_for_connections(game_id)
    await websocket.send_text("info: all players conencted")
    try:
        while True:
            if not active_game.live:
                await manager.wait_for_connections(game_id)

            await websocket.send_json(active_game.get_state(player_id))
            data = await websocket.receive_text()
            try:
                print(f"got bid of {int(data)} from {player_id=}")
            except ValueError:
                print(f"did not receive int from {player_id=}")
                continue

            round_end = active_game.queue_bid(player_id, int(data))
            await manager.open_lock(game_id, player_id)

            if round_end:
                active_game.get_bounty()
                await manager.broadcast(
                    game_id, f"info: {active_game.last_round_details()}"
                    )
    except WebSocketDisconnect:
        manager.disconnect(game_id, websocket)
        active_game.remove_player(player_id)
        await manager.broadcast(game_id, f"info: player {player_id} left")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
