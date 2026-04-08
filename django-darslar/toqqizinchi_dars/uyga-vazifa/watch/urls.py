from django.urls import path
from .models import Category
from .views import CategoryProducts, ProductsListView


app_name = "watch"

urlpatterns = [
    path("", ProductsListView.as_view(), name="products"),
    path("category/<int:pk>/",CategoryProducts.as_view(),name="category-products")
]
