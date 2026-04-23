from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated

class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        return Response({
            "service_count": len(data),
            "data": data
        })

class ServiceCreateView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)

        return Response(
            {
                "status": status.HTTP_200_OK,
                "data": data,
                "messsage":"Service haqida batafsil ma'lumot"
            }
            )

class ServiceDeleteView(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ServiceUpdateView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        try:
            if self.request.user.is_authenticated:
                serializer.save(updated_by=self.request.user)

        except NotAuthenticated:
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    'message': 'Authentikatsiyadan o\'ting iltimos',
                }
            )