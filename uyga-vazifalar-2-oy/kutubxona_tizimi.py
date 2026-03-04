from datetime import datetime, timedelta
from uuid import uuid4


def generate_id():
    """
    Unikal ID yaratish uchun yordamchi funksiya
    """
    return str(uuid4().hex[:10])


class Kitobxon:
    def __init__(self,ism,kitobxon_turi,kutubxonachi_idsi,details=None, telefon_raqam=None,address=None):
        self.id = generate_id()
        self.ism = ism
        self.kitobxon_turi = kitobxon_turi  # o'quvchi, o'qituvchi yoki booshqa kitobxon
        self.kutubxonachi_id = kutubxonachi_idsi
        self.details = details  # Agar o'quvchi bo'lsa sinf+sinf_harfi masalan 9-A, agar o'qituvchi bo'lsa o'qituvchi fani Matematika
        self.telefon_raqam = telefon_raqam
        self.address = address
        self.created_at = datetime.now()

    def __str__(self):
        return f"Kitobxon ma'lumotlari\nID: {self.id}\nIsm: {self.ism}\nTuri: {self.kitobxon_turi}\nDetails: {self.details}\nTelefon raqam: {self.telefon_raqam}\nAdress: {self.address}"

    def get_name(self):
        return self.ism

    def get_reader_type(self):
        return self.kitobxon_turi.lower()

    def get_phone_number(self):
        if self.telefon_raqam is not None:
            return self.telefon_raqam
        return f"{self.ism}-ning telefon raqamlari mavjud emas"

    def get_adress(self):
        if self.address is not None:
            return self.address

        else:
            return (
                f"{self.ism}-kitobxonning yashash manzili haqida ma'lumot mavjud emas"
            )

    def get_reader_id(self):
        return self.id

    def get_reader_librarian_id(self):
        """Kitobxonga bog'langan kutubxonachi idsini qaytaradi"""
        return self.kutubxonachi_id

    def get_details(self):
        if self.details is not None:
            return self.details
        else:
            return f"{self.ism}-kitobxonning detail ma'lumotlari mavjud emas!"

    def get_creation_date(self):
        return self.created_at

    def get_info(self):
        """Kitobxon haqida to'liq ma'lumot qaytaradi."""
        return {
            "ID": self.id,
            "Ism": self.ism,
            "Turi": self.kitobxon_turi,
            "Sinf/Fan": self.details,
            "Telefon": self.telefon_raqam,
            "Manzil": self.address,
            "Qo'shilgan sana": self.created_at.strftime("%Y-%m-%d"),
            "Kutubxonachi ID": self.kutubxonachi_id,
        }

    def change_phone_number(self, phone_number):
        if phone_number != self.get_phone_number():
            self.telefon_raqam = phone_number
        else:
            return "Iltimos yangi telefon raqam kiriting"

        return f"Kitobxon: {self.ism} telefon raqami {phone_number}-ga o'zgartirildi."

    def change_adress(self, new_adress):
        self.address = new_adress

        return f"Kitobxon: {self.ism} yashash manzili {new_adress}-ga o'zgartirildi: "


class Transaction:
    def __init__(self, kitobxon, book_title, inventar_raqami, return_days=15):
        self.id = generate_id()
        self.kitobxon_id = kitobxon.id
        self.kitobxon_ismi = kitobxon.ism
        self.book_title = book_title
        self.inventar_raqami = inventar_raqami
        self.issue_date = datetime.now()  # kitob berilgan sana va vaqt
        self.qaytarish_sanasi = self.issue_date + timedelta(
            days=return_days
        )  # bu xususiyat kitobxon kitobni o'zi qaysa sanagacha qaytarishi kerakligini ko'rsatadi
        self.is_returned = False
        self.qaytarilgan_sana = None  # bu kitobxon kitobni aynan qaysi sanada qaytarganini yozadi avtomatik.

    def get_transaction_id(self):
        return self.id

    def get_kitobxon_id(self):
        return self.kitobxon_id

    @property
    def check_muddat(self):
        """Kitobning qaytarish muddati o'tganligini tekshiradi."""
        return not self.is_returned and datetime.now() > self.qaytarish_sanasi

    def __str__(self):
        status = "Qaytarilgan" if self.is_returned else "Qaytarilmagan"
        if self.check_muddat:
            status = "Muddati o'tgan"
        return (
            f"Tranzaksiya ID: {self.id}\n"
            f"  Kitobxon: {self.kitobxon_id}\n"
            f'  Kitob: "{self.book_title}" (Inv: {self.inventar_raqami})\n'
            f"  Berilgan sana: {self.issue_date.strftime('%Y-%m-%d')}\n"
            f"  Qaytarish sanasi: {self.return_date.strftime('%Y-%m-%d')}\n"
            f"  Holati: {status}\n"
        )

    def mark_as_returned(self):
        self.is_returned = True
        self.qaytarish_sanasi = datetime.now()

        return f"{self.book_title} kitobi {self.qaytarish_sanasi}-sanasida {self.kitobxon_ismi}-tomonidan qaytarildi!"


