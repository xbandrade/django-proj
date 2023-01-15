from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('Home')


def about(request):
    return HttpResponse('About')


def contact(request):
    return HttpResponse('Contact')
