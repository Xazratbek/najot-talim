# TZ-1: KUTUBXONA TIZIMI
# ==============================

# Vazifa:
# Kutubxonadagi kitoblar va foydalanuvchilarni boshqaruvchi dastur yozish.
# Dastur OOP (class va object) asosida yozilishi shart.

# --------------------------------
# 1. Book class
# --------------------------------
# Atributlar:
# - title        : kitob nomi
# - author       : kitob muallifi
# - is_available : kitob mavjudligi (True yoki False)

# Metodlar:
# - borrow()
#   Agar kitob mavjud bo‘lsa, is_available = False qilinsin,
#   aks holda "Kitob hozir mavjud emas" degan xabar chiqsin.

# - return_book()
#   Kitob qaytarilganda is_available = True qilinsin.

# - info()
#   Kitob nomi, muallifi va holatini ekranga chiqarsin.

# --------------------------------
# 2. User class
# --------------------------------
# Atributlar:
# - name            : foydalanuvchi ismi
# - borrowed_books  : olingan kitoblar ro‘yxati (list)

# Metodlar:
# - take_book(book)
#   Agar book mavjud bo‘lsa:
#     - foydalanuvchi ro‘yxatiga qo‘shilsin
#     - book.borrow() chaqirilsin

# - return_book(book)
#   Agar foydalanuvchi shu kitobni olgan bo‘lsa:
#     - ro‘yxatdan olib tashlansin
#     - book.return_book() chaqirilsin

# - show_books()
#   Foydalanuvchi olgan barcha kitoblarni chiqarib bersin.

# --------------------------------
# Classlar o‘rtasidagi bog‘lanish:
# --------------------------------
# - User class Book obyektlari bilan ishlaydi

from datetime import datetime
from uuid import uuid4


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True
        self.count = 1

    def __str__(self):
        return f"Kitob: {self.title} | Avtor: {self.author}"

    def __eq__(self, boshq_kitob_abyekti):
        if self.count == boshq_kitob_abyekti.count:
            return True
        return False


    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def borrow(self):
        if not self.is_available:
            return "Kitob xozirda mavjud emas"

        self.is_available = False

        return "Kitob muvaffaqiyatli olindi"

    def return_book(self):
        self.is_available = True
        return f"{self.title}-kitobi qaytarildi"

    def info(self):
        status = "Mavjud" if self.is_available else "Berilgan"
        return f"Kitob: {self.title}\nMuallif: {self.author}\nHolati: {status}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def get_user_name(self):
        return self.name

    def take_book(self, book: Book):
        if book in self.borrowed_books:
            return f"Siz allaqachon {book.get_title()} kitobini olgansiz"

        result = book.borrow()
        if book.is_available is False:
            self.borrowed_books.append(book)
        return result

    def show_books(self):
        if not self.borrowed_books:
            return "Sizda olingan kitoblar mavjud emas!"

        return f"Siz olgan kitoblar: {[str(book.get_title()) for book in self.borrowed_books]}"

    def return_book(self, book: Book):
        if book not in self.borrowed_books:
            return f"Siz bu {book.get_title()}-kitobini olmagansiz"

        self.borrowed_books.remove(book)
        return book.return_book()


book1 = Book("Sariq devni minib", "Xudoyberdi To‘xtaboyev")
book2 = Book("Mehrobdan chayon", "Abdulla Qodiriy")
print(book1)
user = User("Xazratbek")

print(user.take_book(book1))
print(user.take_book(book1))  # qayta olishga urinish
print(user.show_books())

print(user.return_book(book1))
print(user.return_book(book1))  # qayta qaytarish
print(user.show_books())
