from aiohttp import web
from .db import setup_mongo
from .models import ensure_indexes
from .views import routes
from .config import Config


def init(config):
    app = web.Application()
    app['config'] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    config = Config()
    app = init(config)
    web.run_app(app, port=config.PORT)
