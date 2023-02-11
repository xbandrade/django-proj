import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def fill_username_and_password(self, form, username, password):
        username_field = self.get_by_placeholder(form, 'Enter your username')
        password_field = self.get_by_placeholder(form, 'Enter your password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        form.submit()

    def test_user_valid_data_can_login_successfully(self):
        str_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=str_password
        )
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.fill_username_and_password(form, user.username, str_password)
        self.assertIn(
            f'You are logged in as {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_username_or_password_are_incorrect(self):
        str_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=str_password
        )
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.fill_username_and_password(
            form, user.username + 'a', str_password + 'a'
        )
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_username_and_password_form_is_invalid(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.fill_username_and_password(form, ' ', ' ')
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
