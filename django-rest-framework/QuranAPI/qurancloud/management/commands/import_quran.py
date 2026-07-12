import json
from collections import defaultdict

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from qurancloud.models import Ayah, Edition, Juz, Surah

QURAN_API_BASE = "https://api.alquran.cloud/v1"
DEFAULT_EDITION = "quran-uthmani"


class Command(BaseCommand):
    help = (
        "Import the edition catalogue and the full Quran (114 surahs, all ayahs) "
        "from alquran.cloud (https://alquran.cloud/api) into the database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--edition",
            default=DEFAULT_EDITION,
            help="Edition identifier to import ayah text for (default: quran-uthmani).",
        )
        parser.add_argument(
            "--skip-editions",
            action="store_true",
            help="Skip importing the full edition catalogue (178 editions).",
        )
        parser.add_argument(
            "--skip-juz",
            action="store_true",
            help="Skip building the 30 Juz groupings from imported ayahs.",
        )
        parser.add_argument(
            "--editions-file",
            default=None,
            help=(
                "Path to a local JSON file with the same shape as "
                "GET https://api.alquran.cloud/v1/edition, used instead of "
                "calling the network (useful when the host's IP is rate-limited)."
            ),
        )
        parser.add_argument(
            "--quran-file",
            default=None,
            help=(
                "Path to a local JSON file with the same shape as "
                "GET https://api.alquran.cloud/v1/quran/<edition>, used instead of "
                "calling the network (useful when the host's IP is rate-limited)."
            ),
        )

    def handle(self, *args, **options):
        if not options["skip_editions"]:
            self.import_editions(options["editions_file"])

        edition = self.import_quran(options["edition"], options["quran_file"])

        if not options["skip_juz"]:
            self.build_juz(edition)

        self.stdout.write(self.style.SUCCESS("Quran import complete."))

    def import_editions(self, editions_file=None):
        if editions_file:
            self.stdout.write(f"Loading edition catalogue from {editions_file}...")
            with open(editions_file) as fh:
                editions_data = json.load(fh)["data"]
        else:
            self.stdout.write("Fetching edition catalogue...")
            response = requests.get(f"{QURAN_API_BASE}/edition", timeout=30)
            response.raise_for_status()
            editions_data = response.json()["data"]

        existing = set(Edition.objects.values_list("identifier", flat=True))
        new_editions = [
            Edition(
                identifier=e["identifier"],
                language=e["language"],
                name=e["name"],
                englishName=e["englishName"],
                format=e["format"],
                type=e["type"],
                direction=e.get("direction"),
            )
            for e in editions_data
            if e["identifier"] not in existing
        ]
        Edition.objects.bulk_create(new_editions, ignore_conflicts=True)
        self.stdout.write(
            f"Editions: {len(new_editions)} created, "
            f"{len(editions_data) - len(new_editions)} already present."
        )

    @transaction.atomic
    def import_quran(self, edition_identifier, quran_file=None):
        if quran_file:
            self.stdout.write(f"Loading full Quran text from {quran_file}...")
            with open(quran_file) as fh:
                payload = json.load(fh)["data"]
        else:
            self.stdout.write(f"Fetching full Quran text (edition={edition_identifier})...")
            response = requests.get(f"{QURAN_API_BASE}/quran/{edition_identifier}", timeout=60)
            response.raise_for_status()
            payload = response.json()["data"]

        edition_data = payload["edition"]
        edition, _ = Edition.objects.get_or_create(
            identifier=edition_data["identifier"],
            defaults=dict(
                language=edition_data["language"],
                name=edition_data["name"],
                englishName=edition_data["englishName"],
                format=edition_data["format"],
                type=edition_data["type"],
                direction=edition_data.get("direction"),
            ),
        )

        surahs_payload = payload["surahs"]

        existing_surah_numbers = set(Surah.objects.values_list("number", flat=True))
        new_surahs = [
            Surah(
                number=s["number"],
                name=s["name"],
                english_name=s["englishName"],
                english_name_translation=s["englishNameTranslation"],
                revelation_type=s["revelationType"],
                numberOfAyahs=len(s["ayahs"]),
            )
            for s in surahs_payload
            if s["number"] not in existing_surah_numbers
        ]
        Surah.objects.bulk_create(new_surahs, ignore_conflicts=True)
        self.stdout.write(
            f"Surahs: {len(new_surahs)} created, "
            f"{len(surahs_payload) - len(new_surahs)} already present."
        )

        surah_by_number = {s.number: s for s in Surah.objects.all()}
        already_imported = set(
            Ayah.objects.filter(edition=edition).values_list("surah__number", "number_in_surah")
        )

        new_ayahs = []
        for s in surahs_payload:
            surah = surah_by_number[s["number"]]
            for a in s["ayahs"]:
                if (s["number"], a["numberInSurah"]) in already_imported:
                    continue

                sajda = a.get("sajda")
                sajda_detail = sajda if isinstance(sajda, dict) else {}

                audio_secondary = a.get("audioSecondary")
                if isinstance(audio_secondary, list):
                    audio_secondary = ",".join(audio_secondary) or None

                new_ayahs.append(
                    Ayah(
                        number=a["number"],
                        text=a["text"],
                        number_in_surah=a["numberInSurah"],
                        juz=a["juz"],
                        manzil=a["manzil"],
                        page=a["page"],
                        ruku=a["ruku"],
                        hizb_quarter=a["hizbQuarter"],
                        sajda=bool(sajda),
                        sajda_obligatory=sajda_detail.get("obligatory", False),
                        sajda_recommended=sajda_detail.get("recommended", False),
                        audio=a.get("audio"),
                        audio_secondary=audio_secondary,
                        surah=surah,
                        edition=edition,
                    )
                )

        Ayah.objects.bulk_create(new_ayahs, batch_size=1000, ignore_conflicts=True)
        self.stdout.write(
            f"Ayahs: {len(new_ayahs)} created for edition '{edition.identifier}'."
        )
        return edition

    def build_juz(self, edition):
        self.stdout.write("Building Juz groupings...")
        ayahs = Ayah.objects.filter(edition=edition).only("id", "juz", "surah_id")

        juz_ayah_ids = defaultdict(list)
        juz_surah_ids = defaultdict(set)
        for a in ayahs:
            juz_ayah_ids[a.juz].append(a.id)
            juz_surah_ids[a.juz].add(a.surah_id)

        existing = set(Juz.objects.filter(edition=edition).values_list("number", flat=True))
        created_count = 0
        for number, ayah_ids in juz_ayah_ids.items():
            juz, created = Juz.objects.get_or_create(number=number, edition=edition)
            created_count += int(created)
            juz.ayahs.set(ayah_ids)
            juz.surahs.set(juz_surah_ids[number])

        self.stdout.write(
            f"Juz: {created_count} created, {len(existing)} already present."
        )
