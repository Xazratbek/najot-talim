from .views import ServiceListView, ServiceCreateView, ServiceUpdateView,ServiceDeleteView
from django.urls import path

urlpatterns = [
    path('list/',ServiceListView.as_view(),name='service-list'),
    path('create/',ServiceCreateView.as_view(),name='service-create'),
    path('update/<int:pk>/',ServiceUpdateView.as_view(),name='service-put-update'),
    path('delete/<int:pk>/',ServiceDeleteView.as_view(),name='service-delete')
]
