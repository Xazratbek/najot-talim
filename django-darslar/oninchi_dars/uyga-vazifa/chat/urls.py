from django.urls import path
from .views import ChatPlaceholderView

urlpatterns = [
    path("", ChatPlaceholderView.as_view(), name="home"),
]
