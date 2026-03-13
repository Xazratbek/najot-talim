from django.shortcuts import render
from django.http import HttpResponse

def get_channels_list(request):
    return HttpResponse('Bu yerda kanallar ro\'yxati bo\'ladi')

def get_channel_by_id(request):
    return HttpResponse("Bu yerda kanal haqida batafsil ma'lumot bo'ladi")

def join_to_channel(request, channel_id):
    return HttpResponse(f"Siz {channel_id}-ga muvaffaqiyatli qo'shildingiz")
