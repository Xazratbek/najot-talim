from django.urls import path
from .views import *


urlpatterns = [
    path("categories/", CategoryListView.as_view(),name="category-list"),
    path("category/detail/<int:pk>/", CategoryDetailView.as_view(),name="category-detail"),
    path("category/update/<int:pk>/", CategoryUpdateView.as_view(),name="category-update"),
    path("category/delete/<int:pk>/", CategoryDeleteView.as_view(),name="category-delete"),
    # path("category/create/", categry_creat_view,name="category-create"),
    path("category/create/", CategoryCreateView.as_view(),name="category-create"),
    path("category/products/<int:pk>/", CategoryProducts.as_view(),name="category-products"),

    path("", ServiceListView.as_view(),name="service-list"),
    path("create/", ServiceCreateView.as_view(),name="service-create"),
    path("update/<int:pk>/", ServiceUpdateView.as_view(),name="service-update"),
    path("detail/<int:pk>/", ServiceDetailView.as_view(),name="service-detail"),
    path("delete/<int:pk>/", ServiceDeleteView.as_view(),name="service-delete"),
]
