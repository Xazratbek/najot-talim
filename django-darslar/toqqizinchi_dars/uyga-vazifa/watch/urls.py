from django.urls import path
from .models import Category
from .views import *

app_name = "watch"

urlpatterns = [
    path("", ProductsListView.as_view(), name="products"),
    path("category/<int:pk>/",CategoryProducts.as_view(),name="category-products"),
    path("create/",ProductCreateView.as_view(),name="product-create"),
    path("update/<int:pk>/",ProductUpdateView.as_view(),name="product-update"),
    path("detail/<int:pk>/",ProductDetailView.as_view(),name="product-detail"),
    path("my_products/",MyProducts.as_view(),name="my-products"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product-delete")
]
