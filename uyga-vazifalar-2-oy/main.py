"""
Turdaliyev Xazratbek N-77 guruh 2-oy imtihoni yechimi
"""

#  1.“Tibbiy Qabul Tizimi” (Medical Appointment System)
# Maqsad:
# Bemorlar shifokorlarga onlayn tarzda navbat olishadi, shifokorlar esa o‘z jadvalini boshqarishadi.
# Sinflar:
# 1. Doctor
# Atributlar:
# name: str — shifokor ismi
# specialty: str — mutaxassisligi (masalan, “Tish shifokori”, “Kardiolog”)
# Metodlar:
# info() — shifokor haqida ma’lumot.
# 2. Patient
# Atributlar:
# name: str
# age: int
# Metodlar:
# info() — bemor haqida ma’lumot.
# 3. Hospital
# Atributlar:
# name: str
# doctors: list — tizimdagi barcha shifokorlar
# patients: list — tizimdagi bemorlar
# records: dict — {bemor_ismi: [(shifokor, vaqt)]} ko‘rinishida bandliklar
# Metodlar:
# add_doctor(doctor) — yangi shifokor qo‘shadi
# add_patient(patient) — yangi bemorni ro‘yxatga oladi
# add_record(patient, doctor, time) — bemorni tanlangan vaqtda shifokorga yozadi
# cancel(patient, doctor, time) — bandlikni bekor qiladi
# get_doctor_schedule(doctor) — shifokorning bo‘sh vaqtlarini ko‘rsatadi
# get_patient_appointments(patient) — bemorning band uchrashuvlarini chiqaradi
#  Ishlash mantig‘i:
# Shifokor tizimga kiradi.
# Bemor tizimga kiradi va kerakli shifokorni tanlaydi.
# U o‘ziga qulay vaqtni tanlab qabulga yoziladi agar shu vaqtda boshqa bemor yozilgan bo’lsa bu haqida malumot berishi kerak va boshqa vaqt tanlashi kerak
# Agar kerak bo‘lsa, uchrashuvni bekor qilishi ham mumkin.
# Qo’shimcha funksiya:
# 1.search_by_specialty("Nevrolog") bilan foydalanuvchi kerakli mutaxassisni topsin.
# 2.Tizimga rating funksiyasi qo‘shib, bemorlar shifokorga baho bera olsin

from uuid import uuid4
from datetime import datetime
from enum import Enum
import sys
import time

def loading_animation(kutish_matni):
    animation = "|/-\\"
    for i in range(30):
        sys.stdout.write('\r' + animation[i % len(animation)] + f"{kutish_matni}...")
        sys.stdout.flush()
        time.sleep(0.1)

class Adress:
    def __init__(self, viloyat: str, tuman: str, shahar_or_qishloq: str, uy_raqami: int):
        self.viloyat = viloyat
        self.tuman = tuman
        self.shahar_or_qishloq = shahar_or_qishloq
        self.uy_raqami = uy_raqami

    def __str__(self):
        return f"{self.viloyat.title()}-viloyati, {self.tuman.title()}-tumani, {self.shahar_or_qishloq.capitalize()}, uy raqami: {self.uy_raqami}"

class DoctorSohalari(Enum):
    NEVROLOG = "nevrolog"
    TISH_DOKTORI = "tish doktori"
    FIZIOLOG = "fiziolog"
    LOR = "lor"
    PEDIATR = "pediatr"

class DoctorRatings(Enum):
    ALO = 5
    YAXSHI = 4
    QONIQARLI = 3
    QONIQARSIZ = 2
    YOMON = 1

class Doctor:
    def __init__(self,name: str,familiya: str, sohasi: DoctorSohalari, tajribasi_yil: int, telefon_raqami: int ,yashash_manzili: Adress):
        self.id = uuid4()
        self.name = name
        self.familiya = familiya
        self.sohasi = sohasi
        self.tajribasi_yil = tajribasi_yil
        self.tel_raqam = telefon_raqami
        self.yashash_manzili = yashash_manzili

    def __str__(self):
        return f"Doktor: {self.name.title()} {self.familiya.title()} - Sohasi: {self.sohasi.value.title()} | Bog'lanish uchun: {self.tel_raqam} | {self.tajribasi_yil}-yillik tajribaga ega"

    def get_doctor_adress(self):
        return f"Doktor {self.name.title()}-ning yashash manzili: {self.yashash_manzili}"

    def get_doctor_id(self):
        return self.id

    def get_doctor_name(self):
        return self.name

    def doctor_info(self):
        return f"Doktor: {self.name} | Sohasi: {self.sohasi.value.title()}"

