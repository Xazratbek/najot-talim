from django.urls import path
from .views import *

urlpatterns = [
    path("",laptop_list,name="laptop-list"),
    path("add-laptop/",add_laptop,name="add-laptop"),
    path("laptop/<int:id>/",laptop_detail,name="laptop-detail"),
    path("laptop/update/<int:id>/",update_laptop,name="laptop-update"),
]
