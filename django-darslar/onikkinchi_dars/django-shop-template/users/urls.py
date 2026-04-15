from django.urls import path
from .views import SignUpView, LoginView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/<uuid:id>/",ProfileView.as_view(),name="profile"),
    path("profile/<uuid:id>/update/", ProfileUpdateView.as_view(), name="profile-update"),
]
