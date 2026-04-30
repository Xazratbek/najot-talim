from django.shortcuts import render, get_object_or_404
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status

@api_view(['GET','POST'])
def product_view(request):
    print(request.GET.get('q'))
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    'message': 'Yangi product qo\'shildi',
                    'product_id': serializer.instance.id,
                }
            )


@api_view(['GET','PUT','PATCH','DELETE'])
def product_update_destroy_view(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data=request.data,instance=product)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_202_ACCEPTED,
                    'message': "Muvaffaqiyatli yangilandi",
                    'data': serializer.data,
                }
            )

    elif request.method == 'PATCH':
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data=request.data,instance=product,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_206_PARTIAL_CONTENT,
                    'message': "Muvaffaqiyatli yangilandi",
                    'data': serializer.data,
                }
            )
        else:
            return Response(
                {
                "status": status.HTTP_304_NOT_MODIFIED
                }
            )

    elif request.method == 'DELETE':
        product = get_object_or_404(Product,pk=pk)
        product.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                'message': 'Muvaffaqiyatli o\'chirildi'
            }
        )
