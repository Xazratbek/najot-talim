from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response({
            "data": serializer.data
        })

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Mahsulot qo'shildi"
            })
        return Response({
            "errors": serializer.errors
        })

    def retrieve(self, request, pk):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product)
        return Response({
            "data":serializer.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)

    def update(self, request,pk):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data=request.data,instance=product)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Mahsulot yangilandi",
                "status":status.HTTP_200_OK,
                "data": serializer.data
            })
        return Response({
            "errors": serializer.errors
        })

    def partial_update(self, request,pk):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data=request.data,instance=product,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Mahsulot qisman yangilandi",
                "status":status.HTTP_200_OK,
                "data": serializer.data
            })
        return Response({
            "errors": serializer.errors
        })

    def destroy(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        print(product)
        if product is None:
            return Response({
                "message":f"{pk}-idlik mahsulot topilmadi"
            })
        product.delete()
        return Response({
            "message":"Product o'chirildi",
            "status": status.HTTP_204_NO_CONTENT,
        })