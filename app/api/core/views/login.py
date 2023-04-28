from uuid import uuid4

from aiohttp_apispec import docs, json_schema, response_schema
from aiohttp_session import new_session, Session
from aiohttp.web import Response

from drive_server.app.base.application import View
from drive_server.app.web.response import json_response, error_json_response
from drive_server.app.api.core.schemas import LoginRequestSchema
from drive_server.app.config.dataclasses import UserConfigSection
from drive_server.app.base.schemas import EmptyResponseSchema


class CoreLoginView(View):
    @docs(tags=["core"], summary="Login", description="Login")
    @json_schema(LoginRequestSchema)
    @response_schema(EmptyResponseSchema, 200)
    async def post(self):
        data = self.body
        username = data['username']
        password = data['password']
        user_config: UserConfigSection = self.config.user
        if any((username != user_config.username, password != user_config.password)):
            return error_json_response(http_status=403, status="Forbidden", message="username or password is incorrect")
            
        session = await new_session(self.request)
        session["user"] = {
            'id': str(uuid4())
        }
        return json_response(EmptyResponseSchema)
