from django.urls import path
from .views import *

urlpatterns = [
    path("",get_groups_list,name="groups"),
    path("<int:id>/",get_group_by_id,name="group_by_id"),
]
