from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson import ObjectId
from bson.objectid import InvalidId
from umongo import ValidationError
from . import schemas, services


routes = web.RouteTableDef()


def validate_object_id(object_id):
    try:
        object_id = ObjectId(object_id)
    except InvalidId:
        raise HTTPBadRequest(reason='Invalid id.')
    return object_id


@routes.get('/users')
async def list_top_users(request):
    schema = schemas.UserNoPassSchema()
    users = await services.list_top_users()
    return web.json_response([schema.dump(user)[0] async for user in users], status=200)


@routes.get('/recipes')
async def list_recipes(request):
    recipes = await services.list_recipes(request.rel_url.query)
    schema_recipe = schemas.RecipeNoStepsSchema()
    recipes = [schema_recipe.dump(recipe)[0] async for recipe in recipes]
    return web.json_response(recipes, status=200)


@routes.post('/users')
async def create_user(request):
    try:
        schema = schemas.UserSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        raise HTTPBadRequest(reason=error.messages)

    user = await services.create_user(data)
    return web.json_response(user.dump(), status=201)


@routes.post('/recipes')
async def create_recipe(request):
    try:
        schema = schemas.RecipeSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        raise HTTPBadRequest(reason=error.messages)

    recipe = await services.create_recipe(data)
    return web.json_response(recipe.dump(), status=201)


@routes.get(r'/users/{user_id:\w{24}}')
async def get_user(request):
    user_id = validate_object_id(request.match_info['user_id'])
    user = await services.find_user(user_id)
    schema = schemas.UserNoPassSchema()
    return web.json_response(schema.dump(user)[0], status=200)


@routes.get(r'/recipes/{recipe_id:\w{24}}')
async def get_recipe(request):
    recipe_id = validate_object_id(request.match_info['recipe_id'])
    recipe = await services.find_recipe(recipe_id)
    user = await services.find_user(recipe.author_id)
    recipe_schema = schemas.RecipeSchema()
    user_schema = schemas.UserRecipeSchema()
    recipe = recipe_schema.dump(recipe)[0]
    recipe['author'] = user_schema.dump(user)[0]
    return web.json_response(recipe, status=200)
