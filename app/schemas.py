from .models import User, Recipe


UserSchema = User.schema.as_marshmallow_schema()
RecipeSchema = Recipe.schema.as_marshmallow_schema()


class UserNoPassSchema(UserSchema):
    class Meta:
        exclude = ['password']


class RecipeNoStepsSchema(RecipeSchema):
    class Meta:
        exclude = ['cooking_steps']


class UserRecipeSchema(UserSchema):
    class Meta:
        exclude = ['password', 'favorites', 'recipes_count']

