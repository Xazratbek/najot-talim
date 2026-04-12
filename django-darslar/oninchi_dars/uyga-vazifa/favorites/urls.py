from django.urls import path
from .views import ToggleFavoriteView

app_name = 'favorites'

urlpatterns = [
    path('toggle-favorite/<uuid:uuid>/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

]
