from .views import add_card, my_cart, remove_cart_item, clear_cart,decrease_cart_item, my_orders
from django.urls import path

urlpatterns = [
    path("add/to/cart/",add_card,name='add-to-cart'),
    path("my_cart/",my_cart,name='my-cart'),
    path("remove/<uuid:item_id>/", remove_cart_item, name='remove-cart-item'),
    path("decrease/<uuid:item_id>/", decrease_cart_item, name='decrease-cart-item'),
    path('clear/<uuid:card_id>/',clear_cart,name='clear-card'),
    path("my_orders/",my_orders,name='my-orders')
]
