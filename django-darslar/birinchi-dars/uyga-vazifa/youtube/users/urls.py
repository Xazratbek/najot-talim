from django.urls import path
from .views import *

urlpatterns = [
    path("",get_users,name="get_users"),
    path("<int:id>/",get_user_by_id,name="get_user_by_id")
]
