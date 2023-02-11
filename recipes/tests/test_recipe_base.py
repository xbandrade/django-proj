from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='12345678',
                    email='user@gmail.com',
                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    prep_time=10,
                    prep_time_unit='minutes',
                    servings=5,
                    servings_unit='servings',
                    prep_steps='Recipe Prep steps',
                    prep_steps_is_html=False,
                    is_published=True,
                    ):
        if not category_data:
            category_data = {}
        if not author_data:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            prep_time=prep_time,
            prep_time_unit=prep_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            prep_steps=prep_steps,
            prep_steps_is_html=prep_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qt=10):
        recipes = []
        for i in range(qt):
            kwargs = {'author_data': {'username': f'user{i}'},
                      'slug': f'slug{i}',
                      'title': f'Recipe Title {i}'}
            recipe = self.make_recipe(**kwargs)  # A recipe is needed
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
