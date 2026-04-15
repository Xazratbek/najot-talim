from django.shortcuts import render, get_object_or_404
from django.views import View
from .service import parent_categories, discount_desc, category_unique_product,new_arrivals, featured_products
from home.service import get_sliders, get_banners, get_brands
from blog.service import get_latest_posts
from django.contrib import messages
from .models import Comment, Saved, RecentlyProduct, ProductView, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from orders.models import Order
from django.http import HttpResponse



class IndexView(View):
    def get(self, request):
        context = {
            'categories': parent_categories(),
            'discount_desc': discount_desc(),
            'category_unique_product': category_unique_product(),
            'new_arrivals': new_arrivals(),
            "featured_products":  featured_products(),
            'sliders': get_sliders(),
            'banners': get_banners(),
            'brands': get_brands(),
            'latest_posts': get_latest_posts(),
        }
        return render(request,"index.html",context=context)


class ProductDetailView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        # RecentlyProduct.objects.get_or_create(
        #     user=request.user,
        #     product = product
        # )

        ProductView.objects.create(
            product = product
        )

        context = {
            'product': product,
            'categories': parent_categories(),
            'comments': product_comments(id),
            'product_view_count': product.view_product.count()

        }
        return render(request, "product.html", context=context)


@login_required()
def comment_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    text = request.POST.get('text', None)
    rate = request.POST.get('rate', 1)

    # client = user.orders.filter(status='done').select_related('items', 'products')


    if not (rate >= 1 and rate <= 5):
        messages.warning(request, 'Siz rate ni 1-5 oraligida berishingiz kerak')

    Comment.objects.create(
        product=product,
        user=user,
        text=text,
        rate=rate
    )

    messages.warning(request, 'Izohingiz qoldirildi')


@login_required()
def update_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()
    if comment.user == request.user:
        text = request.POST.get('text', None)
        rate = request.POST.get('rate', 1)

        # comment.update(text=text, rate=rate)

        comment.text = text
        comment.rate = rate
        comment.save()

        messages.success(request, 'Comment ozgartirildi')
    else:
        messages.warning(request, 'Bu commentni ozgartirolmaysiz')

@login_required()
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment ochirildi')
    else:
        messages.warning(request, 'Bu commentni ochirolmaysiz')

@login_required()
def my_comments(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, '#', {'comments': comments})


def product_comments(product_id):
    comments = Comment.objects.filter(product=product_id)
    return comments


@login_required(login_url='login')
def saved(request, id):
    product = Product.objects.get(id=id)
    saved, created = Saved.objects.get_or_create(user=request.user, product=product)

    if created:
        print("Maxsulot qo'shildi: ")
        messages.success(request, 'maxsulot qoshildi')
        return HttpResponse('Maxsulot qo\'shildi')

    if not created:
        saved.delete()
        print("Maxsulot olib tashlandi")
        messages.success(request, 'Olib tashlandi')
        return HttpResponse('Maxsulot olib tashlandi')


@login_required()
def user_saveds(request):
    saved_products = request.user.saved_products.all().select_related('product')
    return render(request, 'wishlist.html', {'saved_products': saved_products})

@login_required()
def user_recently(request):
    recently_products = request.user.recently_products.all().select_related('product')
    return render(request, 'recently.html', {'recently_products': recently_products})
