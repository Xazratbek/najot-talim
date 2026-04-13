from django.urls import path
from .views import IndexView, ProductDetailView

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("product/<uuid:id>/",ProductDetailView.as_view(),name="product_detail")
]
