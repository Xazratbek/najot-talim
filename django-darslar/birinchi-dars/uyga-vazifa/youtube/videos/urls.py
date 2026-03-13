from django.urls import path
from .views import *

urlpatterns = [
    path("",get_videos,name="get_videos"),
    path("<int:id>/",get_video_by_id,name="get_video_by_id")
]
