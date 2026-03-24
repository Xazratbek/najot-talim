from django.urls import path
from .views import *

urlpatterns = [
    path("",flowers,name="flowers_list"),
    path("add/",add_flower,name="add_flower"),
    path("detail/<int:id>/",flower_detail,name="flower-detail"),
    path("update/<int:id>/",update_flower,name="update_flower"),
    path("delete/<int:id>/",delete_flower,name="delete_flower")
]
