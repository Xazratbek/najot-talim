from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, login

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username','email','password','bio']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio','')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Login yoki parol xato.")
            if not user.is_active:
                raise serializers.ValidationError("Foydalanuvchi faol emas.")
        else:
            raise serializers.ValidationError("Username va password kiritilishi shart.")

        data['user'] = user
        return data
