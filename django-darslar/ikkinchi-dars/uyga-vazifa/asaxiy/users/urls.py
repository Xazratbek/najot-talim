from django.urls import path
from .views import *


urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("edit/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
]
