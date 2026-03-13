from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def product_list(request):
    return HttpResponse("Product list")

def product_detail(request, **kwargs):
    return HttpResponse(f"{kwargs["id"]}")