from django.urls import path
from .views import ReviewsPlaceholderView

urlpatterns = [
    path("", ReviewsPlaceholderView.as_view(), name="home"),
]
