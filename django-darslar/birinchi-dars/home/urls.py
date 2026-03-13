from django.urls import path
from .views import *

urlpatterns = [
    path("home-page/",home_page)
]
