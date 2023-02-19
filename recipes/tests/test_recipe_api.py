from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response

    def get_recipe_raw_data(self):
        return {
            'title': 'This is a new TITLE test',
            'description': 'This is a new description',
            'prep_time': 1,
            'prep_time_unit': 'Minutes',
            'prep_steps': 'These are the preparation steps',
            'servings': 1,
            'servings_unit': 'Slice',
        }

    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password'),
        )
        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        number_of_recipes = 7
        self.make_recipe_in_batch(number_of_recipes)
        response = self.client.get(reverse('recipes:recipes-api-list'))
        quant_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(
            quant_of_loaded_recipes,
            number_of_recipes
        )

    def test_recipe_api_list_dont_show_unpublished_recipes(self):
        recipe_not_published, _ = self.make_recipe_in_batch(2)
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        category = self.make_category(name='CORRECT CATEGORY')
        category_not_wanted = self.make_category(name='NOT THIS CATEGORY')
        recipes = self.make_recipe_in_batch(10)
        for recipe in recipes:
            recipe.category = category
            recipe.save()
        recipes[0].category = category_not_wanted
        recipes[0].save()
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category.id}'
        ...
        response = self.get_recipe_api_list(api_url)
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_recipe(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        author = access_data.get('user')
        recipe.author = author
        jwt_access_token = access_data.get('jwt_access_token')
        recipe.save()
        new_title = f'The new title updates by {author.username}'
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={
                'title': new_title,
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            response.data.get('title'),
            new_title
        )

    def test_recipe_api_list_user_cant_update_someone_elses_recipe(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        another_user = self.get_auth_data(username='cant_update')
        another_users_jwt_access_token = another_user.get('jwt_access_token')
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {another_users_jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            403,
        )
