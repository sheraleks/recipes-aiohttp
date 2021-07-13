from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict
from .models import User, Recipe
from pymongo import DESCENDING, ASCENDING


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
    found = await User.find_one({'nickname': user.nickname})
    if found:
        raise HTTPConflict(reason='nickname already taken')
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
    return recipe


async def list_recipes(params):
    filter = {'status': 'active'}
    if 'hashtag' in params: filter['hashtags'] = params['hashtag']
    if 'name_part' in params: filter['name'] = {'$regex': params['name_part'], '$options': '$i'}
    if 'author_id' in params: filter['_id'] = params['author_id']
    if 'with_photo' in params: filter['result_photo'] = {'$exists': params['with_photo']}
    result = Recipe.find(filter)
    if 'sort_by' in params:
        sort_order = ASCENDING
        if 'sort_order' in params and params['sort_order'] != 'ascending': sort_order=DESCENDING
        result = result.sort([(params['sort_by'], sort_order)])
    return result
