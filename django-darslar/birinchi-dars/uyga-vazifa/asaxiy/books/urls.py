from django.urls import path
from .views import *

urlpatterns = [
    path("",books,name="get_users"),
    path("category/",book_category,name="get_user_by_id")
]
