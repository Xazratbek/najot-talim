from django.shortcuts import render
from django.http import HttpResponse

def get_lessons(request):
    return HttpResponse("Darslar chiqadi shu yerda")

def get_lesson_by_id(request, id):
    return HttpResponse("Sizning darsingiz: {id}")