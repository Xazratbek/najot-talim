from django.shortcuts import render
from django.http import HttpResponse

def get_users(request):
    return HttpResponse("<h1 style='color: red'>Userlar chiqadi bu yerda</p>")

def get_user_by_id(request, id):
    return HttpResponse(f"hey user: {id}")