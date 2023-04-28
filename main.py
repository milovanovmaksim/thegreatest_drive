import os
import pathlib

import aiohttp_cors
from aiohttp import web
from aiohttp_session import setup as setup_aiohttp_session, SimpleCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec


from common.utils import show_api_url
from drive_server.app.base.application import Application
from drive_server.app.config.dataclasses import create_config
from drive_server.app.store.store import Store
from drive_server.app.web.middlewares import setup_middlewares
from drive_server.app.web.routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent


def create_app() -> Application:
    app: Application = web.Application()
    app.config = create_config(app)
    # TODO: настроить базовую конфигурацию для логгера
    # TODO: присвоить app.logger новый логгер
    app.store = Store(app)
    app.cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        )
    })

    setup_aiohttp_session(app, SimpleCookieStorage(cookie_name='sessionid'))
    setup_routes(app)
    setup_aiohttp_apispec(app, static_path='/swagger_static', title='kts-drive', url='/docs/json', swagger_path='/docs')
    setup_middlewares(app)
    return app


if __name__ == '__main__':
    show_api_url()
    print(f'Интерфейс S3 доступен по {os.environ.get("MINIO_SERVER_URL")},'
          f' логин: {os.environ.get("MINIO_ROOT_USER")}, пароль: {os.environ.get("MINIO_ROOT_PASSWORD")}')
    web.run_app(create_app(), port=8888)
