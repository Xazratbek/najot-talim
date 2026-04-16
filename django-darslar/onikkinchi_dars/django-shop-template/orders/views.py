from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from .models import Order, Card, CardItem, OrderItem


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
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=400)

    quantity = int(request.POST.get('quantity', 1))
    card = Card.objects.filter(user=request.user).first()
    card_item = get_object_or_404(CardItem, id=item_id, card=card)
    card_item.quantity -= quantity
    if card_item.quantity <= 0:
        card_item.delete()
        return JsonResponse({"status": "success",'message': "item removed"})

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
                "product_id": item.product.id if item.product else None,
                "card_id": str(card.id),
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
    item = card.items.filter(id=item_id).first()
    item.delete()
    return JsonResponse({'status': 'success'})


@login_required(login_url='login')
def clear_cart(request, card_id):
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=400)

    card = Card.objects.get(user=request.user)
    card_items = CardItem.objects.filter(card=card)
    for item in card_items:
        item.delete()

    return JsonResponse({"status": 'success','message': 'Card items cleared'})


@login_required(login_url="login")
def create_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        
        order = Order.objects.create(user=request.user, address=address)
                
        card = Card.objects.filter(user=request.user).first()
        
        for i in card.items.all():
            OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity, total_price=i.total_price)
            
        data = []
        for item in order.items:
            data.append({
                "id": item.id,
                "product_id": item.product.id if item.product else None,
                "order_id": str(order.id),
                "title": item.product.title if item.product else "Deleted product",
                "price": float(item.total_price),
                "quantity": item.quantity,
                "image": item.product.images.first().photo.url if item.product and item.product.images.exists() else "",
            })
        
        return JsonResponse({'status': 201, 'message': 'zakaz yaratildi', 'finish_price': order.finished_price, 'items':data})
        
        



@login_required(login_url="login")
def my_orders(request):
    done_orders = request.user.orders.filter(status='done').prefetch_related('items__product')
    new_orders = Order.objects.none()
    cancelled_orders = Order.objects.none()

    cancelled = request.GET.get("cancelled","")
    if cancelled:
        cancelled_orders = request.user.orders.filter(status='cancelled').prefetch_related('items__product')

    new = request.GET.get("new","")
    if new:
        new_orders = request.user.orders.filter(status='paid').prefetch_related('items__product')

    return render(request,"my_orders.html",context={"done_orders": done_orders,'new_orders': new_orders,'cancelled_orders': cancelled_orders})
