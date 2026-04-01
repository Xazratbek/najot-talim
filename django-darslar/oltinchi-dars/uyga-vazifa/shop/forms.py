from django.forms import ModelForm
from .models import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class CarsForm(ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"