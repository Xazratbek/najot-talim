from django.urls import path
from .views import *

urlpatterns = [
    path("",flowers,name="gullar"),
    path("buy-flower/",buy_flower,name="buy-flowers"),
]
