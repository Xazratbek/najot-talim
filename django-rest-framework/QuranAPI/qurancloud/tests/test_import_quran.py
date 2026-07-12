from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase

from qurancloud.models import Ayah, Edition, Juz, Surah

EDITIONS_PAYLOAD = {
    "data": [
        {
            "identifier": "quran-uthmani",
            "language": "ar",
            "name": "القرآن الكريم",
            "englishName": "Uthmani",
            "format": "text",
            "type": "quran",
            "direction": "rtl",
        },
        {
            "identifier": "en.sahih",
            "language": "en",
            "name": "Sahih International",
            "englishName": "Saheeh International",
            "format": "text",
            "type": "translation",
            "direction": "ltr",
        },
    ]
}

QURAN_PAYLOAD = {
    "data": {
        "edition": {
            "identifier": "quran-uthmani",
            "language": "ar",
            "name": "القرآن الكريم",
            "englishName": "Uthmani",
            "format": "text",
            "type": "quran",
            "direction": "rtl",
        },
        "surahs": [
            {
                "number": 1,
                "name": "سُورَةُ ٱلْفَاتِحَةِ",
                "englishName": "Al-Faatiha",
                "englishNameTranslation": "The Opening",
                "revelationType": "Meccan",
                "ayahs": [
                    {
                        "number": 1,
                        "text": "بِسْمِ اللَّهِ",
                        "numberInSurah": 1,
                        "juz": 1,
                        "manzil": 1,
                        "page": 1,
                        "ruku": 1,
                        "hizbQuarter": 1,
                        "sajda": False,
                    },
                    {
                        "number": 2,
                        "text": "الْحَمْدُ لِلَّهِ",
                        "numberInSurah": 2,
                        "juz": 1,
                        "manzil": 1,
                        "page": 1,
                        "ruku": 1,
                        "hizbQuarter": 1,
                        "sajda": {"id": 1, "recommended": True, "obligatory": False},
                        "audioSecondary": ["https://example.com/1.mp3", "https://example.com/2.mp3"],
                    },
                ],
            }
        ],
    }
}


def _mock_response(payload):
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = payload
    return response


def _fake_get(url, timeout=30):
    if url.endswith("/edition"):
        return _mock_response(EDITIONS_PAYLOAD)
    if "/quran/" in url:
        return _mock_response(QURAN_PAYLOAD)
    raise AssertionError(f"Unexpected URL requested: {url}")


class ImportQuranCommandTests(TestCase):
    @patch("qurancloud.management.commands.import_quran.requests.get", side_effect=_fake_get)
    def test_import_creates_editions_surahs_ayahs_juz(self, mock_get):
        out = StringIO()
        call_command("import_quran", stdout=out)

        self.assertEqual(Edition.objects.count(), 2)
        self.assertEqual(Surah.objects.count(), 1)
        self.assertEqual(Ayah.objects.count(), 2)
        self.assertEqual(Juz.objects.count(), 1)

        sajda_ayah = Ayah.objects.get(number_in_surah=2)
        self.assertTrue(sajda_ayah.sajda)
        self.assertTrue(sajda_ayah.sajda_recommended)
        self.assertFalse(sajda_ayah.sajda_obligatory)
        self.assertEqual(
            sajda_ayah.audio_secondary,
            "https://example.com/1.mp3,https://example.com/2.mp3",
        )

        plain_ayah = Ayah.objects.get(number_in_surah=1)
        self.assertFalse(plain_ayah.sajda)

    @patch("qurancloud.management.commands.import_quran.requests.get", side_effect=_fake_get)
    def test_import_is_idempotent(self, mock_get):
        call_command("import_quran", stdout=StringIO())
        call_command("import_quran", stdout=StringIO())

        self.assertEqual(Edition.objects.count(), 2)
        self.assertEqual(Surah.objects.count(), 1)
        self.assertEqual(Ayah.objects.count(), 2)
        self.assertEqual(Juz.objects.count(), 1)

    @patch("qurancloud.management.commands.import_quran.requests.get", side_effect=_fake_get)
    def test_skip_editions_still_creates_import_edition(self, mock_get):
        call_command("import_quran", "--skip-editions", stdout=StringIO())

        called_urls = [call.args[0] for call in mock_get.call_args_list]
        self.assertFalse(any(url.endswith("/edition") for url in called_urls))
        self.assertEqual(Edition.objects.count(), 1)
        self.assertEqual(Edition.objects.get().identifier, "quran-uthmani")

    @patch("qurancloud.management.commands.import_quran.requests.get", side_effect=_fake_get)
    def test_skip_juz_does_not_create_juz(self, mock_get):
        call_command("import_quran", "--skip-juz", stdout=StringIO())
        self.assertEqual(Juz.objects.count(), 0)
