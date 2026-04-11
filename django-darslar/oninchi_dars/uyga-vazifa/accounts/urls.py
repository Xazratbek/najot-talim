from django.urls import path
from .views import RegisterView, ProfileUpdateView, ProfileView, LogoutView

app_name = "accounts"

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/",RegisterView.as_view(),name="signup"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path('profile/update/',ProfileUpdateView.as_view(),name="update"),
]
