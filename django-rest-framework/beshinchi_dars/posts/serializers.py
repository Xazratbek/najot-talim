from rest_framework import serializers
from .models import Post
from rest_framework.exceptions import ValidationError
from django.utils.html import escape
from rest_framework import status

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self,value):
        if value:
            if value.startswith('a'):
                raise ValidationError('Sarlavha a bilan boshlanmasin')
        return escape(value.strip())

    def validate_desc(self, value):
        if not value:
            raise ValidationError('Content bosh bo\'lishi mumkin emas')
        if '4' in value:
            raise ValidationError('Content ichida raqamlar bo\'lmasin')

        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({
            "message": "Kitoblar ro'yxati",
            'status': status.HTTP_200_OK
        })
        return data

    def create(self, validated_data):
        validated_data['title'] = validated_data.get('title').strip()
        validated_data['author'] = validated_data.get('author').lower()
        return validated_data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.author = validated_data.get('author')
        instance.save()
        return instance