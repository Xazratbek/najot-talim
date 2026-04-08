from django.urls import path
from .views import SignUpView, LoginView, LogOutView,HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("signup/",SignUpView.as_view(),name="signup"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",LogOutView.as_view(),name="logout"),
]
