from rest_framework import serializers
from .models import Product
from rest_framework.exceptions import ValidationError
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def validate_name(self, value):
    #     if "jonibek" in value:
    #         raise ValidationError({"name":"name ichida jonibek degan so'z bo'lmasin"})
    #     return value

    def validate(self, attrs):
        print(attrs)
        if Decimal('12') == attrs.get('price'):
            raise ValidationError({"price":"price ichida 12 degan so'z bo'lmasin"})
        return attrs
