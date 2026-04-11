from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreateForm, CustomUserEditForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "registration/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        listing_qs = user.user_listings.select_related("listing_category", "user").prefetch_related("images")
        context['favorite_listings'] = user.user_favorites.select_related(
            "favorite_listing__listing_category",
            "favorite_listing__user",
        ).prefetch_related("favorite_listing__images")
        context['active_listings'] = listing_qs.filter(status="active")
        context['sold_listings'] = listing_qs.filter(status="sold")
        context['archived_listings'] = listing_qs.filter(status="archived")
        context['deleted_listings'] = listing_qs.filter(status="deleted")
        context['current_tab'] = self.request.GET.get("tab", "active")

        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = "registration/update.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("accounts:profile")

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("listing:list")