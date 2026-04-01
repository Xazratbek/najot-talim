from django.urls import path
from .views import *

urlpatterns = [
    path("",CarListView.as_view(),name="cars-list"),
    path("update/<int:pk>/",CarUpdateView.as_view(),name="cars-update"),
    path("delete/<int:pk>/",CarDeleteView.as_view(),name="cars-delete"),
    path("detail/<int:pk>/",CarDetailView.as_view(),name="cars-detail"),
    path("create/",CarCreateView.as_view(),name="cars-create"),

    path('categories/',CategoryListView.as_view(),name="category-list"),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name="category-update"),
    path('category/delete/<int:pk>',CategoryDeleteView.as_view(),name="category-delete"),
    path('category/<int:pk>/',CategoryDetailView.as_view(),name="category-detail"),
    path('category/create/',CategoryCreatView.as_view(),name="category-create"),
    path("search/",CarsSearchView.as_view(),name="search")

]
