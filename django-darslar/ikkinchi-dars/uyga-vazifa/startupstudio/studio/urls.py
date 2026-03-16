from django.urls import path
from .views import *

urlpatterns = [
    path("",startups,name="startups")
]
