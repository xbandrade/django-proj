from django.http import HttpResponse
from django.shortcuts import render


recipe_list = [
    'Ukrainian Pierogi',
    'Single-Serving Chocolate Chip Cookie', 
    'Lemon Pepper Chicken Wings', 
    'Golden Chicken Vegetable Soup With Chickpeas', 
    'Chocolate Bundt Cake', 
    'Crispy Spiced Roasted Chickpeas', 
    'Cincinnati Chili', 
    'Spicy Sesame Chile Oil Noodles', 
    'Spaghetti Carbonara', 
    'Mango Dessert Cup',
    ]

names = [
    'Lamar Ortega',
    'Arthur Odonnell',
    'Abram Moon',
    'Jalen Decker',
    'Emmalee Salinas',
    'Trey Ramos',
    'Jadyn Andrews',
    'Clara Cross',
    'Johnny Newton',
    'London Merritt',
    ]


def home(request):
    context = {
        'names': names,
        'n': range(10),
        'recipe_list': recipe_list,
        'info': zip(names, recipe_list),
    }
    return render(request, 'recipes/pages/home.html', context=context)
