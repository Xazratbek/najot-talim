from django.urls import path
from .views import CategoryListView, CategoryDetailView

app_name = "category"

urlpatterns = [
    path("",CategoryListView.as_view(),name="list"),
    path("<str:slug>/",CategoryDetailView.as_view(),name="detail"),

]
