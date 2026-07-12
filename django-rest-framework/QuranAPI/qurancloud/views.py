from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializer import *


class EditionListView(ListAPIView):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    filterset_fields = ["format", "language", "type"]
    search_fields = ["identifier", "name", "englishName"]


class EditionDetailView(RetrieveAPIView):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    lookup_field = "identifier"
    lookup_url_kwarg = "edition"


class AyahListView(ListAPIView):
    queryset = Ayah.objects.select_related("surah", "edition").all()
    serializer_class = AyahSerializer
    filterset_fields = ["surah__number", "edition__identifier", "juz", "page", "sajda"]


class SurahListView(ListAPIView):
    queryset = Surah.objects.prefetch_related("ayahs")
    serializer_class = SurahSerializer


class SurahDetailView(RetrieveAPIView):
    queryset = Surah.objects.prefetch_related("ayahs")
    serializer_class = SurahSerializer
    lookup_field = "number"
    lookup_url_kwarg = "number"


class SurahEditionDetailView(RetrieveAPIView):
    serializer_class = SurahSerializer
    lookup_field = "number"
    lookup_url_kwarg = "number"

    def get_queryset(self):
        edition = self.kwargs["edition"]
        return Surah.objects.prefetch_related(
            Prefetch("ayahs", queryset=Ayah.objects.filter(edition__identifier=edition))
        )


class JuzListView(ListAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer


class JuzDetailView(RetrieveAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    lookup_field = "number"
    lookup_url_kwarg = "number"
