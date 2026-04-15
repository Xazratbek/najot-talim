from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class BlogView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'single-blog.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'