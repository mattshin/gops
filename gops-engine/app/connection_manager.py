from collections import defaultdict

from fastapi import WebSocket

CONNECTION_MAX_GROUP_SIZE = 2

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)

    async def connect(self, group_id: str, websocket: WebSocket):
        await websocket.accept()
        if len(self.active_connections[group_id]) >= CONNECTION_MAX_GROUP_SIZE:
            await websocket.close(code=1000, reason=f"Maximum connections made for {group_id=}")
            return False
        self.active_connections[group_id].append(websocket)
        return True

    def disconnect(self, group_id: str, websocket: WebSocket):
        self.active_connections[group_id].remove(websocket)

    async def broadcast(self, group_id: str, message: str):
        for connection in self.active_connections[group_id]:
            await connection.send_text(message)