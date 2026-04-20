from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response

class BookListCreateApiView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                'message': 'Kitoblar ro\'yxati',
                'books_count': books.count(),
                'data': serializer.data
            }
        )

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    'message': "Yangi kitob qo'shildi",
                    'new_book': serializer.data
                }
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                'message': 'Notog\'ri ma\'lumot yuborildi',
                'errors': serializer.errors
            }
        )

class UpdateDestroyDetailView(APIView):
    def put(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        if book:
            serializer = BookSerializer(data=request.data,instance=book)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_202_ACCEPTED,
                        'message': "Kitob ma'lumotlari yangilandi",
                        'updated_data': serializer.data
                    }
                )
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    'message': "Notog'ri ma'lumot kiritildi",
                    "errors": serializer.errors
                }
            )

    def get(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        serializer = BookSerializer(book)
        if book:
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    'data': serializer.data
                }
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                'message': f"{pk}-id lik kitob mavjud emas",
                'errors': serializer.errors
            }
        )

    def patch(self,request,pk):
        book = Book.objects.filter(pk=pk).first()
        if book:
            serializer = BookSerializer(data=request.data,instance=book,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_206_PARTIAL_CONTENT,
                        'message': "Ma'lumotlar yangilandi",
                        'updated_data': serializer.data
                    }
                )
        return Response(
            {
                "status":status.HTTP_400_BAD_REQUEST,
                'message': "Notog'ri ma'lumotlar",
                'errors': serializer.errors
            }
        )

    def delete(self, request, pk):
        book = Book.objects.filter().first()
        if book:
            book.delete()
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    'message': 'Muvaffaqiyatli o\'chirildi'
                }
            )