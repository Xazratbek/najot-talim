from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CategoryForm, OrderForm, OrderItemForm, TelefonForm
from .models import Category, Order, OrderItem, Telefon


class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, "category/create.html", {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("category_list")

        return render(request, "category/create.html", {"form": form})


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "category/list.html", context={"categories": categories})


class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related("phones"), pk=pk)
        telefonlar = category.phones.all()
        return render(
            request,
            "category/detail.html",
            context={"category": category, "telefonlar": telefonlar},
        )


class CategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)

        return render(request, "category/update.html", context={"form": form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")

        return render(request, "category/update.html", context={"form": form})


class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, "category/delete.html", context={"category": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect("category_list")


class TelefonCreateView(View):
    def get(self, request):
        form = TelefonForm()
        return render(request, "telefon/create.html", context={"form": form})

    def post(self, request):
        form = TelefonForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("telefon_list")

        return render(request, "telefon/create.html", context={"form": form})


class TelefonListView(View):
    def get(self, request):
        telefonlar = Telefon.objects.all()
        return render(request, "telefon/list.html", context={"telefonlar": telefonlar})


class TelefonUpdateView(View):
    def get(self, request, pk):
        telefon = get_object_or_404(Telefon, pk=pk)
        form = TelefonForm(instance=telefon)

        return render(request, "telefon/update.html", context={"form": form})

    def post(self, request, pk):
        telefon = get_object_or_404(Telefon, pk=pk)
        form = TelefonForm(request.POST, request.FILES, instance=telefon)
        if form.is_valid():
            form.save()
            return redirect("telefon_list")

        return render(request, "telefon/update.html", context={"form": form})


class TelefonDetailView(View):
    def get(self, request, pk):
        telefon = get_object_or_404(Telefon.objects.select_related("category"), pk=pk)
        return render(request, "telefon/detail.html", context={"telefon": telefon})


class TelefonDeleteView(View):
    def get(self, request, pk):
        telefon = get_object_or_404(Telefon, pk=pk)
        return render(request, "telefon/delete.html", context={"telefon": telefon})

    def post(self, request, pk):
        telefon = get_object_or_404(Telefon, pk=pk)
        telefon.delete()
        return redirect("telefon_list")

class OrderCreateView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, "order/create.html", context={"form": form})

    def post(self, request):
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("order_list")

        return render(request, "order/create.html", context={"form": form})


class OrderListView(View):
    def get(self, request):
        orders = Order.objects.select_related("user").prefetch_related("items").order_by("-id")
        return render(request, "order/list.html", context={"orders": orders})


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.select_related("user").prefetch_related("items__telefon"),
            pk=pk,
        )
        order_items = order.items.all()
        return render(
            request,
            "order/detail.html",
            context={"order": order, "order_items": order_items},
        )


class OrderUpdateView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(instance=order)
        return render(request, "order/update.html", context={"form": form, "order": order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect("order_list")

        return render(request, "order/update.html", context={"form": form, "order": order})


class OrderDeleteView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, "order/delete.html", context={"order": order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect("order_list")


class OrderItemCreateView(View):
    def get(self, request):
        form = OrderItemForm()
        return render(request, "orderitem/create.html", context={"form": form})

    def post(self, request):
        form = OrderItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("orderitem_list")

        return render(request, "orderitem/create.html", context={"form": form})


class OrderItemListView(View):
    def get(self, request):
        order_items = OrderItem.objects.select_related("order__user", "telefon").order_by("-id")
        return render(request, "orderitem/list.html", context={"order_items": order_items})


class OrderItemDetailView(View):
    def get(self, request, pk):
        order_item = get_object_or_404(
            OrderItem.objects.select_related("order__user", "telefon", "telefon__category"),
            pk=pk,
        )
        return render(
            request,
            "orderitem/detail.html",
            context={"order_item": order_item},
        )


class OrderItemUpdateView(View):
    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        form = OrderItemForm(instance=order_item)
        return render(
            request,
            "orderitem/update.html",
            context={"form": form, "order_item": order_item},
        )

    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        form = OrderItemForm(request.POST, instance=order_item)

        if form.is_valid():
            form.save()
            return redirect("orderitem_list")

        return render(
            request,
            "orderitem/update.html",
            context={"form": form, "order_item": order_item},
        )


class OrderItemDeleteView(View):
    def get(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        return render(request, "orderitem/delete.html", context={"order_item": order_item})

    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, pk=pk)
        order_item.delete()
        return redirect("orderitem_list")
