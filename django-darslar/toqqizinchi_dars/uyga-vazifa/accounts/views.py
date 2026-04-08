from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views import View
from watch.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash

class ProfileView(View):
    def get(self, request, pk):
        profile = get_object_or_404(CustomUser, pk=pk)
        return render(request, "registration/profile.html",context={"profile": profile})

class HomePageView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "home.html",context={"kategoriyalar": categories})

class SignUpView(View):
    def get(self,request):
        form = CustomUserCreationForm()
        return render(request,"registration/signup.html",context={"form":form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        u_name = request.POST.get("username")
        u_pass = request.POST.get("password")

        user = authenticate(request, username=u_name, password=u_pass)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {
                "error": "Login yoki parol xato",
                "form": form
            })

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")

class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user_p = get_object_or_404(CustomUser, pk=self.kwargs.get("pk"))
        return user_p == self.request.user

    def get(self, request, pk):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, "registration/update_profile.html", {"form": form})

    def post(self, request, pk):
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile-update", pk=request.user.pk)
        return render(request, "registration/update_profile.html", {"form": form})

class PasswordChange(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user_data = get_object_or_404(CustomUser, pk=self.kwargs.get("pk"))
        return user_data == self.request.user

    def get(self, request, pk):
        form = PasswordChangeForm(user=request.user)
        return render(request, "registration/password_change.html", {"form": form})

    def post(self, request, pk):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile-update", pk=user.pk)

        return render(request, "registration/password_change.html", {"form": form})
