from datetime import datetime
from typing import AsyncIterable, Dict
from aiohttp.web_exceptions import HTTPNotFound
from bson import ObjectId
from .models import User, Recipe
from pymongo import DESCENDING, ASCENDING

async def create_recipe(data):
    recipe = Recipe(**data)
    await recipe.commit()
    return recipe

async def create_user(data):
    user = User(**data)
    await user.commit()
    return user

async def list_top_users():
    return User.find({'status': 'active'}).sort([("recipes_count", DESCENDING)]).limit(10)

async def find_user(user_id):
    user = await User.find_one({'_id': user_id, 'status': 'active'})
    if not user:
        raise HTTPNotFound()
    return user

'''
async def find_items() -> AsyncIterable[Item]:
    return Item.find({})


async def create_item(data: Dict) -> Item:
    item = Item(**data)
    await item.commit()
    return item


async def find_item(item_id: ObjectId) -> Item:
    item = await Item.find_one({'_id': item_id})
    if not item:
        raise HTTPNotFound()

    return item


async def update_item(item_id: ObjectId, data: Dict) -> Item:
    item = await find_item(item_id)

    item.update(data)
    item.updated_time = datetime.utcnow()
    await item.commit()

    return item


async def delete_item(item_id: ObjectId) -> None:
    item = await find_item(item_id)
    await item.delete()
'''