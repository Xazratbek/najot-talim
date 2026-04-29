from rest_framework.serializers import ModelSerializer
from .models import Book, Meva

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['title','description','published_year','isbn','price','author']

class MevaSerializer(ModelSerializer):
    class Meta:
        model = Meva
        fields = '__all__'