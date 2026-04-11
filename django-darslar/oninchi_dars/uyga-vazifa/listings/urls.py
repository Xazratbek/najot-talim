from django.urls import path
from .views import *

app_name = "listing"

urlpatterns = [
    path("",ListingListView.as_view(),name="list"),
    path("<uuid:uuid>/",ListingDetailView.as_view(),name="detail"),
    path("delete/<uuid:uuid>/",ListingDeleteView.as_view(),name="delete"),
    path("create/",ListingCreateView.as_view(),name="create"),
    path("update/<uuid:uuid>/",ListingUpdateView.as_view(),name="update"),
]
