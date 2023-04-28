from aiohttp_apispec import docs, response_schema

from drive_server.app.api.files.schemas import FilesSchema
from drive_server.app.base.application import View
from drive_server.app.web.response import json_response
from drive_server.app.store.s3.accessor import S3Accessor
from drive_server.app.web.mixins import AuthRequiredMixin


class FilesListView(AuthRequiredMixin, View):
    @docs(tags=['files'], summary='S3 files list view')
    @response_schema(FilesSchema, 200)
    async def get(self):
        s3_accessor: S3Accessor = self.store.s3
        files = await s3_accessor.list_objects()
        return json_response(data={"items": files}, schema=FilesSchema)
