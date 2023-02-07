from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-testing',
            prep_time=10,
            prep_time_unit='minutes',
            servings=5,
            servings_unit='servings',
            prep_steps='Recipe Prep steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('prep_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_prep_steps_is_html_is_false_by_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-testing',
            prep_time=10,
            prep_time_unit='minutes',
            servings=5,
            servings_unit='servings',
            prep_steps='Recipe Prep steps',
        )
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.prep_steps_is_html)

    def test_recipe_prep_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.prep_steps_is_html,
            msg='prep_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='is_published is not False',
        )

    def test_recipe_str_representation(self):
        needed_str = 'Testing Str Representation'
        self.recipe.title = needed_str
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed_str,
            msg=f"Recipe str representation must be '{needed_str}',"
                f" but '{self.recipe}' was received",
        )
