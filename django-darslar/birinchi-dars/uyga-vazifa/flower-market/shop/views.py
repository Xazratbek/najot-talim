from django.shortcuts import render
from django.http import HttpResponse

def flowers(request):
    return HttpResponse("Gullar 💐")

def buy_flower(request):
    return HttpResponse("Gul sotib olish")