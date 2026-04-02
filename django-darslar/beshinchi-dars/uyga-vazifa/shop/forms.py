from django.forms import ModelForm
from django import forms
from .models import Category, Order, OrderItem, Telefon

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=150)
    recepient = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.widgets.Textarea)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class TelefonForm(ModelForm):
    class Meta:
        model = Telefon
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["user", "status"]


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "telefon", "quantity"]
