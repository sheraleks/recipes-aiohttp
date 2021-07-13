from marshmallow import Schema, fields
from .models import User, Recipe, RecipeWithUser


UserSchema: Schema = User.schema.as_marshmallow_schema()
RecipeSchema: Schema = Recipe.schema.as_marshmallow_schema()
RecipeWithUserSchema: Schema = RecipeWithUser.schema.as_marshmallow_schema()

class UserNoPassSchema(UserSchema):
    class Meta:
        exclude = ['password']

class RecipeNoStepsSchema(RecipeSchema):
    class Meta:
        exclude = ['cooking_steps']

class ListRecipeParamsSchema(Schema):
    hashtag = fields.Str()
    name_part = fields.Str()
    author_id = fields.Str()
    with_photo = fields.Bool()
    sort_by = fields.Str()
    sort_order = fields.Str()


class UserRecipeSchema(UserSchema):
    class Meta:
        exclude = ['password', 'favorites', 'recipes_count']

'''
class UpdateItemSchema(ItemSchema):
    class Meta:
        fields = ['name']
'''