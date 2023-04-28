from drive_server.app.base.store import BaseStore
from drive_server.app.store.s3.accessor import S3Accessor
from drive_server.app.store.websockets.websocket_accessor import WebSocketAccessor


class Store(BaseStore):
    def _init_(self):
        self.s3 = S3Accessor(self.app)
        self.ws = WebSocketAccessor(self.app)

    @property
    def accessors(self):
        yield self.s3
