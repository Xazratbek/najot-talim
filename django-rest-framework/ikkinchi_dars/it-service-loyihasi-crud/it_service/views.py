from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer
from rest_framework.response import Response

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services,many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

class ServiceCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Yangi service qo\'shildi',
                    'new_service': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Notog'ri ma'lumot yuborildi",
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ServiceUpdateView(APIView):
    def put(self, request, pk):
        service = Service.objects.filter(pk=pk).first()
        if service:
            serializer = ServiceSerializer(data=request.data,instance=service)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': status.HTTP_202_ACCEPTED,
                        'message': f'Service: {serializer.instance.title} yangilandi',
                        'updated_data': serializer.data
                    }
                )
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Notog'ri ma'lumot yuborildi",
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': f"{pk}-id bilan service topilmadi",
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        service = Service.objects.filter(pk=pk).first()
        if service:
            serializer = ServiceSerializer(data=request.data,instance=service,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': status.HTTP_206_PARTIAL_CONTENT,
                        'message': f'Ma\'lumot yangilandi',
                        'updated_data': serializer.data
                    }
                )
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Notog'ri ma'lumot yuborildi",
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': f"{pk}-id bilan service topilmadi",
            },
            status=status.HTTP_400_BAD_REQUEST)

class ServiceDeleteView(APIView):
    def delete(self, request, pk):
        service = Service.objects.filter(pk=pk).first()
        if service:
            service.delete()
            return Response(
                {
                    'status': status.HTTP_204_NO_CONTENT,
                    'message': 'Service o\'chirildi'
                }
            )
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "service topilmadi",
            },
            status=status.HTTP_400_BAD_REQUEST)