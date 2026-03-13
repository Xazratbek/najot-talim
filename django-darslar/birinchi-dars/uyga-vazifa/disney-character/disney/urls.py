from django.urls import path
from .views import getOneCharacter, search_movies,search_movies_html

urlpatterns = [
    path("character/<int:character_id>/", getOneCharacter, name="get_one_character"),
    path("search/", search_movies, name="search_movies"),
    path("searchhtml/", search_movies_html, name="search_movies"),
]
