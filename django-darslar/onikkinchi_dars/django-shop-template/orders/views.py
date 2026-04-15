from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Order, OrderItem, Card, CardItem


def add_card(request, pruduct_id, quantity=1):
    product = get_object_or_404(Product, pk=pruduct_id)
    card, created = Card.objects.get_or_create(user=request.user)

    product = CardItem.objects.filter(card=card, product=product).first()

    if not product:
        CardItem.objects.create(
        card=card,
        product=product,
        quantity=quantity)

    if product:
        product.quantity += quantity
        product.save()
