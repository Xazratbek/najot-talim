from django.urls import path
from .views import IndexView, ProductDetailView, saved, user_saveds

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("product/<uuid:id>/",ProductDetailView.as_view(),name="product_detail"),
    path('add/to/saved/<uuid:id>/',saved, name='add-to-saved'),
    path('wishlist/',user_saveds,name='wishlist')
]
