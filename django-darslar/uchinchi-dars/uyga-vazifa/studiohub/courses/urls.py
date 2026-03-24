from django.urls import path
from .views import *


urlpatterns = [
    path("",course_list,name="course-list"),
    path("add/",add_course,name="add-course"),
    path("update/<int:id>/",update_course,name="update-course"),
    path("delete/<int:id>/",delete_course,name="delete-course"),
    path("detail/<int:id>/",course_detail,name="course-detail"),
]
