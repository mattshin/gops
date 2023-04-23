import asyncio
from collections import defaultdict

from fastapi import WebSocket

CONNECTION_MAX_GROUP_SIZE = 2


class Connection:
    websocket = None
    verbose = False

    def __init__(self, websocket, verbose):
        self.websocket = websocket
        self.verbose = verbose

    async def send_message(self, msg: str, verbose_only: bool = False):
        if not verbose_only or (verbose_only and self.verbose):
            await self.websocket.send_json({"info": verbose_only, "msg": msg})

    async def send_json(self, data, verbose_only: bool = False):
        if not verbose_only or (verbose_only and self.verbose):
            data["info"] = verbose_only
            await self.websocket.send_json(data)

    async def close(self, reason:str = "Closed by server"):
        self.websocket.close(code=1000, reason=reason)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)
        self.locks = defaultdict(set)

    async def connect(self, group_id: str, websocket: WebSocket, verbose=False):
        await websocket.accept()
        if len(self.active_connections[group_id]) >= CONNECTION_MAX_GROUP_SIZE:
            await websocket.close(
                code=1000, reason=f"Maximum connections made for {group_id=}"
            )
            return None
        connection = Connection(websocket, verbose)
        self.active_connections[group_id].append(connection)
        return connection

    def disconnect(self, group_id: str, connection: Connection):
        self.active_connections[group_id].remove(connection)
    
    def disconnect_all(self, group_id: str, reason="Closed by server"):
        for connection in self.active_connections[group_id]:
            connection.close(reason)
        self.active_connections[group_id] = list()

    async def broadcast(self, group_id: str, message: str, verbose_only: bool = False):
        for connection in self.active_connections[group_id]:
            await connection.send_message(message, verbose_only=verbose_only)

    async def broadcast_json(self, group_id: str, data: dict, verbose_only: bool = False):
        for connection in self.active_connections[group_id]:
            await connection.send_json(data, verbose_only=verbose_only)

    async def wait_for_connections(
        self, group_id, num_connections=CONNECTION_MAX_GROUP_SIZE
    ):
        num_connections = max(num_connections, CONNECTION_MAX_GROUP_SIZE)
        while len(self.active_connections[group_id]) < num_connections:
            await asyncio.sleep(1)
        return

    async def open_lock(
        self, lock_id, connection_id, num_connections=CONNECTION_MAX_GROUP_SIZE
    ):
        num_connections = max(num_connections, CONNECTION_MAX_GROUP_SIZE)
        if connection_id not in range(num_connections):
            raise RuntimeError(f"{connection_id=} too high")

        self.locks[lock_id].add(connection_id)
        while 0 < len(self.locks[lock_id]) < num_connections:
            await asyncio.sleep(1)

        return True

    async def reset_lock(self, lock_id):
        self.locks[lock_id] = set()
