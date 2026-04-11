from django.shortcuts import render, get_object_or_404
from .models import Category
from django.views.generic import ListView, DetailView
from django.db.models import Q
from listings.models import Listing


class CategoryListView(ListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related("categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_listings"] = (
            Listing.objects.filter(status="active")
            .select_related("user", "listing_category")
            .prefetch_related("images")
            .order_by("-view_count")[:12]
        )
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = "categories/detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Category.objects.prefetch_related("categories"),
            slug=self.kwargs.get("slug"),
        )

    def get_category_listings(self):
        category = self.object

        if category.categories.exists():
            categories = [category.id] + list(
                category.categories.values_list("id", flat=True)
            )
            queryset = Listing.objects.filter(
                listing_category_id__in=categories,
                status="active",
            )
        else:
            queryset = Listing.objects.filter(
                listing_category=category,
                status="active",
            )

        q = self.request.GET.get("q", "")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(city__icontains=q)
            )

        price_from = self.request.GET.get("price_from", "")
        if price_from:
            queryset = queryset.filter(price__gte=price_from)

        price_to = self.request.GET.get("price_to", "")
        if price_to:
            queryset = queryset.filter(price__lte=price_to)

        currency = self.request.GET.get("currency", "")
        if currency:
            queryset = queryset.filter(currency=currency)

        condition = self.request.GET.get("condition", "")
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.select_related("user", "listing_category").prefetch_related("images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sub_categories"] = self.object.categories.all()
        context["category_listings"] = self.get_category_listings()
        context["listing_count"] = context["category_listings"].count()
        context["root_categories"] = Category.objects.filter(parent__isnull=True).prefetch_related("categories")
        context["current_q"] = self.request.GET.get("q", "")
        context["current_price_from"] = self.request.GET.get("price_from", "")
        context["current_price_to"] = self.request.GET.get("price_to", "")
        context["current_currency"] = self.request.GET.get("currency", "")
        context["current_condition"] = self.request.GET.get("condition", "")

        return context
