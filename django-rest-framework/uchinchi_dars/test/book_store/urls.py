from .views import *
from django.urls import path

urlpatterns = [
    path('',book_list),
    path('nimadur/<int:pk>/',update_destroy_api_view),
]
