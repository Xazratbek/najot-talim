from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CategoryForm, ServiceForm
from .models import Service, Category
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator


class CategoryCreateView(CreateView):
    model = Category
    template_name = "category/create.html"
    context_object_name = "form"
    fields = "__all__"

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        paginator = Paginator(categories, 5)
        page_number = request.GET.get("page")
        print(page_number)
        page_obj = paginator.get_page(page_number)

        return render(request,"category/list.html",context={"categories": categories,"page_obj":page_obj})

class CategoryListView(ListView):
    model = Category
    template_name = "category/list.html"
    context_object_name = "categories"

class CategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category,pk=pk)
        form = CategoryForm(request.POST, instance=category)

        return render(request,"category/update.html",context={"form": form, "category": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()

            return redirect("service-list")
        return render(request,"category/update.html",context={"form": form, "category": category})

class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category,pk=pk)
        return render(request,"category/detail.html",context={"category": category})

class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, "category/delete.html", context={"category": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect("category-list")


class ServiceListView(View):
    def get(self, request):
        services = Service.objects.all()
        return render(request, "service/list.html",context={"services": services})

class ServiceCreateView(View):
    def get(self, request):
        form = ServiceForm()
        return render(request, "service/create.html",context={"form": form})

    def post(self, request):
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service-list")

        return render(request, "service/create.html",context={"form": form})

class ServiceUpdateView(View):
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form =  ServiceForm(request.POST, instance=service)
        return render(request, "service/update.html",context={"form": form,"service": service})

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form =  ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("service-list")

        return render(request, "service/update.html",context={"form": form,"service": service})

class ServiceDetailView(View):
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        return render(request, "service/detail.html",context={"service": service})

class ServiceDeleteView(View):
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        return render(request, "service/delete.html", context={"service": service})

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return redirect("service-list")

class CategoryProducts(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category_products = category.services.all()

        return render(request,"category/services.html",context={"category": category, "category_products": category_products})