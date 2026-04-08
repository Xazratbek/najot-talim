from django import forms
from .models import Product, ProductImage

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            cleaned = []
            for uploaded_file in data:
                cleaned.append(single_file_clean(uploaded_file, initial))
            return cleaned
        return single_file_clean(data, initial)

class ProductForm(forms.ModelForm):
    images = MultipleFileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name','description',"brand","category","price","stock","color","warranty_months"]