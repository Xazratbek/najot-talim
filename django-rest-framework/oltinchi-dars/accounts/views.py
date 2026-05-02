from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import logout
from django.shortcuts import redirect

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "email": user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            logout(request)
            return Response({
                "status": status.HTTP_200_OK,
                'message': "Tizimdan muvaffaqiyatli chiqdingiz"
            })
        return Response(
            {
                "status":status.HTTP_400_BAD_REQUEST,
                'message': "Siz tizimga kirmagansiz yoki nimadur xato ketdi"
            }
        )