class Bemor:
    def __init__(self,name: str, familiyasi: str, age: int, yashash_manzili: Adress):
        self.id = uuid4()
        self.ism = name
        self.familiyasi = familiyasi
        self.age = age
        self.yashash_manzili = yashash_manzili

    def bemor_info(self):
        return f"ID: {self.id} | Bemor ismi: {self.ism} - {self.familiyasi} | Yoshi: {self.age} | Yashash manzili: {self.yashash_manzili}"

class RecordStatus(Enum):
    BAND_QILINGAN = "band qilingan"
    KUTMOQDA = "kutmoqda"
    SUCCESS = "qabul tugagan"
    BEKOR_QILINGAN = "bekor qilingan"

class Kasalxona:
    def __init__(self, name, kasalxona_manzili: Adress):
        self.name = name
        self.kasalxona_manzili = kasalxona_manzili
        self.doctorlar = {}
        self.bemorlar = {}
        self.records = {}

    @staticmethod
    def generate_record_id():
        return uuid4()

    def add_doctor(self,doctor: Doctor):
        if doctor.id in self.doctorlar.keys():
            raise ValueError(f"ID: {doctor.id} | Doktor ismi: {doctor.get_doctor_name()} doktor kasalxonada allaqachon ro'yxatdan o'tgan!")
        else:
            self.doctorlar[doctor.id] = {
            "doctor": doctor,
            "rating": None,
            "baholangan": 0
        }

    def add_patient(self,bemor: Bemor):
        if bemor.id in self.bemorlar.keys():
            raise ValueError(f"Bunday ID lik bemor tizimda allaqachon mavjud!")
        else:
            self.bemorlar[bemor.id] = bemor

    def add_record(self, bemor: Bemor, doctor: Doctor, from_time: datetime, until: datetime):
        record_id = self.generate_record_id()
        self.records[record_id] = {"bemor": bemor, "doctor": doctor, "from_time": from_time, "until": until, "record_status": RecordStatus.BAND_QILINGAN}

    def doktorni_bahola(self,doctor: Doctor, baho: DoctorRatings):
        self.doctorlar[doctor.id]['rating'] = baho
        self.doctorlar[doctor.id]['baholangan'] += 1
        return True

    def cancel_record(self,record_id):
        for record in self.records.keys():
            if record_id == record:
                self.records[record_id]['record_status'] = RecordStatus.BEKOR_QILINGAN

    def get_doctor_schedule(self, doctor: Doctor):
        doctor_records = []
        for record_id, record_data in self.records.items():

            if (record_data['doctor'].id == doctor.id and
                record_data['record_status'] != RecordStatus.BEKOR_QILINGAN and
                record_data['record_status'] != RecordStatus.SUCCESS):
                doctor_records.append({
                    'record_id': record_id,
                    'bemor': record_data['bemor'],
                    'from_time': record_data['from_time'],
                    'until': record_data['until'],
                    'status': record_data['record_status']
                })

        doctor_records.sort(key=lambda x: x['from_time'])

        if not doctor_records:
            print("Doktor hozircha to'liq bo'sh. Hech qanday band qilingan vaqt yo'q!\n")
            return []

        return doctor_records

    def get_patient_appointments(self, bemor: Bemor):
        bemor_records = []
        for record_id, record_data in self.records.items():
            if record_data['bemor'].id == bemor.id:
                bemor_records.append({
                    'record_id': record_id,
                    'doctor': record_data['doctor'],
                    'from_time': record_data['from_time'],
                    'until': record_data['until'],
                    'status': record_data['record_status']
                })

        bemor_records.sort(key=lambda x: x['from_time'])

        if not bemor_records:
            print("Hech qanday uchrashuv topilmadi!\n")
            return []

        return bemor_records

    def get_doctor_by_profession(self, sohasi: DoctorSohalari):
        data = []
        for key in self.doctorlar.keys():
            if sohasi == self.doctorlar[key]['doctor'].sohasi:
                data.append(self.doctorlar[key]['doctor'])

        return data

