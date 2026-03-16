from django.shortcuts import render
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"

class BookEditView(UpdateView):
    model = Book
    template_name = "books/book_edit.html"
    context_object_name = "book_edit"
    fields = ['name', 'author', 'price', 'description']
    success_url = reverse_lazy('books_list')

class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"

class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book_delete.html"
    context_object_name = "book"
    success_url = reverse_lazy('books_list')
