import uuid
from datetime import datetime

from aiohttp import MultipartReader, BodyPartReader
from aiohttp_apispec import docs, response_schema

from drive_server.app.api.files.schemas import FilesUploadSchema
from drive_server.app.api.files.utils import make_upload_callback
from drive_server.app.base.application import View
from drive_server.app.store.s3.accessor import S3Accessor
from drive_server.app.store.websockets.websocket_accessor import WebSocketAccessor, WebSocketMessageKind
from drive_server.app.web.response import json_response
from drive_server.app.web.mixins import AuthRequiredMixin


class FilesUploadView(AuthRequiredMixin ,View):
    @docs(tags=['files'], summary='S3 file upload view')
    @response_schema(FilesUploadSchema, 200)
    async def post(self):
        upload_id = self.request.headers.get('x-upload-id')
        total_size = self.request.headers.get('Content-Length')
        multipart_reader: MultipartReader = await self.request.multipart()
        body_part_reader: BodyPartReader = await multipart_reader.next()
        filename: str = body_part_reader.filename
        callback = make_upload_callback(self.store, self.request.user_id, upload_id, total_size)
        s3: S3Accessor = self.store.s3
        ws: WebSocketAccessor = self.store.ws
        await s3.upload(key=filename, reader=body_part_reader, upload_callback=callback)
        await ws.push(self.request.user_id, WebSocketMessageKind.UPLOAD_FINISH, {'upload_id': upload_id})
        return json_response(data={
            'upload_id': upload_id,
            'filename': filename,
            'size': total_size,
            'created': datetime.now(),
        },  schema=FilesUploadSchema)
