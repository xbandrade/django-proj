
import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Value
from django.db.models.aggregates import Count, Max, Min, Sum
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')')
        )
    ).order_by('-id')
    number_of_recipes = recipes.aggregate(Count('id'))
    print(recipes)
    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['id__count'],
    }
    return render(
        request,
        'recipes/pages/theory.html', context=context
    )
