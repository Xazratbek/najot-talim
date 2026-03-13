from django.http import HttpResponse
from django.urls import path
from .views import *


urlpatterns = [
    path('list/',product_list),
    path('detail/<int:id>/',product_detail)
]
