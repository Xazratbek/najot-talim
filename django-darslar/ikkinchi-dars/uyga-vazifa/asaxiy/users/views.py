from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import User

class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

class UserUpdateView(UpdateView):
    model = User
    template_name = "users/update.html"
    fields = ['name', 'email', 'age', 'bio']
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy('user_list')

class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"