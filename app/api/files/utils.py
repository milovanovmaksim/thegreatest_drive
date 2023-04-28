from uuid import UUID

from drive_server.app.store.store import Store
from drive_server.app.store.websockets.websocket_accessor import WebSocketAccessor, WebSocketMessageKind


def make_upload_callback(store: Store, user_id: str, upload_id: UUID, total_size: int):
    async def upload_callback(uploaded_size: int):
        ws: WebSocketAccessor = store.ws
        kind: str = WebSocketMessageKind.UPLOAD_PROGRESS
        data = {'upload_id': upload_id, 'total_size': total_size}
        await ws.push(user_id, kind, data)
    return upload_callback
