from django.shortcuts import render
# from django.contrib.auth.views import
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreateForm, CustomUserEditForm
from .models import CustomUser
from django.urls import reverse_lazy
from django.views import View

# class SignUpView(CreateView):
#     form_class = CustomUserCreateForm
#     template_name = "registration/signup.html"
#     success_url = reverse_lazy("home")

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreateForm()
        return render(request, "registration/signup.html",context={"form": form})

    def post(self, request):
        form = CustomUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request,"registration/signup.html",context={"form": form})

class AccountUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = "registration/edit.html"
    success_url = reverse_lazy("home")

class HomePageView(View):
    def get(self, request):
        return render(request,"home.html")