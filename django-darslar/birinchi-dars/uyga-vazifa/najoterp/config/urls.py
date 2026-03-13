
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("students/",include("users.urls")),
    path("lessons/",include("lessons.urls")),
]
