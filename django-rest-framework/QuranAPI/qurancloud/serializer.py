from rest_framework.serializers import ModelSerializer
from .models import *

class EditionSerializer(ModelSerializer):
    class Meta:
        model = Edition
        fields = "__all__"

class SurahMiniSerializer(ModelSerializer):
    class Meta:
        model = Surah
        fields = ['number', 'english_name', 'english_name_translation']

class AyahSerializer(ModelSerializer):
    surah = SurahMiniSerializer()
    class Meta:
        model = Ayah
        fields = [
            "number","text","number_in_surah","juz","manzil","page",
            "ruku","hizb_quarter","sajda","audio","audio_secondary",
            "edition",'surah'
        ]

class SurahSerializer(ModelSerializer):
    ayahs = AyahSerializer(many=True, read_only=True)
    class Meta:
        model = Surah
        fields = ['number','name','english_name','english_name_translation','revelation_type','numberOfAyahs','ayahs']

class JuzSerializer(ModelSerializer):
    ayahs = AyahSerializer(many=True)
    surahs = SurahSerializer(many=True)
    edition = EditionSerializer()
    class Meta:
        model = Juz
        fields = "__all__"