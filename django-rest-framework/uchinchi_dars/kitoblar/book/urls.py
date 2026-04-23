from django.urls import path
from .views import BookListCreateApiView, UpdateDestroyDetailView

urlpatterns = [
    path("list-create/",BookListCreateApiView.as_view(),name='list-create'),
    path("update-destroy-detail/<int:pk>/",UpdateDestroyDetailView.as_view(),name='update-detail-destroy'),
]
