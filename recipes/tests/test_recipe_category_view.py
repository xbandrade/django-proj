from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
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
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)
