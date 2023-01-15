from django.http import HttpResponse
from django.urls import path
from recipes.views import home, about, contact


urlpatterns = [
    path('', home),
    path('about/', about),
    path('contact/', contact),
]
