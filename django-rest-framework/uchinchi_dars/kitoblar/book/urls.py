from django.urls import path
# from .views import BookListCreateApiView, UpdateDestroyDetailView
from .views import mevalar, meva_qoshish

urlpatterns = [
    # path("list-create/",BookListCreateApiView.as_view(),name='list-create'),
    # path("update-destroy-detail/<int:pk>/",UpdateDestroyDetailView.as_view(),name='update-detail-destroy'),
    path('',mevalar),
    path('create/',meva_qoshish),
]