adress_1 = Adress("Andijon","Izboskan","Yangi qishloq qishlog'i",13)
adress_2 = Adress("Andijon","Paxtaobod","Nimadir Shahar",13)
bemor_xazratbek = Bemor("Xazratbek","Turdaliyev",22,adress_1)
bemor_hasan = Bemor("Hasan","Husanov",18,adress_2)
doktor_1 = Doctor("Abdullajon","Shakar",DoctorSohalari.NEVROLOG,7,998939498849,adress_2)
doktor_2 = Doctor("Ali","Valiyev",DoctorSohalari.FIZIOLOG,2,998939498888,adress_1)
kasalxona_1 = Kasalxona("Xazratbek shifoxonasi",adress_2)

print(adress_1)
print(adress_2)
print(bemor_xazratbek.bemor_info())
print(doktor_1.doctor_info())
kasalxona_1.add_doctor(doktor_1)
kasalxona_1.add_doctor(doktor_2)
kasalxona_1.add_patient(bemor_xazratbek)
kasalxona_1.add_patient(bemor_hasan)
kasalxona_1.add_record(bemor_xazratbek,doktor_1,datetime.now(),datetime(2026,1,30,10,14))
kasalxona_1.add_record(bemor_hasan,doktor_2,datetime.now(),datetime(2026,2,12,10,14))

# print(kasalxona_1.records)
# print(kasalxona_1.doctorlar)
# print(kasalxona_1.bemorlar)
bemorning_band_uchrashuvlari = kasalxona_1.get_patient_appointments(bemor_xazratbek)
doktorning_band_vaqtlari = kasalxona_1.get_doctor_schedule(doktor_1)

print(f"{bemor_xazratbek.ism}-ning band uchrashuvlari\n\n")
for i in range(len(bemorning_band_uchrashuvlari)):
    print(f"Record ID: {bemorning_band_uchrashuvlari[i]['record_id']}\nDoctor: {bemorning_band_uchrashuvlari[i]['doctor']}\nShu vaqtdan: {bemorning_band_uchrashuvlari[i]['from_time']}\nShu vaqtgacha: {bemorning_band_uchrashuvlari[i]['until']}\nXolati: {bemorning_band_uchrashuvlari[i]['status'].value}\n")


print("Doktorning bo'sh vaqtlari: \n")
for i in range(len(doktorning_band_vaqtlari)):
    print(f"Record ID: {doktorning_band_vaqtlari[i]['record_id']}\nBemor: {doktorning_band_vaqtlari[i]['bemor'].bemor_info()}\nShu vaqtdan: {doktorning_band_vaqtlari[i]['from_time']}\nShu vaqtgacha: {doktorning_band_vaqtlari[i]['until']}\nXolati: {doktorning_band_vaqtlari[i]['status'].value}\n")

kasalxona_1.get_doctor_by_profession(DoctorSohalari.NEVROLOG)


# ----------------------
print("\n\nIkkinchi xolat: ")
bemorning_band_uchrashuvlari = kasalxona_1.get_patient_appointments(bemor_hasan)
doktorning_band_vaqtlari = kasalxona_1.get_doctor_schedule(doktor_2)


for i in range(len(bemorning_band_uchrashuvlari)):
    print(f"Record ID: {bemorning_band_uchrashuvlari[i]['record_id']}\nDoctor: {bemorning_band_uchrashuvlari[i]['doctor']}\nShu vaqtdan: {bemorning_band_uchrashuvlari[i]['from_time']}\nShu vaqtgacha: {bemorning_band_uchrashuvlari[i]['until']}\nXolati: {bemorning_band_uchrashuvlari[i]['status'].value}\n")

for i in range(len(doktorning_band_vaqtlari)):
    print(f"Record ID: {doktorning_band_vaqtlari[i]['record_id']}\nBemor: {doktorning_band_vaqtlari[i]['bemor'].bemor_info()}\nShu vaqtdan: {doktorning_band_vaqtlari[i]['from_time']}\nShu vaqtgacha: {doktorning_band_vaqtlari[i]['until']}\nXolati: {doktorning_band_vaqtlari[i]['status'].value}\n")

for data in kasalxona_1.get_doctor_by_profession(DoctorSohalari.NEVROLOG):
    print(data.doctor_info())