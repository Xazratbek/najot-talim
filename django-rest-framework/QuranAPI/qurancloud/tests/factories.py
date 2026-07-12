from qurancloud.models import Ayah, Edition, Juz, Surah


def make_edition(**overrides):
    defaults = dict(
        identifier="quran-uthmani",
        language="ar",
        name="القرآن الكريم",
        englishName="Uthmani",
        format="text",
        type="quran",
        direction="rtl",
    )
    defaults.update(overrides)
    return Edition.objects.create(**defaults)


def make_surah(**overrides):
    defaults = dict(
        number=1,
        name="سُورَةُ ٱلْفَاتِحَةِ",
        english_name="Al-Faatiha",
        english_name_translation="The Opening",
        revelation_type="Meccan",
        numberOfAyahs=7,
    )
    defaults.update(overrides)
    return Surah.objects.create(**defaults)


def make_ayah(surah, edition, **overrides):
    defaults = dict(
        number=1,
        text="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        number_in_surah=1,
        juz=1,
        manzil=1,
        page=1,
        ruku=1,
        hizb_quarter=1,
        sajda=False,
        surah=surah,
        edition=edition,
    )
    defaults.update(overrides)
    return Ayah.objects.create(**defaults)


def make_juz(edition, number=1, ayahs=None, surahs=None):
    juz = Juz.objects.create(number=number, edition=edition)
    if ayahs:
        juz.ayahs.set(ayahs)
    if surahs:
        juz.surahs.set(surahs)
    return juz
