from aiohttp.test_utils import unittest_run_loop
from app.models import User, Recipe
from tests import AppTestCase


class UserListTestCase(AppTestCase):

    @unittest_run_loop
    async def test_list_users(self):
        user1 = User(nickname='test1', password='test1')
        await user1.commit()
        user2 = User(nickname='test2', password='test2')
        await user2.commit()

        resp = await self.client.get("/users")
        assert resp.status == 200
        users = await resp.json()
        assert len(users) == 2


class RecipeListTestCase(AppTestCase):

    @unittest_run_loop
    async def test_list_users(self):
        author_id = '60ead8d8910b3793218d65d7'
        recipe1 = Recipe(author_id=author_id, name='уха', dish_type='суп')
        await recipe1.commit()

        recipe2 = Recipe(author_id=author_id, name='свинина', dish_type='второе')
        await recipe2.commit()

        resp = await self.client.get("/recipes")
        assert resp.status == 200
        recipes = await resp.json()
        assert len(recipes) == 2


class UserCreateTestCase(AppTestCase):

    @unittest_run_loop
    async def test_create_user(self):
        data = {
            'nickname': 'test3',
            'password': 'test3'
        }
        resp = await self.client.post("/users", json=data)
        assert resp.status == 201

        user = await User.find_one({'nickname': data['nickname']})
        assert user.nickname == data['nickname']


class UserGetTestCase(AppTestCase):

    @unittest_run_loop
    async def test_get_user(self):
        user1 = User(nickname='test21', password='test1')
        await user1.commit()

        found = await User.find_one({'nickname': user1.nickname})
        assert found.nickname == user1.nickname


class RecipeGetTestCase(AppTestCase):

    @unittest_run_loop
    async def test_get_user(self):
        author_id = '60ead8d8910b3793218d65d7'
        recipe1 = Recipe(author_id=author_id, name='уха', dish_type='суп')
        await recipe1.commit()

        found = await Recipe.find_one({'_id': recipe1.id})
        assert found.id == recipe1.id