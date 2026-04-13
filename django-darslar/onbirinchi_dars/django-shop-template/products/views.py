from django.shortcuts import render
from django.views import View
from .models import Product
from .service import parent_categories, discount_desc, category_unique_product,new_arrivals, featured_products
from home.service import get_sliders, get_banners, get_brands
from blog.service import get_latest_posts


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
        context = {
            'product': product,
            'categories': parent_categories()
        }
        return render(request, "product.html", context=context)
