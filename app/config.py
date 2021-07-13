import os

MONGODB_HOST = 'localhost'
IN_DOCKER = bool(os.environ.get('IN_DOCKER', False))
if IN_DOCKER:
    MONGODB_HOST = 'mongo'


class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI', f'mongodb://{MONGODB_HOST}:27017/recipes')
    PORT = int(os.environ.get('PORT', 8080))
    DEBUG = bool(os.environ.get('DEBUG', False))


class TestConfig(Config):
    MONGODB_URI = os.environ.get('MONGODB_TEST_URI', f'mongodb://{MONGODB_HOST}:27017/recipes_test')
    DEBUG = True