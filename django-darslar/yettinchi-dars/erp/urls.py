from django.urls import path
from .views import *


urlpatterns = [
    path("students/",StudentListView.as_view(),name="student-list"),
    path("student/update/<int:pk>/",StudentUpdateView.as_view(),name="student-update"),
    path("student/delete/<int:pk>/",StudentDeleteView.as_view(),name="student-delete"),
    path("student/<int:pk>/",StudentDetailView.as_view(),name="student-detail"),
    path("student/create/",StudentCreateView.as_view(),name="student-create"),

    ######### Teacher urllari
    path("teachers/",TeacherListView.as_view(),name="teacher-list"),
    path("teacher/update/<int:pk>/",TeacherUpdateView.as_view(),name="teacher-update"),
    path("teacher/delete/<int:pk>/",TeacherDeleteView.as_view(),name="teacher-delete"),
    path("teacher/<int:pk>/",TeacherDetailView.as_view(),name="teacher-detail"),
    path("teacher/create/",TeacherCreateView.as_view(),name="teacher-create"),

    ######## Guruh urllari

    path("",GuruhListView.as_view(),name="guruh-list"),
    path("guruh/update/<int:pk>/",GuruhUpdateView.as_view(),name="guruh-update"),
    path("guruh/delete/<int:pk>/",GuruhDeleteView.as_view(),name="guruh-delete"),
    path("guruh/<int:pk>/",GuruhDetailView.as_view(),name="guruh-detail"),
    path("guruh/create/",GuruhCreateView.as_view(),name="guruh-create"),
]
