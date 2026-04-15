from django.shortcuts import render, get_object_or_404, redirect
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

        if request.user.is_authenticated:
            RecentlyProduct.objects.get_or_create(
                user=request.user,
                product=product
            )

        ProductView.objects.create(
            product = product
        )

        user_comment = None
        if request.user.is_authenticated:
            user_comment = product.comments.filter(user=request.user).first()

        context = {
            'product': product,
            'categories': parent_categories(),
            'comments': product_comments(id),
            'product_view_count': product.view_product.count(),
            'user_comment': user_comment,

        }
        return render(request, "product.html", context=context)


@login_required()
def comment_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    if request.method != "POST":
        return redirect('product_detail', id=product.id)

    text = request.POST.get('text', '').strip()

    try:
        rate = int(request.POST.get('rate', 1))
    except (TypeError, ValueError):
        rate = 1

    if not (1 <= rate <= 5):
        messages.warning(request, 'Siz rate ni 1-5 oraligida berishingiz kerak')
        return redirect('product_detail', id=product.id)

    if Comment.objects.filter(product=product, user=user).exists():
        messages.warning(request, 'Siz bu mahsulot uchun avval izoh qoldirgansiz')
        return redirect('product_detail', id=product.id)

    Comment.objects.create(
        product=product,
        user=user,
        text=text,
        rate=rate
    )

    messages.success(request, 'Izohingiz qoldirildi')
    return redirect('product_detail', id=product.id)


@login_required()
def update_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()
    if comment is None:
        messages.warning(request, 'Comment topilmadi')
        return redirect('index')

    if request.method != "POST":
        return redirect('product_detail', id=comment.product.id)

    if comment.user == request.user:
        text = request.POST.get('text', '').strip()
        try:
            rate = int(request.POST.get('rate', 1))
        except (TypeError, ValueError):
            rate = 1

        if not (1 <= rate <= 5):
            messages.warning(request, 'Siz rate ni 1-5 oraligida berishingiz kerak')
            return redirect('product_detail', id=comment.product.id)

        comment.text = text
        comment.rate = rate
        comment.save()

        messages.success(request, 'Comment ozgartirildi')
    else:
        messages.warning(request, 'Bu commentni ozgartirolmaysiz')
    return redirect('product_detail', id=comment.product.id)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()
    if comment is None:
        messages.warning(request, 'Comment topilmadi')
        return redirect('index')

    product_id = comment.product.id
    if request.method != "POST":
        return redirect('product_detail', id=product_id)

    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment ochirildi')
    else:
        messages.warning(request, 'Bu commentni ochirolmaysiz')
    return redirect('product_detail', id=product_id)

@login_required()
def my_comments(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'recently.html', {'recently_products': [], 'comments': comments})


def product_comments(product_id):
    comments = Comment.objects.filter(product=product_id)
    return comments


@login_required(login_url='login')
def saved(request, id):
    product = Product.objects.get(id=id)
    saved, created = Saved.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, 'maxsulot qoshildi')
        return HttpResponse('Maxsulot qo\'shildi')

    if not created:
        saved.delete()
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
