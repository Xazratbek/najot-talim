from django.urls import path
from .views import *

urlpatterns = [
    path("edition/", EditionListView.as_view(), name="edition-list"),
    path("edition/<str:edition>/", EditionDetailView.as_view(), name="edition-detail"),
    path("ayah/", AyahListView.as_view(), name="ayah-list"),
    path("surah/", SurahListView.as_view(), name="surah-list"),
    path("surah/<int:number>/", SurahDetailView.as_view(), name="surah-detail"),
    path("surah/<int:number>/<str:edition>/", SurahEditionDetailView.as_view(), name="surah-edition-detail"),
    path("juz/", JuzListView.as_view(), name="juz-list"),
    path("juz/<int:number>/", JuzDetailView.as_view(), name="juz-detail"),
]
