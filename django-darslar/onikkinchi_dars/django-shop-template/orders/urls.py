from .views import add_card, my_cart, remove_cart_item
from django.urls import path

urlpatterns = [
    path("add/to/cart/",add_card,name='add-to-cart'),
    path("my_cart/",my_cart,name='my-cart'),
    path("remove/<uuid:item_id>/", remove_cart_item, name='remove-cart-item'),
]
