from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from .models import Order, Card, CardItem, OrderItem
from decimal import Decimal
from products.models import PromoCode, PromoCodeUsage
from django.utils import timezone
from django.db import transaction


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
                "price": Decimal(item.total_price),
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
        promo_code_str = request.POST.get('promo_code', '').strip()

        card = Card.objects.filter(user=request.user).first()

        chegirma_miqdori = Decimal(0)

        with transaction.atomic():
            order = Order.objects.create(user=request.user, address=address)
            for i in card.items.all():
                OrderItem.objects.create(order=order,product=i.product,quantity=i.quantity,total_price=i.total_price)

            umumiy_summa = Decimal(sum(i.total_price for i in order.items.all()))

            if promo_code_str:
                promo = PromoCode.objects.filter(code=promo_code_str, is_active=True).first()

                if not promo:
                    return JsonResponse({"status": 400, 'message': "Promokod topilmadi yoki faol emas"})

                if promo.expire_at and promo.expire_at < timezone.now():
                    return JsonResponse({"status": 400, 'message': "Promokod muddati tugagan"})

                if umumiy_summa < promo.min_order_amount:
                    return JsonResponse({"status": 400, 'message': f"Minimal buyurtma summasi {promo.min_order_amount} bo'lishi kerak"})

                if promo.promo_type == 'welcome':
                    if request.user.orders.filter(status='paid').count() >= 3:
                        return JsonResponse({"status": 400, "message": "Bu kod faqat dastlabki 3 ta buyurtma uchun"})

                elif promo.promo_type == 'personal':
                    usage = PromoCodeUsage.objects.filter(user=request.user, promocode=promo).first()
                    if usage and usage.usage_count >= 1:
                        return JsonResponse({"status": 400, "message": "Siz bu promokoddan foydalanib bo'lgansiz"})

                yangi_summa = PromoCode.apply_discount(promo.discount_type, promo.discount_value, umumiy_summa)
                chegirma_miqdori = umumiy_summa - yangi_summa
                umumiy_summa = yangi_summa
                order.finished_price = umumiy_summa
                order.save()

                usage, created = PromoCodeUsage.objects.get_or_create(user=request.user, promocode=promo)
                usage.usage_count += 1
                usage.save()

            cash = request.user.balance
            if umumiy_summa > cash.amount:
                return JsonResponse({'status': 400, 'message': 'Pulingiz yetmaydi'})

            cash.amount -= umumiy_summa
            cash.save()

            order.status = 'paid'
            order.save()
            card.items.all().delete()

        data = [{
            "id": item.id,
            "product_id": item.product.id if item.product else None,
            "order_id": str(order.id),
            "title": item.product.title if item.product else "O'chirilgan mahsulot",
            "price": float(item.total_price),
            "quantity": item.quantity,
            "image": item.product.images.first().photo.url if item.product and item.product.images.exists() else ""
        } for item in order.items.all()]

        return JsonResponse({
            'status': 201,
            'message': 'Buyurtma yaratildi',
            'finished_price': float(umumiy_summa),
            'discount': float(chegirma_miqdori),
            'items': data
        })

@login_required(login_url="login")
def cancelled_order(request, order_id):
    status = request.POST.get('status', 'cancelled')
    order = Order.objects.filter(user=request.user, id=order_id).first()
    order.status = status
    order.save()

    return JsonResponse({'status': 200, 'message': f'{order.id} orderi bekor qilindi'})


@login_required(login_url="login")
def my_orders(request):
    done_orders = request.user.orders.filter(status='done').prefetch_related('items__product')
    new_orders = Order.objects.none()
    cancelled_orders = Order.objects.none()

    cancelled = request.GET.get("cancelled","")
    if cancelled:
        cancelled_orders = request.user.orders.filter(status='cancelled').prefetch_related('items__product').order_by('-updated_at')

    new = request.GET.get("new","")
    if new:
        new_orders = request.user.orders.filter(status='paid').prefetch_related('items__product').order_by('-created_at')


    return render(request,"my_orders.html",context={"done_orders": done_orders,'new_orders': new_orders,'cancelled_orders': cancelled_orders})

def check_promo(request,promo_code):
    try:
        promo = PromoCode.objects.filter(code=promo_code,is_active=True).first()
        if promo is not None:
            usage = PromoCodeUsage.objects.filter(user=request.user,promocode=promo).first()
            if promo.expire_at < timezone.now():
                return JsonResponse({"status": 400, 'message': "Promo code amal qilish muddati tugagan"})

            if promo.promo_type == 'welcome' and request.user.orders.count() > 3:
                return JsonResponse({"status": 400, 'message': "Bu promo code faqat birinchi 3-ta buyurtma uchun ishlaydi"})

            if promo.promo_type == 'personal' and usage.usage_count > 1:
                return JsonResponse({'status': 400, 'message': "Siz bu promo codeni oldin ishlatgansiz"})

            if PromoCode.objects.filter(code=promo_code,is_active=True).exists():
                return JsonResponse({"status": 200, 'message': 'Promo code mavjud'})

            else:
                return JsonResponse({"status": 400, 'message': 'Promo code mavjud emas'})
        else:
            return JsonResponse({"status": 404, 'message': 'Promo code topilmadi'})
    except PromoCode.DoesNotExist:
        return JsonResponse({"status": 400, 'message': "Promo code mavjud emas"})
