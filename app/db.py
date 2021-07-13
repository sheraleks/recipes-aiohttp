import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from umongo import MotorAsyncIOInstance


instance = MotorAsyncIOInstance()


async def init_mongo(app, mongodb_uri):
    loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(mongodb_uri, io_loop=loop)
    return conn.get_database()


async def setup_mongo(app):
    config = app['config']
    app['db'] = await init_mongo(app, config.MONGODB_URI)
    instance.init(app['db'])

    async def close_mongo(app):
        app['db'].client.close()

    app.on_cleanup.append(close_mongo)
