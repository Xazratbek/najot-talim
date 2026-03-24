from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='projects'),
    path('project/<int:id>/', views.project_details, name='project-detail'),
    path('add/', views.add_project, name='add-project'),
    path('update/<int:id>/', views.update_project, name='update-project'),
    path('delete/<int:id>/', views.delete_project, name='delete-project'),
]
