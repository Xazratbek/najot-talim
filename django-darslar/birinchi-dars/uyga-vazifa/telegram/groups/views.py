from django.shortcuts import render
from django.http import HttpResponse

def get_groups_list(request):
    return HttpResponse('Bu yerda guruhlar bo\'ladi')

def get_group_by_id(request):
    return HttpResponse("Bu yerda guruh haqida batafsil ma'lumot bo'ladi")