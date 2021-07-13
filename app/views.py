import logging
from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson import ObjectId
from bson.objectid import InvalidId
from umongo import ValidationError
import json
from . import services, schemas

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)

# TODO: через curl запросы работают


def validate_object_id(object_id: str) -> ObjectId:
    try:
        object_id = ObjectId(object_id)
    except InvalidId:
        logger.error(f'invalid id {object_id}')
        raise HTTPBadRequest(reason='Invalid id.')
    return object_id


@routes.get('/users/top')
async def list_top_users(request: web.Request) -> web.Response:
    schema = schemas.UserNoPassSchema()
    users = await services.list_top_users()
    return web.json_response([schema.dump(user)[0] async for user in users], status=200)

# TODO: пагинация, проверка author_id, get запрос
@routes.post('/recipes/list')
async def list_recipes(request: web.Request) -> web.Response:
    try:
        schema = schemas.ListRecipeParamsSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)
    recipes = await services.list_recipes(data)
    schema_recipe = schemas.RecipeNoStepsSchema()
    recipes = [schema_recipe.dump(recipe)[0] async for recipe in recipes]

    return web.json_response({'recipes': recipes, 'page': 1}, status=200)

@routes.post('/users')
async def create_user(request: web.Request) -> web.Response:
    try:
        schema = schemas.UserSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)

    user = await services.create_user(data)
    return web.json_response(user.dump(), status=201)

@routes.post('/recipes')
async def create_recipe(request: web.Request) -> web.Response:
    try:
        schema = schemas.RecipeSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)

    recipe = await services.create_recipe(data)
    return web.json_response(recipe.dump(), status=201)

@routes.get(r'/users/{user_id:\w{24}}')
async def get_user(request: web.Request) -> web.Response:
    user_id = validate_object_id(request.match_info['user_id'])
    user = await services.find_user(user_id)
    schema = schemas.UserNoPassSchema()
    return web.json_response(schema.dump(user)[0], status=200)

@routes.get(r'/recipes/{recipe_id:\w{24}}')
async def get_recipe(request: web.Request) -> web.Response:
    recipe_id = validate_object_id(request.match_info['recipe_id'])
    recipe = await services.find_recipe(recipe_id)
    user = await services.find_user(recipe.author_id)
    recipe_schema = schemas.RecipeNoStepsSchema()
    user_schema = schemas.UserRecipeSchema()
    recipe = recipe_schema.dump(recipe)[0]
    recipe['author'] = user_schema.dump(user)[0]
    return web.json_response(recipe, status=200)

'''
@routes.get(r'/items/{item_id:\w{24}}')
async def get_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])
    item = await services.find_item(item_id)

    return web.json_response(item.dump(), status=200)


@routes.put(r'/items/{item_id:\w{24}}')
async def update_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])

    try:
        schema = schemas.UpdateItemSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)

    item = await services.update_item(item_id, data)

    return web.json_response(item.dump(), status=200)


@routes.delete(r'/items/{item_id:\w{24}}')
async def delete_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])
    await services.delete_item(item_id)

    return web.json_response({}, status=204)
'''