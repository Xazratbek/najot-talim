from django.urls import path
from .views import ToggleFavoriteView

urlpatterns = [
    path('toggle-favorite/<uuid:uuid>/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

]
