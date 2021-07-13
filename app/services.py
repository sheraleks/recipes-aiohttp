from datetime import datetime
from typing import AsyncIterable, Dict
from aiohttp.web_exceptions import HTTPNotFound
from bson import ObjectId
from .models import User, Recipe, RecipeWithUser
from pymongo import DESCENDING, ASCENDING

# TODO: Проверка лайков
async def create_recipe(data):
    recipe = Recipe(**data)
    author_id = data['author_id']
    user = await User.find_one({'_id': author_id, 'status': 'active'})
    if not user:
        raise HTTPNotFound(reason='author not found')
    user.recipes_count += 1
    await user.commit()
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

async def find_recipe(recipe_id):
    recipe = await Recipe.find_one({'_id': recipe_id, 'status': 'active'})
    if not recipe:
        raise HTTPNotFound()
    user = await find_user(recipe.author_id)
    recipe_with_user = RecipeWithUser()
    recipe_with_user.author_id = user.id
    recipe_with_user.author_nickname = user.nickname
    recipe_with_user.status = user.status
    recipe_with_user.created_date = recipe.created_date
    recipe_with_user.name = recipe.name
    if recipe.description is not None:
        recipe_with_user.description = recipe.description
    if recipe.cooking_steps is not None:
        recipe_with_user.cooking_steps = recipe.cooking_steps
    if recipe.result_photo is not None:
        recipe_with_user.result_photo = recipe.result_photo
    if recipe.dish_type is not None:
        recipe_with_user.dish_type = recipe.dish_type
    if recipe.likes is not None:
        recipe_with_user.likes = recipe.likes
    if recipe.likes_count is not None:
        recipe_with_user.likes_count = recipe.likes_count
    if recipe.hashtags is not None:
        recipe_with_user.hashtags = recipe.hashtags
    recipe_with_user.status = recipe.status
    return recipe_with_user


# TODO: проверка корректности передачи параметров
async def list_recipes(data):
    filter = {'status': 'active'}
    if 'hashtag' in data: filter['hashtags'] = data['hashtag']
    if 'name_part' in data: filter['name'] = {'$regex': data['name_part'], '$options': '$i'}
    if 'author_id' in data: filter['_id'] = data['author_id']
    if 'with_photo' in data: filter['result_photo'] = {'$exists': data['with_photo']}
    result = Recipe.find(filter)
    if 'sort_by' in data:
        sort_order = ASCENDING
        if 'sort_order' in data and data['sort_order'] != 'ascending': sort_order=DESCENDING
        result = result.sort([(data['sort_by'], sort_order)])
    return result

'''
async def find_user_recipe(recipe_id):
    recipe = await Recipe.find_one({'_id': recipe_id, 'status': 'active'})
    if not recipe:
        raise HTTPNotFound()
    recipe.__class__ = RecipeUser
    user = await User.find_one({'_id': recipe.author_id})
    recipe.author_nickname = user.nickname
    recipe.author_status = user.status
    return recipe
'''

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