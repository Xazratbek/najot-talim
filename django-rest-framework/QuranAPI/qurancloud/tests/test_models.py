from django.db import IntegrityError, transaction
from django.test import TestCase

from .factories import make_ayah, make_edition, make_juz, make_surah


class EditionModelTests(TestCase):
    def test_str_returns_identifier(self):
        edition = make_edition(identifier="en.sahih")
        self.assertEqual(str(edition), "en.sahih")

    def test_identifier_is_unique(self):
        make_edition(identifier="quran-uthmani")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_edition(identifier="quran-uthmani")

    def test_timestamps_are_auto_populated(self):
        edition = make_edition()
        self.assertIsNotNone(edition.created_at)
        self.assertIsNotNone(edition.updated_at)


class SurahModelTests(TestCase):
    def test_str_returns_english_name(self):
        surah = make_surah(english_name="Al-Baqara")
        self.assertEqual(str(surah), "Al-Baqara")

    def test_number_is_unique(self):
        make_surah(number=2)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_surah(number=2)

    def test_default_ordering_by_number(self):
        make_surah(number=3, english_name="Aal-Imran")
        make_surah(number=1, english_name="Al-Faatiha")
        make_surah(number=2, english_name="Al-Baqara")
        from qurancloud.models import Surah

        numbers = list(Surah.objects.values_list("number", flat=True))
        self.assertEqual(numbers, [1, 2, 3])


class AyahModelTests(TestCase):
    def setUp(self):
        self.edition = make_edition()
        self.surah = make_surah()

    def test_str_includes_surah_and_number(self):
        ayah = make_ayah(self.surah, self.edition, number=1)
        self.assertIn(self.surah.english_name, str(ayah))
        self.assertIn("1", str(ayah))

    def test_sajda_details_default_false(self):
        ayah = make_ayah(self.surah, self.edition)
        self.assertFalse(ayah.sajda)
        self.assertFalse(ayah.sajda_obligatory)
        self.assertFalse(ayah.sajda_recommended)

    def test_sajda_detail_can_be_set(self):
        ayah = make_ayah(
            self.surah,
            self.edition,
            number_in_surah=206,
            sajda=True,
            sajda_recommended=True,
            sajda_obligatory=False,
        )
        self.assertTrue(ayah.sajda)
        self.assertTrue(ayah.sajda_recommended)
        self.assertFalse(ayah.sajda_obligatory)

    def test_unique_together_surah_edition_number_in_surah(self):
        make_ayah(self.surah, self.edition, number_in_surah=1)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_ayah(self.surah, self.edition, number_in_surah=1)


class JuzModelTests(TestCase):
    def setUp(self):
        self.edition = make_edition()
        self.surah = make_surah()
        self.ayah = make_ayah(self.surah, self.edition)

    def test_str_includes_number(self):
        juz = make_juz(self.edition, number=1)
        self.assertEqual(str(juz), "Juz: 1")

    def test_relations(self):
        juz = make_juz(self.edition, number=1, ayahs=[self.ayah], surahs=[self.surah])
        self.assertIn(self.ayah, juz.ayahs.all())
        self.assertIn(self.surah, juz.surahs.all())

    def test_unique_together_number_edition(self):
        make_juz(self.edition, number=1)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_juz(self.edition, number=1)
