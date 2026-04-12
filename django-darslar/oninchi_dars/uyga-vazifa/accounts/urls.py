from django.urls import path, reverse_lazy
from .views import RegisterView, ProfileUpdateView, ProfileView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = "accounts"

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/",RegisterView.as_view(),name="signup"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path('profile/update/',ProfileUpdateView.as_view(),name="update"),
    path(
        'password/change/',
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url=reverse_lazy('accounts:password_change_done')
        ),
        name='password_change'
    ),
    path(
        'password/change/done/',
        PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