class Kutubxonachi:
    def __init__(self, uid, ism, school):
        self.uid = uid
        self.ism = ism
        self.school = school
        self.readers = []
        self.transactions = []
        print(f"Kutubxonachi '{ism}' ({school}) tizimga qo'shildi.")

    def get_librarian_id(self):
        return self.uid

    def get_name(self):
        return self.ism

    def add_reader(
        self,
        ism,
        kitobxon_turi,
        details=None,
        telefon_raqam=None,
        address=None,
    ):
        new_reader = Kitobxon(
            ism, kitobxon_turi, self.uid, details, telefon_raqam, address
        )
        self.readers.append(new_reader)
        print(f"Yangi kitobxon qo'shildi: {ism}")
        return new_reader

    def check_qaytarilmagan_kitob(self, reader):
        for transaction in self.transactions:
            if transaction.kitobxon_id == reader.id and not transaction.is_returned:
                return transaction

        return None

    def kitob_ber(self, reader, book_title, inventar_raqam, return_days=15):
        self.transactions.append(
            Transaction(reader, book_title, inventar_raqam, return_days)
        )
        qaytarilmagan_kitob = self.check_qaytarilmagan_kitob(reader)

        if qaytarilmagan_kitob:
            print(
                f"Xatolik! {reader.get_name()}-da qaytarilmagan kitob bor: {book_title}"
            )
            return None

        new_transaction = Transaction(reader, book_title, inventar_raqam, return_days)
        self.transactions.append(new_transaction)
        print(f"Kitob: {book_title} {reader.get_name()}-ga berildi")

        return new_transaction

    def return_book(self, transaction):
        transaction.mark_as_returned()

    def get_dashboard_status(self):
        data = {
            "total_students": [
                student.get_name()
                for student in self.readers
                if student.get_reader_type() == "student"
            ],
            "total_teachers": [
                teacher.get_name()
                for teacher in self.readers
                if teacher.get_reader_type() == "teacher"
            ],
            "other_readers": [
                other for other in self.readers if other.get_reader_type() == "other "
            ],
            "qaytarilmagan_kitoblar": len(
                [
                    transaction
                    for transaction in self.transactions
                    if not transaction.is_returned
                ]
            ),
            "muddati_otgan_kitoblar": len(
                [book for book in self.transactions if book.check_muddat]
            ),
        }
        return data

