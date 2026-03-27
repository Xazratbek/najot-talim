from django.forms import ModelForm

from .models import Category, Order, OrderItem, Telefon


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
