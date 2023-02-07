from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_doesnt_load_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)  # A recipe is needed
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipe(self):
        needed_title = 'Detail page - This loads one recipe'
        # A recipe is needed for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)
