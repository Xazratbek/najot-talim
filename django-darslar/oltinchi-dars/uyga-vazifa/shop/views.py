from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import CategoryForm, CarsForm
from django.db.models import Q

# class CategoryCreatView(CreateView):
#     model = Category
#     template_name = "category/create.html"

# class CategoryUpdateView(UpdateView):
#     model = Category
#     template_name = "category/update.html"
#     fields = ["name"]

# class CategoryDeleteView(DeleteView):
#     model = Category
#     template_name = "category/delete.html"
#     success_url = reverse_lazy("category-list")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["category"] = self.get_object()

#         return context

# class CategoryListView(ListView):
#     model = Category
#     template_name = "category/list.html"
#     context_object_name = "categories"

# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = "category/detail.html"
#     context_object_name = "category"


# ##### Car viewlari


# class CarCreateView(CreateView):
#     model = Cars
#     template_name = "cars/create.html"

# class CarUpdateView(UpdateView):
#     model = Cars
#     template_name = "cars/update.html"
#     fields = ["make",'model','price',"category","photo","desc"]

# class CarDeleteView(DeleteView):
#     model = Cars
#     template_name = "cars/delete.html"
#     success_url = reverse_lazy("cars-list")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["cars"] = self.get_object()
#         return context

# class CarDetailView(DetailView):
#     model = Cars
#     template_name = "cars/detail.html"
#     context_object_name = "cars"

# class CarListView(ListView):
#     model = Cars
#     template_name = "cars/list.html"
#     context_object_name = "cars"


class CategoryCreatView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request,"category/create.html",context={"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category-list")

        return render(request,"category/create.html",context={"form": form})

class CategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category,pk=pk)
        form = CategoryForm(instance=category)
        return render(request,"category/update.html",context={"form": form})

    def post(self, request, pk):
        category = get_object_or_404(Category,pk=pk)
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect("category-list")

        return render(request,"category/update.html",context={"category":category,"form":form})

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "category/list.html",context={"categories":categories})

class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, "category/delete.html",context={"form": form,"category": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect("category-list")

class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, "category/detail.html",context={"category": category})

class CarCreateView(View):
    def get(self, request):
        form = CarsForm()
        return render(request, "cars/create.html",context={"form": form})

    def post(self, request):
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cars-list")

        return render(request,"cars/create.html",context={"form": form})

class CarDetailView(View):
    def get(self, request, pk):
        car = get_object_or_404(Cars,pk=pk)
        return render(request, "cars/detail.html",context={"cars": car})

class CarUpdateView(View):
    def get(self, request, pk):
        car = get_object_or_404(Cars, pk=pk)
        form = CarsForm(instance=car)

        return render(request,"cars/update.html",context={"cars": car,"form": form})

    def post(self, request, pk):
        car = get_object_or_404(Cars,pk=pk)
        form = CarsForm(request.POST, request.FILES,instance=car)
        if form.is_valid():
            form.save()
            return redirect("cars-list")

        return render(request, "cars/update.html",context={"form": form,"cars": car})

class CarListView(View):
    def get(self, request):
        cars = Cars.objects.all()
        return render(request, "cars/list.html",context={"cars":cars})

class CarDeleteView(View):
    def get(self, request, pk):
        car = get_object_or_404(Cars,pk=pk)
        form = CarsForm(instance=car)

        return render(request,"cars/delete.html",context={"form": form,"cars": car})

    def post(self, request, pk):
        car = get_object_or_404(Cars,pk=pk)
        car.delete()
        return redirect("cars-list")

class CarsSearchView(View):
    def get(self,request):
        q = request.GET.get("q","")
        cars = Cars.objects.filter(Q(model__icontains=q) | Q(desc__icontains=q))
        return render(request, "cars/search.html",context={"cars": cars})