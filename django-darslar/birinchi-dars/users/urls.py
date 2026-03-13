from django.urls import path
from .views import *

urlpatterns = [
    path("user-list/",user_list)
]
