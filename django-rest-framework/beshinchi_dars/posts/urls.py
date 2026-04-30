from django.urls import path
from .views import *


urlpatterns = [
    path('',PostListAPIView.as_view()),
    path('create/',PostCreateAPIView.as_view()),
    path('update/<int:pk>/',PostUpdateAPIView.as_view()),
    path('detail/<int:pk>/',PostRetrieveAPIView.as_view()),
    path('delete/<int:pk>/',PostDestroyAPIView.as_view()),
]
