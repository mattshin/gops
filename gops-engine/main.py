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
    await manager.broadcast(game_id, "info: all players conencted, starting game")
    try:

        await manager.wait_for_connections(game_id)
        await manager.broadcast(game_id, "info: all players conencted, starting game")
        await websocket.send_json(active_game.get_state(player_id))
        while True:
            if not active_game.live:
                await manager.wait_for_connections(game_id)

            data = await websocket.receive_text()

            if active_game.queue_bid(player_id, int(data)):
                active_game.get_bounty()
                await manager.broadcast(
                    game_id, active_game.last_round_details() 
                )
    except WebSocketDisconnect:
        manager.disconnect(game_id, websocket)
        active_game.remove_player(player_id)
        await manager.broadcast(game_id, f"info: player {player_id} left the game")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
