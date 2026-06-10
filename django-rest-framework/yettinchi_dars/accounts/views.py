from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404, redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request,user=user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = RefreshToken.for_user(user)
            return Response({
                "token": token.key,
                'user_id': user.pk,
                'email':user.email,
                'status': status.HTTP_200_OK
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)