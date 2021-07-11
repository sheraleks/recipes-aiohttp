from marshmallow import Schema
from .models import User, Recipe


UserSchema: Schema = User.schema.as_marshmallow_schema()
RecipeSchema: Schema = Recipe.schema.as_marshmallow_schema()

class UserNoPassSchema(UserSchema):
    class Meta:
        exclude = ['password']


'''
class UpdateItemSchema(ItemSchema):
    class Meta:
        fields = ['name']
'''