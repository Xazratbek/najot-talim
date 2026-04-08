from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ProductForm
from .models import Category, Product, ProductImage
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import UpdateView


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
        print(page_obj)
        return render(request, "home.html", context={"page_obj": page_obj})

class ProductCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = ProductForm()
        return render(request, "watch/create.html",context={"form": form})

    def post(self, request):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.sotuvchi = request.user
            product.save()
            files = request.FILES.getlist('images')
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            return redirect('home')
        return render(request,"watch/create.html",context={"form": form})

class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        return product.sotuvchi == self.request.user

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, "watch/update.html",context={"form": form,"product": product})

    def post(self, request, pk):
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(request.POST, request.FILES,instance=product)
            if form.is_valid():
                form.save()
            files = request.FILES.getlist('images')
            if files:
                ProductImage.objects.filter(product=product).delete()
                for f in files:
                    ProductImage.objects.create(product=product, image=f)

            return redirect("product-detail",pk=product.pk)

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).prefetch_related("images")
        return render(request, "watch/detail.html",context={"product": product})

class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin, View):
    def test_func(self):
        product = get_object_or_404(Product,pk=self.kwargs.get("pk"))
        return product.sotuvchi == self.request.user

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect("product-list")

class MyProducts(LoginRequiredMixin,View):
    def get(self, request):
        products = Product.objects.filter(sotuvchi=request.user).prefetch_related("images")
        return render(request, "watch/myproducts.html",context={"products": products})
