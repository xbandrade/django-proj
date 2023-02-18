import os
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.utils.translation import gettext_lazy as _
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest

PER_PAGE = os.environ.get('PER_PAGE', 6)


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.recipe_list_views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here!', body.text)

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    @patch('recipes.views.recipe_list_views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        needed_title = 'This is what I need'
        recipes[0].title = needed_title
        recipes[0].save()
        self.browser.get(self.live_server_url)
        search_translation = 'Search for a recipe'
        search_input = self.browser.find_element(
            By.XPATH,
            f"//input[@placeholder='{search_translation}']"
        )
        search_input.send_keys(needed_title)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(
            needed_title,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.recipe_list_views.PER_PAGE', new=2)
    def test_recipe_home_pagination(self):
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()
        x = self.browser.find_elements(By.CLASS_NAME, 'recipe')
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2
        )