class LibrarySystem:
    """Butun kutubxona tizimini boshqaruvi uchun markaziy class (admin panel) desa ham bo'ladi"""

    def __init__(self, name="ElektronFormular Markaziy Tizimi"):
        self.name = name
        self.librarians = []
        self.kutubxona_loglari = []
        print(f"'{self.name}' ishga tushirildi!")

    def _log_action(self, bajaruvchi, harakat, details=""):
        log_data = f"[{datetime.now().strftime("%Y-%m-%d %H:%M")}] | Bajaruvchi: {bajaruvchi} | Harakat: {harakat} | Tafsilotlar: {details}"
        self.kutubxona_loglari.append(log_data)

    def add_librarian(self, ism, school):
        uid = generate_id()
        new_librarian = Kutubxonachi(uid, ism, school)
        self.librarians.append(new_librarian)
        self._log_action(
            "Admin",
            "Yangi kutubxonachi qo'shish",
            f"{school}-maktabidan yangi {ism}-kutubxonachisi tizimga kirgazildi",
        )

        return new_librarian

    def get_librarian_by_id(self, uid):
        for librarian in self.librarians:
            if librarian.get_librarian_id() == uid:
                return librarian

        return None

    def get_global_statistics(self):
        total_readers = sum(len(librarian.readers) for librarian in self.librarians)
        total_transactions = sum(
            len(librarian.transactions) for librarian in self.librarians
        )
        total_schools = len(set(librarian.school for librarian in self.librarians))
        return {
            "Jami kutubxonachilar": len(self.librarians),
            "Jami kitobxonlar": total_readers,
            "Jami tranzaksiyalar": total_transactions,
            "Jami maktablar": total_schools,
        }

    def print_kutubxona_loglari(self):
        if not self.kutubxona_loglari:
            return "Loglar jurani bo'sh"
        for log in self.kutubxona_loglari:
            print(log)

        print("--------------------------------\n")


def run_demo():
    system = LibrarySystem()  # Admin panelni ishga tushuramiz

    # kutubxonachilarni ro'yxatdan o'tkazamiz

    kutubxonachi1 = system.add_librarian("Ali", "15-Maktab")
    kutubxonachi2 = system.add_librarian("Vali", "15-DIMI")
    print(f"Kutubxonachi: {kutubxonachi1.get_name()} o'z faoliyatini boshladi")
    student1 = kutubxonachi1.add_reader(
            "Xazratbek",
            "student",
            "11-A",
            "+998939498849",
            "Andijon viloyati Izboskan tumani",
        )

    other1 = kutubxonachi2.add_reader(
            "Hasan",
            "other",
            "boshqa kitobxon",
            "+998939498840",
            "Andijon viloyati Buloqboshi tumani",
        )

    student2 = kutubxonachi1.add_reader(
            "Husan",
            "student",
            "11-B",
            "+998939498849",
            "Andijon viloyati Izboskan tumani",
        )

    teacher1 = kutubxonachi2.add_reader(
        "Abdulloh",
        "teacher",
        "Matematika o'qituvchisi",
        "+998939498841",
        "Andijon viloyati",
    )

    # Kitob berish jarayoni
    transcaction1 = Transaction(student1, "Ufq romani", "INV001", return_days=5)

    transaction2 = Transaction(student2, "Ufq romani", "INV002", return_days=10)
    transaction3 = kutubxonachi1.kitob_ber(
        student1, "Ufq romani", "INV003", return_days=-1
    )
    transaction4 = kutubxonachi2.kitob_ber(
        teacher1, "Ufq romani", "INV003", return_days=10
    )

    if transcaction1:
        kutubxonachi1.check_qaytarilmagan_kitob(student1)

    if transaction2:
        kutubxonachi1.check_qaytarilmagan_kitob(teacher1)

    if transaction3:
        kutubxonachi2.check_qaytarilmagan_kitob(other1)

    if transaction4:
        kutubxonachi2.check_qaytarilmagan_kitob(teacher1)

    print("Kutubxona dashboard statistika")
    stats_kutubxonachi1 = kutubxonachi1.get_dashboard_status()
    print(f"Kutubxonachi statistikasi: {kutubxonachi1.get_name()}")
    for key, value in stats_kutubxonachi1.items():
        print(f"{key.replace("_"," ").title()}: {value}")

    stats_kutubxonachi2 = kutubxonachi2.get_dashboard_status()
    print(f"Kutubxonachi statistikasi: {kutubxonachi2.get_name()}")

    for key, value in stats_kutubxonachi2.items():
        print(f"{key.replace("_"," ").title()}: {value}")

    # 7. Admin tizimning umumiy statistikasini ko'radi
    print("\n---Admin Paneli: Umumiy Statistika ---")
    global_stats = system.get_global_statistics()
    for key, value in global_stats.items():
        print(f"{key}: {value}")

    # 8. Admin operatsiyalar jurnalini ko'radi
    system.print_kutubxona_loglari()


if __name__ == "__main__":
    run_demo()
