from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Order, OrderItem, Card, CardItem

@login_required(login_url='login')
def add_card(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)
        card, created = Card.objects.get_or_create(user=request.user)
        card_item = CardItem.objects.filter(card=card, product=product).first()

        if card_item is None:
            CardItem.objects.create(
            card=card,
            product=product,
            quantity=quantity)
            return JsonResponse({'status': 'success', 'message': 'Added successfully'})

        if card_item:
            card_item.quantity += quantity
            card_item.save()
            return JsonResponse({'status': 'success', 'message': f'Quantity: {quantity}-ga oshdi'})


    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='login')
def decrease_cart_item(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    card = Card.objects.filter(user=request.user)
    product = get_object_or_404(Product, id=item_id)
    card_item = CardItem.objects.filter(card=card,product=product).first()
    card_item.quantity -= quantity
    card_item.save()
    return JsonResponse({"status": "success",'message': f"item decreased to -{quantity}"})

@login_required(login_url="login")
def my_cart(request):
    if request.method == "GET":
        card, created = Card.objects.get_or_create(user=request.user)

        cart_items = card.items.all().select_related('product')

        data = []
        for item in cart_items:
            data.append({
                "id": item.id,
                "title": item.product.title if item.product else "Deleted product",
                "price": float(item.total_price),
                "quantity": item.quantity,
                "image": item.product.images.first().photo.url if item.product and item.product.images.exists() else "",
            })

        return JsonResponse({
            'status': 'success',
            'cart_items': data,
            'total_count': sum(i.quantity for i in cart_items)
        })


@login_required(login_url="login")
def remove_cart_item(request, item_id):
    if request.method != "POST":
        return JsonResponse({'status': 'error'}, status=400)

    card = Card.objects.filter(user=request.user).first()
    if card is None:
        return JsonResponse({'status': 'error'}, status=404)

    item = card.items.filter(id=item_id).first()
    if item is None:
        return JsonResponse({'status': 'error'}, status=404)

    item.delete()
    return JsonResponse({'status': 'success'})


@login_required(login_url='login')
def clear_cart(request, card_id):
    card = Card.objects.get(user=request.user)
    card_items = CardItem.objects.filter(card=card)
    for item in card_items:
        item.delete()

    return JsonResponse({"status": 'success','message': 'Card items cleared'})

@login_required(login_url="login")
def my_orders(request):
    done_orders = request.user.orders.filter(status='done').prefetch_related('items','products')
    cancelled = request.GET.get("cancelled","")
    if cancelled:
        cancelled_orders = request.user.orders.filter(status='cancelled').prefetch_related('items','products')

    new = request.GET.get("new","")
    if new:
        new_orders = request.user.orders.filter(status='paid').prefetch_related('items','products')

    return render(request,"my_orders.html",context={"done_orders": done_orders,'new_orders': new_orders,'cancelled_orders': cancelled_orders})