from django.urls import path
from .views import *

urlpatterns = [
    path("",get_lessons,name="student_list"),
    path("<int:student_id>/",get_lesson_by_id,name="student_detail"),
]
