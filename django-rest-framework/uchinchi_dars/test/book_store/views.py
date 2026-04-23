from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Book
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        lst_data = []

        for book in books:
            book_dict = {
                'title': book.title,
                'summary': book.summary,
                'isbn': book.isbn,
                'published_date': str(book.published_date),
                'pages': book.pages
            }
            lst_data.append(book_dict)

        return Response(
            {
                'data': lst_data
            }
        )

    elif request.method == 'POST':
        title =  request.data.get('title')
        author =  request.data.get('author')
        summary =  request.data.get('summary')
        isbn =  request.data.get('isbn')
        published_date =  request.data.get('published_date')
        pages =  request.data.get('pages')
        book = Book.objects.create(title=title,author_id=int(author),summary=summary,isbn=isbn,published_date=published_date,pages=pages)

        return Response(
            {
                "message": "Kitob qoshildi"
            }
        )

@api_view(['PUT','PATCH','DELETE',"GET"])
def update_destroy_api_view(request,pk):
    book = get_object_or_404(Book,pk=pk)
    if request.method == 'GET':
        if book:
            serialized_data = {}
            serialized_data['title'] = book.title
            serialized_data['summary'] = book.summary
            serialized_data['isbn'] = book.isbn
            serialized_data['published_date'] = book.published_date
            serialized_data['pages'] = book.pages

            return Response(
                {
                    "data": serialized_data
                }
            )
    elif request.method == 'PUT':
        title =  request.data.get('title','')
        author =  request.data.get('author','')
        summary =  request.data.get('summary','')
        isbn =  request.data.get('isbn','')
        published_date =  request.data.get('published_date','')
        pages =  request.data.get('pages','')

        book.update(title=title,author_id=author,summary=summary,isbn=isbn,published_date=published_date,pages=pages)

        return Response(
            {
                "status": status.HTTP_202_ACCEPTED,
                'message': 'Yangilandi'
            }
        )

    elif request.method == 'PATCH':
        data = request.data
        new_data = book.update(**data)
        return Response(
            {
                "message": 'Yangilandi'
            }
        )

    elif request.method == 'DELETE':
        book.delete()
        return Response(
            {
                "message": "O'chirildi"
            }
        )