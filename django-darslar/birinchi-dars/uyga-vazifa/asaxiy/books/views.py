from django.shortcuts import render
from django.http import *

def books(request):
    return HttpResponse("Kitoblar chiqadi")

def book_category(request):
    return HttpResponse("Kitoblar kategoriyalar")