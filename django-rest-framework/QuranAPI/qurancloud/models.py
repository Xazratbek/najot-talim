from django.db import models
from utils.models import BaseModel


class Edition(BaseModel):
    identifier = models.CharField(max_length=1000, unique=True)
    language = models.CharField(max_length=50)
    name = models.TextField()
    englishName = models.CharField(max_length=500)
    format = models.CharField(max_length=128)
    type = models.CharField(max_length=150)
    direction = models.CharField(max_length=80, null=True)

    class Meta:
        ordering = ["identifier"]

    def __str__(self):
        return self.identifier


class Ayah(BaseModel):
    number = models.PositiveIntegerField()
    text = models.TextField()
    number_in_surah = models.PositiveIntegerField()
    juz = models.PositiveIntegerField()
    manzil = models.PositiveIntegerField()
    page = models.PositiveIntegerField()
    ruku = models.PositiveIntegerField()
    hizb_quarter = models.PositiveIntegerField()
    sajda = models.BooleanField(default=False)
    sajda_obligatory = models.BooleanField(default=False)
    sajda_recommended = models.BooleanField(default=False)
    audio = models.CharField(max_length=600, null=True, blank=True)

    audio_secondary = models.CharField(max_length=600, null=True, blank=True)

    surah = models.ForeignKey(
        "qurancloud.Surah", on_delete=models.CASCADE, related_name="ayahs"
    )
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)

    class Meta:
        ordering = ["number"]
        unique_together = ("surah", "edition", "number_in_surah")

    def __str__(self):
        return f"{self.surah.english_name} - Ayah {self.number}"


class Surah(BaseModel):
    number = models.PositiveIntegerField(unique=True)
    name = models.TextField()
    english_name = models.CharField(max_length=255)
    english_name_translation = models.CharField(max_length=255)
    revelation_type = models.CharField(max_length=255)
    numberOfAyahs = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return str(self.english_name)


class Juz(BaseModel):
    number = models.PositiveIntegerField()
    ayahs = models.ManyToManyField(Ayah, related_name="juzs")
    surahs = models.ManyToManyField(Surah, related_name="juzzsurahs")
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)

    class Meta:
        ordering = ["number"]
        unique_together = ("number", "edition")

    def __str__(self):
        return str(f"Juz: {self.number}")
