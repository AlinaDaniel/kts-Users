from typing import Optional

from aiohttp.web import Application as AiohttpApplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequest

from app.store import setup_accessors
from app.store.crm.accessor import CrmAccessor
from app.web.config import Config, setup_config
from app.web.middlewars import setup_middlewares
from app.web.routes import setup_routes
from aiohttp_apispec import setup_aiohttp_apispec

class Application(AiohttpApplication):
    config: Optional[Config]= None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None

class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app()
class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request
app = Application()

# настройка приложения
def run_app():
    # app("database")={}
    setup_config(app)
    # пути приложения и связь с вьюхами
    setup_routes(app)
    # валидация и генерация сваги
    setup_aiohttp_apispec(app, title='CRM Application', url='/docs/json', swagger_path='/docs')
    # обработка ошибок и валидация
    setup_middlewares(app)
    # бд
    setup_accessors(app)
    # запуск
    aiohttp_run_app(app)
