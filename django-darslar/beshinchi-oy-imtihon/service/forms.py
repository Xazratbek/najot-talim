from django.forms import ModelForm
from .models import Category, Service


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"