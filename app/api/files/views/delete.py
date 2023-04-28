from aiohttp_apispec import docs, response_schema, json_schema

from drive_server.app.base.application import View
from drive_server.app.web.response import json_response
from drive_server.app.api.files.schemas import FilesDeleteSchema
from drive_server.app.base.schemas import EmptyResponseSchema
from drive_server.app.store.s3.accessor import S3Accessor
from drive_server.app.web.mixins import AuthRequiredMixin


class FilesDeleteView(AuthRequiredMixin, View):
    @docs(tags=['files'], summary='Delete file by key')
    @json_schema(FilesDeleteSchema)
    @response_schema(EmptyResponseSchema, 200)
    async def post(self):
        s3_accessor: S3Accessor = self.store.s3
        data = self.body
        key: str = data.get('key')
        files = await s3_accessor.delete_object(key)
        return json_response(schema=EmptyResponseSchema)

