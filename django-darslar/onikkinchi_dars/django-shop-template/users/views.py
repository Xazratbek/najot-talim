from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cash
from django.http import JsonResponse

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            return redirect('index')
        return render(request, 'registration/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm(request=request)
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        return render(request,"registration/login.html",{"form": form}, )


class ProfileView(LoginRequiredMixin,View):
    def get(self, request,id):
        cash = Cash.objects.filter(user=request.user).first()
        context = {}
        context['card_number'] = cash.card_number
        context['card_date'] = cash.card_date
        context['cvv'] = cash.cvv
        context['amount'] = cash.amount
        return render(request, "profile.html",context=context)

class ProfileUpdateView(LoginRequiredMixin,View):
    def get(sel, request,id):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, "registration/profile_update.html",context={"form": form})

    def post(self, request, id):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get("new_password")
            if new_password:
                user.set_password(new_password)
            user.save()
            if new_password:
                update_session_auth_hash(request, user)
            return redirect('profile',id=id)

        return render(request, "registration/profile_update.html",context={"form": form})

@login_required(login_url="login")
def add_cash(request):
    if request.method == "POST":
        amount = request.POST.get('amount')

        cash = Cash.objects.filter(user=request.user).first()
        cash.ammount += amount
        cash.save()

    return JsonResponse({'status': 200, 'message':'Muvaffaqiyatli pul otkazildi', 'amount': cash.ammount})
