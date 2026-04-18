from django.urls import path
from .views import cars_list_create_view, cars_update_destroy_view

urlpatterns = [
    path("",cars_list_create_view,name='cars_list_create'),
    path("<int:pk>/",cars_update_destroy_view,name='cars_update_destroy_view')
]
