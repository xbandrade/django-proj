from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()  # A recipe is needed for this test
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_doesnt_load_unpublished_recipes(self):
        self.make_recipe(is_published=False)  # A recipe is needed
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_category_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_doesnt_load_unpublished_recipes(self):
        recipe = self.make_recipe(is_published=False)  # A recipe is needed
        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'Category Test'
        # A recipe is needed for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category',
                                           kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

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
