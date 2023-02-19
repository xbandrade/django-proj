from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from authors.forms import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None
        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id=id,
            ).first()
            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, form, recipe_exists):
        context = {
            'form': form,
            'recipe_exists': recipe_exists,
        }
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context
        )

    def get(self, request, id=None):
        recipe_exists = id
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form, recipe_exists)

    def post(self, request, id=None):
        recipe_exists = id
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.prep_steps_is_html = False
            recipe.is_published = False
            recipe.save()
            messages.success(request, _('Recipe saved successfully'))
            return redirect(
                reverse(
                    'authors:dashboard',
                )
            )
        return self.render_recipe(form, recipe_exists)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, _('Recipe successfully deleted'))
        return redirect(reverse('authors:dashboard'))
