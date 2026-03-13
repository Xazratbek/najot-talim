from django.urls import path
from .views import *

urlpatterns = [
    path("",get_students,name="student_list"),
    path("<int:student_id>/",get_student_by_id,name="student_detail"),
]
