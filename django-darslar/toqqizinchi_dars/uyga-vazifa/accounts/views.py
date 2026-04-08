from django.shortcuts import render, redirect
from .models import CustomUser
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from watch.models import Category

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