from django.urls import path
from .views import BlogView, BlogDetailView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('post/<uuid:id>', BlogDetailView.as_view(), name='blog-detail'),
]
