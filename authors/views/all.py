from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import AuthorRecipeForm, LoginForm, RegisterForm
from recipes.models import Recipe


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
    ).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'authors/pages/dashboard.html', context=context)
