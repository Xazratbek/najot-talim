from django.urls import path
from .views import *

urlpatterns = [
    path("", BookListView.as_view(), name="books_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("edit/<int:pk>/", BookEditView.as_view(), name="book_edit"),
    path("delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
]
