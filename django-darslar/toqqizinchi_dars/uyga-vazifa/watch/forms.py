from django import forms
from .models import Product, ProductImage

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name','description',"brand","category","price","stock","color","warranty_months"]