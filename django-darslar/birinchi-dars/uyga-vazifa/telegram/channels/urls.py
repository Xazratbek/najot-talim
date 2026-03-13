from django.urls import path
from .views import *

urlpatterns = [
    path("",get_channels_list,name="channels_list"),
    path("<int:id>/",get_channel_by_id,name="channel_id"),
    path("<int:id>/",join_to_channel,name="join_channel"),
]
