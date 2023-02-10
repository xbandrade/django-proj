from unittest.mock import patch

from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination_range


class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_initial_ranges_are_correct(self):
        # Curr page = 1, Qt Page = 2, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Curr page = 2, Qt Page = 2, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Curr page = 10, Qt Page = 4, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Curr page = 14, Qt Page = 4, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_sure_final_ranges_are_correct(self):
        # Curr page = 19, Qt Page = 4, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Curr page = 20, Qt Page = 4, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Curr page = 21, Qt Page = 4, Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_invalid_page_query_redirects_to_page_1(self):
        for i in range(9):
            kwargs = {'author_data': {'username': f'user{i}'},
                      'slug': f'slug{i}'}
            self.make_recipe(**kwargs)
        with patch('recipes.views.PER_PAGE', new=3):
            page = {'page': 'not-int'}
            response = self.client.get(reverse('recipes:home'), page)
            self.assertEqual(response.context['recipes'].number, 1)
