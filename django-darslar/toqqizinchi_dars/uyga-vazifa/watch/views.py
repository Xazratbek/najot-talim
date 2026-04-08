from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ProductForm
from .models import Category, Product, ProductImage
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin, PermissionRequiredMixin

class CategoryProducts(View):
    def get(self, request, pk):
        kategoriya = get_object_or_404(Category,pk=pk)
        mahsulotlar = kategoriya.products.all()
        return render(request, "watch/category-products.html",context={"kategoriya": kategoriya,"mahsulotlar": mahsulotlar})

class ProductsListView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-id')
        page_number = request.GET.get("page", 1)
        paginator = Paginator(products, 10)
        page_obj = paginator.get_page(page_number)

        return render(request, "home.html", context={"page_obj": page_obj})

class ProductCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = ProductForm()
        return render(request, "watch/create.html",context={"form": form})

    def post(self, request):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.instance.sotuvchi = request.user
            product.save()
            files = request.FILES.getlist('images')
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            return redirect('home')