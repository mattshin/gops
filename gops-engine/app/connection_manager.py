import asyncio
from collections import defaultdict

from fastapi import WebSocket

CONNECTION_MAX_GROUP_SIZE = 2


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)
        self.locks = defaultdict(set)

    async def connect(self, group_id: str, websocket: WebSocket):
        await websocket.accept()
        if len(self.active_connections[group_id]) >= CONNECTION_MAX_GROUP_SIZE:
            await websocket.close(
                code=1000, reason=f"Maximum connections made for {group_id=}"
            )
            return False
        self.active_connections[group_id].append(websocket)
        return True

    def disconnect(self, group_id: str, websocket: WebSocket):
        self.active_connections[group_id].remove(websocket)

    async def broadcast(self, group_id: str, message: str):
        for connection in self.active_connections[group_id]:
            await connection.send_text(message)

    async def broadcast_json(self, group_id: str, data: dict):
        for connection in self.active_connections[group_id]:
            await connection.send_json(data)

    async def wait_for_connections(
        self, group_id, num_connections=CONNECTION_MAX_GROUP_SIZE
    ):
        num_connections = max(num_connections, CONNECTION_MAX_GROUP_SIZE)
        while len(self.active_connections[group_id]) < num_connections:
            await asyncio.sleep(1)
        return

    async def open_lock(self, lock_id, connection_id, num_connections=CONNECTION_MAX_GROUP_SIZE):
        num_connections = max(num_connections, CONNECTION_MAX_GROUP_SIZE)
        if connection_id not in range(num_connections):
            raise RuntimeError(f"{connection_id=} too high")

        self.locks[lock_id].add(connection_id)
        while len(self.locks[lock_id]) < num_connections:
            await asyncio.sleep(1)

        return True
