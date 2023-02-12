from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from recipes.models import Recipe

from .forms import AuthorRecipeForm, LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    context = {
        'form': form,
        'form_action': reverse('authors:register_create'),
    }
    return render(request, 'authors/pages/register_view.html', context=context)


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User has been created, please log in')
        del request.session['register_form_data']
        return redirect(reverse('authors:login'))
    context = {
        'form': form,
    }
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    context = {
        'form': form,
        'form_action': reverse('authors:login_create'),
    }
    return render(request, 'authors/pages/login.html', context=context)


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
    else:
        logout(request)
        messages.success(request, 'Logged out successfully')
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    )
    context = {
        'recipes': recipes,
    }
    return render(request, 'authors/pages/dashboard.html', context=context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        id=id,
    ).first()
    if not recipe:
        raise Http404()
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
        messages.success(request, 'Recipe saved successfully')
        return redirect(
            reverse('authors:dashboard_recipe_edit', kwargs={'id': id})
        )
    context = {
        'recipe': recipe,
        'form': form,
    }
    return render(request, 'authors/pages/dashboard_recipe.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    recipe = None
    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.prep_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Recipe created successfully')
        return redirect(
            reverse('authors:dashboard_recipe_create')
        )
    context = {
        'form': form,
    }
    return render(request, 'authors/pages/dashboard_recipe_create.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    id = POST.get('id')
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        id=id,
    ).first()
    if not recipe:
        raise Http404()
    recipe.delete()
    messages.success(request, 'Recipe successfully deleted')
    return redirect(reverse('authors:dashboard'))
