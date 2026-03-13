from django.shortcuts import render
from django.http import HttpResponse

def get_videos(request):
    return HttpResponse("<h1 style='color: red'>Videolar chiqadi bu yerda</p>")

def get_video_by_id(request, id):
    return HttpResponse(f"Your video: {id}")