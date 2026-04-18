from django.urls import path
from .views import product_view, product_update_destroy_view

urlpatterns = [
    path('',product_view,name='product_view'),
    path('<int:pk>/',product_update_destroy_view,name='product_update_destroy_view'),
]
