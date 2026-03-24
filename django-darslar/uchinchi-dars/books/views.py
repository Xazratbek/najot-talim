from django.shortcuts import render
from .models import Book
from django.shortcuts import redirect


def book_list(request):
    books = Book.objects.all()
    return render(request, '/book_list.html', {'books': books})

def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')

        book = Book(title = title, desc = desc, author = author, isbn = isbn)
        book.save()

        return redirect('list')


    return render(request, 'books/add_book.html')