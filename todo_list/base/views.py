from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'base/home.html')

# Create your views here.
