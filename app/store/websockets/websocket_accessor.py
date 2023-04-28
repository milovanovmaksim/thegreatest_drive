from enum import Enum
from typing import Any, Optional
import json

from aiohttp.web import WebSocketResponse

from drive_server.app.base.application import Request
from drive_server.app.base.connect_accessor import BaseAccessor


class WSConnectionNotFound(Exception):
    pass


class WebSocketMessageKind(Enum):
    INITIAL = 'INITIAL'
    UPLOAD_PROGRESS = 'UPLOAD_PROGRESS'
    UPLOAD_FINISH = 'UPLOAD_FINISH'


class WebSocketAccessor(BaseAccessor):
    def _init_(self):
        self._connections: dict[str, Any] = {}

    async def handle(self, request: Request):
        user_id = request.user_id
        await self.close(user_id)
        ws_response: WebSocketResponse = WebSocketResponse()
        await ws_response.prepare(request)
        self._connections[user_id] = ws_response
        await self.push(user_id, WebSocketMessageKind.INITIAL)
        await self.read(user_id)
        return ws_response


    async def close(self, _id: str):
        try:
            connection = self._connections.pop(_id)
            await connection.close()
        except KeyError:
            pass
        

    async def push(self, user_id: str, kind: WebSocketMessageKind, data: Optional[dict] = {}):
        data.update({'kind': kind.value})
        data: str = json.dumps(data)
        await self._push(user_id, data)

    async def read(self, user_id: str):
        async for message in self._connections.get(user_id):
            print('message', message)

    async def _push(self, _id: str, data: str):
        connection: WebSocketResponse = self._connections.get(_id)
        if connection is None:
            raise WSConnectionNotFound(f"WS connection not found for user {_id}")
        await connection.send_str(data)
