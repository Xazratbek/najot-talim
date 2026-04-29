from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .models import Book
from django.shortcuts import get_object_or_404

# class BookModelViewSet(ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class BookGenericAPIView(GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     lookup_field = 'pk'

#     def get_object(self,pk):
#         return get_object_or_404(Book,pk=pk)

#     def get(self, request,pk=None):
#         if pk is not None:
#             return Response(
#                 {
#                     "status": status.HTTP_200_OK,
#                     'data': self.get_serializer(self.get_object(pk)).data
#                 }
#             )

#         return Response(
#             {
#                 "status": status.HTTP_200_OK,
#                 'data': self.get_serializer(self.get_queryset(),many=True).data
#             }
#         )

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "status": status.HTTP_201_CREATED,
#                     'message': "Kitob qo'shildi",
#                     'new_book': serializer.data
#                 }
#             )
#         return Response(
#             {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 'message': "Xato ma'lumot kiritildi",
#                 'errors': serializer.errors
#             }
#         )

#     def put(self, request, pk):
#         serializer = self.get_serializer(data=request.data,instance=self.get_object(pk=pk))
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "status": status.HTTP_200_OK,
#                     'message': 'Kitob yangilandi'
#                 }
#             )
#         return Response(
#             {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 'message': "Xato ma'lumot kiritildi",
#                 'errors': serializer.errors
#             }
#         )

#     def patch(self, request,pk):
#         serializer = self.get_serializer(data=request.data,instance=self.get_object(pk=pk))
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "status": status.HTTP_202_ACCEPTED,
#                     'message': "Kitob qisman yangilandi"
#                 }
#             )

#         return Response(
#         {
#             "status": status.HTTP_400_BAD_REQUEST,
#             'message': "Xato ma'lumot kiritildi",
#             'errors': serializer.errors
#         }
#     )

#     def delete(self,request, pk):
#         self.get_object(pk=pk).delete()
#         return Response(
#             {
#                 "status": status.HTTP_204_NO_CONTENT,
#                 'message': "Kitob o'chirildi"
#             }
#         )


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'Barcha kitoblar',
            'count': len(response.data),
            'data': response.data
        }
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'Kitob topildi',
            'data': response.data
        }
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'status': status.HTTP_201_CREATED,
            'message': 'Kitob muvaffaqiyatli qo\'shildi',
            'data': response.data
        }
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'Kitob muvaffaqiyatli yangilandi',
            'data': response.data
        }
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'Kitob qisman muvaffaqiyatli yangilandi',
            'data': response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Kitob muvaffaqiyatli o\'chirildi'
            },
            status=status.HTTP_204_NO_CONTENT
        )