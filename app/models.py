from aiohttp import web
from datetime import datetime
from umongo import Document, fields
from .db import instance


@instance.register
class User(Document):
    nickname = fields.StrField(required=True, unique=True)
    password = fields.StrField(required=True)
    status = fields.StrField(default='active')
    favorites = fields.ListField(fields.ObjectIdField())
    recipes_count = fields.IntField(default=0)


@instance.register
class Recipe(Document):
    author_id = fields.ObjectIdField(required=True)
    created_date = fields.DateTimeField(default=datetime.utcnow)
    name = fields.StrField(required=True)
    description = fields.StrField()
    cooking_steps = fields.ListField(fields.StrField(), required=True)
    result_photo = fields.StrField()
    dish_type = fields.StrField(required=True)
    likes = fields.ListField(fields.ObjectIdField())
    likes_count = fields.IntField(default=0)
    hashtags = fields.ListField(fields.StrField())
    status = fields.StrField(default='active')


async def ensure_indexes(app: web.Application) -> None:
    await User.ensure_indexes()
    await Recipe.ensure_indexes()
