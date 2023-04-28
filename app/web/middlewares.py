import json
import uuid

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp_apispec.middlewares import validation_middleware
from aiohttp_session import get_session
from aiohttp.web import json_response

from drive_server.app.base.application import Application, Request
from drive_server.app.web.response import error_json_response


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if not session.new:
        user_id = session['user']['id']
        request.user_id = user_id
    return await handler(request)


@middleware
async def error_handling_middleware(request: Request, handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status='bad request',
            message=str(e),
            data=json.loads(e.text))
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=e.reason,
            message=str(e))
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message="internal server error")


def setup_middlewares(app: Application):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
    