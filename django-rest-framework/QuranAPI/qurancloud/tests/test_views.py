from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import make_ayah, make_edition, make_juz, make_surah


class EditionAPITests(APITestCase):
    def setUp(self):
        self.quran_edition = make_edition(
            identifier="quran-uthmani", language="ar", format="text", type="quran"
        )
        self.translation_edition = make_edition(
            identifier="en.sahih",
            language="en",
            format="text",
            type="translation",
            name="Sahih International",
            englishName="Saheeh International",
        )

    def test_list_editions(self):
        url = reverse("edition-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_editions_by_language(self):
        url = reverse("edition-list")
        response = self.client.get(url, {"language": "en"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        identifiers = [item["identifier"] for item in response.data["results"]]
        self.assertEqual(identifiers, ["en.sahih"])

    def test_search_editions(self):
        url = reverse("edition-list")
        response = self.client.get(url, {"search": "Saheeh"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["identifier"], "en.sahih")

    def test_search_editions_no_match(self):
        url = reverse("edition-list")
        response = self.client.get(url, {"search": "no-such-edition"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_retrieve_edition_by_identifier(self):
        url = reverse("edition-detail", kwargs={"edition": "quran-uthmani"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identifier"], "quran-uthmani")

    def test_retrieve_unknown_edition_returns_404(self):
        url = reverse("edition-detail", kwargs={"edition": "does-not-exist"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SurahAPITests(APITestCase):
    def setUp(self):
        self.edition = make_edition(identifier="quran-uthmani")
        self.other_edition = make_edition(identifier="en.sahih", language="en", type="translation")
        self.surah = make_surah(number=1, english_name="Al-Faatiha", numberOfAyahs=2)
        make_ayah(self.surah, self.edition, number=1, number_in_surah=1, text="Ar")
        make_ayah(self.surah, self.edition, number=2, number_in_surah=2, text="Ar2")
        make_ayah(self.surah, self.other_edition, number=1, number_in_surah=1, text="En")

    def test_list_surahs(self):
        url = reverse("surah-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_surah_by_number_returns_all_editions_ayahs(self):
        url = reverse("surah-detail", kwargs={"number": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], 1)
        self.assertEqual(len(response.data["ayahs"]), 3)

    def test_retrieve_surah_filtered_by_edition(self):
        url = reverse("surah-edition-detail", kwargs={"number": 1, "edition": "quran-uthmani"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["ayahs"]), 2)
        for ayah in response.data["ayahs"]:
            self.assertEqual(ayah["edition"], self.edition.id)

    def test_retrieve_unknown_surah_returns_404(self):
        url = reverse("surah-detail", kwargs={"number": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AyahAPITests(APITestCase):
    def setUp(self):
        self.edition = make_edition(identifier="quran-uthmani")
        self.surah1 = make_surah(number=1, english_name="Al-Faatiha")
        self.surah2 = make_surah(number=2, english_name="Al-Baqara")
        make_ayah(self.surah1, self.edition, number=1, number_in_surah=1, juz=1, page=1)
        make_ayah(
            self.surah2,
            self.edition,
            number=8,
            number_in_surah=1,
            juz=1,
            page=2,
            sajda=True,
            sajda_recommended=True,
        )

    def test_list_ayahs(self):
        url = reverse("ayah-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_ayahs_by_surah_number(self):
        url = reverse("ayah-list")
        response = self.client.get(url, {"surah__number": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["surah"]["number"], 2)

    def test_filter_ayahs_by_sajda(self):
        url = reverse("ayah-list")
        response = self.client.get(url, {"sajda": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertTrue(response.data["results"][0]["sajda_recommended"])


class JuzAPITests(APITestCase):
    def setUp(self):
        self.edition = make_edition(identifier="quran-uthmani")
        self.surah = make_surah(number=1)
        self.ayah = make_ayah(self.surah, self.edition)
        self.juz = make_juz(self.edition, number=1, ayahs=[self.ayah], surahs=[self.surah])

    def test_list_juz(self):
        url = reverse("juz-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_juz_by_number(self):
        url = reverse("juz-detail", kwargs={"number": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["ayahs"]), 1)
        self.assertEqual(len(response.data["surahs"]), 1)

    def test_retrieve_unknown_juz_returns_404(self):
        url = reverse("juz-detail", kwargs={"number": 30})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SwaggerSchemaTests(APITestCase):
    def test_swagger_ui_is_reachable(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
