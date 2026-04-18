from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarsSerializer
from .models import Cars

@api_view(['GET','POST'])
def cars_list_create_view(request):
    if request.method == 'GET':
        cars = Cars.objects.all()
        serializer = CarsSerializer(cars,many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Cars list',
            'data': serializer.data
        })

    elif request.method == 'POST':
        serializer = CarsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    'message': 'Yangi product qo\'shildi',
                    'car_id': serializer.instance.id,
                    'data': serializer.data
                }
            )

@api_view(['GET','PUT','PATCH','DELETE'])
def cars_update_destroy_view(request,pk):
    if request.method == 'GET':
        car = get_object_or_404(Cars,pk=pk)
        serializer = CarsSerializer(car)
        return Response({
            'status': status.HTTP_200_OK,
            'message': f'Car id: {car.id}',
            'data': serializer.data
        })

    elif request.method == 'PUT':
        car = get_object_or_404(Cars,pk=pk)
        serializer = CarsSerializer(data=request.data,instance=car)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_202_ACCEPTED,
                    'message': 'Updated',
                    'car_id': serializer.instance.id,
                    'data': serializer.data
                }
            )
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

    elif request.method == 'PATCH':
        car = get_object_or_404(Cars,pk=pk)
        serializer = CarsSerializer(data=request.data,instance=car,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_206_PARTIAL_CONTENT,
                    'message': 'Partial update boldi',
                    'product_id': serializer.instance.id,
                    'data': serializer.data
                }
            )

    elif request.method == 'DELETE':
        car = get_object_or_404(Cars,pk=pk)
        car.delete()
        return Response(
            {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'O\'chirildi car'
            }
        )