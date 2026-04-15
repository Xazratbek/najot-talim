from django.urls import path
from .views import *

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("search/", ProductSearchView.as_view(), name="product-search"),
    path("product/<uuid:id>/",ProductDetailView.as_view(),name="product_detail"),
    path("product/<uuid:product_id>/comment/create/", comment_create, name="comment-create"),
    path("comment/<uuid:comment_id>/update/", update_comment, name="comment-update"),
    path("comment/<uuid:comment_id>/delete/", delete_comment, name="comment-delete"),
    path('add/to/saved/<uuid:id>/',saved, name='add-to-saved'),
    path('wishlist/',user_saveds,name='wishlist'),
    path('recently/', user_recently, name='recently'),
]
