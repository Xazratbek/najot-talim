from django.urls import path
from .views import (
    SignUpView,
    LoginView,
    LogOutView,
    HomePageView,
    EditProfileView,
    PasswordChange,
    ProfileView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("signup/",SignUpView.as_view(),name="signup"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",LogOutView.as_view(),name="logout"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("profile/<int:pk>/update/", EditProfileView.as_view(), name="profile-update"),
    path("profile/<int:pk>/password-change/", PasswordChange.as_view(), name="password-change"),
]
