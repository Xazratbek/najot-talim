from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from django.utils import timezone

class BookListCreateApiView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        return Response({
            "status": status.HTTP_200_OK,
            "book_count": len(data),
            "data": data
        })

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Avtorizatsiyadan o'ting",code=status.HTTP_401_UNAUTHORIZED)

        else:
            serializer.save(author=self.request.user)

class UpdateDestroyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Book.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        print("UPDATE bo'lyapti...")

        response = super().update(request, *args, **kwargs)

        return Response({
            "status": status.HTTP_202_ACCEPTED,
            "data": response.data
        })

    def perform_update(self, serializer):
        serializer.save(
            updated_at=timezone.now()
        )

    def destroy(self, request, *args, **kwargs):
        print("DELETE bo'lyapti...")

        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()