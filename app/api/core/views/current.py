from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_session import get_session
from aiohttp_apispec import docs, response_schema

from drive_server.app.web.response import json_response, error_json_response
from drive_server.app.base.application import View
from drive_server.app.base.schemas import EmptyResponseSchema



class CoreCurrentView(View):
    @docs(tags=["core"], summary="user authorization check", description="Check the user is logged in")
    @response_schema(EmptyResponseSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        if session.new:
            raise HTTPUnauthorized()
        return json_response(EmptyResponseSchema)
