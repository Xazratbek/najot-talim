from rest_framework.serializers import ModelSerializer
from .models import Product
from django.forms import ModelForm

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'