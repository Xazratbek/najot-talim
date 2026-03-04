# B-Variant
#Drawsqlda arxitektura, pythonda psycopg2 app, create
#Turdaliyev Xazratbek n77 Variant B


import psycopg2
from prettytable import PrettyTable
import getpass
import bcrypt
from datetime import datetime
import random


from prettytable import PrettyTable
table = PrettyTable()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )

def input_nonempty(msg):
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("Bo'sh bo'lmasin.")

def generate_talaba_kodi() -> int:
    return random.randint(1111,99999)

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_db(self):
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
        }

class NajotKutubxona:
    def __init__(self,database: Database, name: str):
        self.name = name
        self.conn = psycopg2.connect(**database.get_db())
        self.cur = self.conn.cursor()

    def __str__(self):
        return f"{self.name}-kutubxonasi"

    def check_user_login(self,email: str,parol: str):
        self.cur.execute("SELECT password FROM users WHERE email=%s",(email))
        row = self.cur.fetchone()
        if not row:
            return False

        stored_hash = row[0]
        return bcrypt.checkpw(parol.encode(),stored_hash.encode())

    def get_user_id_and_role_by_email(self,email: str):
        self.cur.execute("SELECT id, role FROM users WHERE email=%s",(email))
        data = self.cur.fetchone()

        if not data:
            return None
        else:
            return data


    def register_user(self,role: str):
        full_name = input_nonempty("F.I.O-ni kiriting: ")
        email = input_nonempty("Emailni kiriting: ")
        password = getpass.getpass("Parolni kiriting: ")
        hashed_password = hash_password(password)
        self.cur.execute("INSERT INTO users(full_name,email,password,role) VALUES(%s,%s,%s,%s) RETURNING id",(full_name,email,hashed_password,role))
        user_id = self.cur.fetchone()[0]
        self.conn.commit()
        if not user_id:
            return None

        else:
            return user_id

    def register_author(self):
        full_name = input_nonempty("F.I.O-ni kiriting: ")
        country = input("Davlatingizni kiriting (Majburiy emas: Enter skip):") or None
        self.cur.execute("INSERT INTO authors(full_name,country) VALUES(%s,%s) RETURNING id",(full_name,country))
        author_id = self.cur.fetchone()[0]
        self.conn.commit()
        if not author_id:
            return None
        else:
            return author_id

    def get_available_books(self):
        self.cur.execute("SELECT books.id AS kitob_id, books.title, authors.full_name AS avtor_fio, books.description, books.published_year AS chiqarilgan_sana, genres.name AS kitob_janri FROM books JOIN authors ON books.authord_id=authors.id JOIN genres ON books.genre_id=genres.id;")
        available_books = self.cur.fetchall()
        table.clear()
        table.field_names = [col.name for col in self.cur.description]
        table.add_rows(available_books)

        return table

    def search_books(self):
        search_type = int(input("1.Kitob nomi bo'yicha qidirish\n2.Janr bo'yicha qidirish\nTanlang: "))
        if search_type == 1:
            kitob_nomi = input_nonempty("Kitob nomini kiriting: ")
            self.cur.execute("SELECT books.id AS kitob_id,books.title AS kitob_nomi, authors.full_name AS avtor_fio, books.description, books.published_year AS chiqarilgan_sana, genres.name AS kitob_janri FROM books JOIN authors ON books.authord_id=authors.id JOIN genres ON books.genre_id=genres.id WHERE books.title ILIKE %s",(kitob_nomi))
            books = self.cur.fetchall()
            table.clear()
            table.field_names = [col.name for col in self.cur.description]
            table.add_rows(books)
            return table

        elif search_type == 2:
            janr = input_nonempty("Janrni kiriting: ")
            self.cur.execute("SELECT books.id AS kitob_id,books.title AS kitob_nomi, authors.full_name AS avtor_fio, books.description, books.published_year AS chiqarilgan_sana, genres.name AS kitob_janri FROM books JOIN authors ON books.authord_id=authors.id JOIN genres ON books.genre_id=genres.id WHERE genres.name ILIKE %s",(janr))
            books = self.cur.fetchall()
            table.clear()
            table.field_names = [col.name for col in self.cur.description]
            table.add_rows(books)
            return table

    def add_comment(self,user_id: int):
        books = self.get_available_books()
        book_id = int(input(f"Kitobni idsin tanlang:\n{books}"))
        content = input_nonempty("Izoxingizni kiriting: ")
        self.cur.execute("INSERT INTO comments(user_id,book_id,content) VALUES(%s,%s,%s) RETURNING id",(user_id,book_id,content))
        comment_id = self.cur.fetchone()[0]
        self.conn.commit()
        if not comment_id:
            return None
        else:
            return comment_id


    def get_book_detail_info(self):
        books = self.get_available_books()
        book_id = int(input(f"Kitobni idsin tanlang:\n{books}"))
        self.cur.execute("SELECT books.id AS kitob_id,books.title AS kitob_nomi, authors.full_name AS avtor_fio, books.description, books.published_year AS chiqarilgan_sana, genres.name AS kitob_janri FROM books JOIN authors ON books.authord_id=authors.id JOIN genres ON books.genre_id=genres.id WHERE books.id=%s",(book_id))
        book_data = self.cur.fetchall()
        table.clear()
        table.field_names = [col.name for col in self.cur.description]
        table.add_rows(book_data)

        return table

    def get_genres(self):
        self.cur.execute("SELECT * FROM genres")
        genres = self.cur.fetchall()
        table.clear()
        table.field_names = [col.name for col in self.cur.description]
        table.add_rows(genres)

        return table

    def add_book(self,author_id: int):
        janrlar = self.get_genres()
        genre_id = int(input(f"Janr idsini tanlang: {janrlar}"))
        title = input_nonempty("Kitob nomini kiriting: ")
        description = input("Description kiriting: ")
        published_year = input("Kitob chiqgan sanani kiriting (Format: Yil-oy-kun): ")
        self.cur.execute("INSERT INTO books(title,authord_id,description,published_year,genre_id) VALUES(%s,%s,%s,%s,%s) RETURNING id",(title,author_id,description,published_year,genre_id))
        book_id = self.cur.fetchone()[0]
        self.conn.commit()

        if not book_id:
            return None

        else:
            return book_id


    def add_genre(self):
        name = input_nonempty("Janr nomini kiriting: ")
        self.cur.execute("INSERT INTO genres(name) VALUES(%s) RETURNING id",(name))
        genre_id = self.cur.fetchone()[0]
        self.conn.commit()
        if not genre_id:
            return None

        else:
            return genre_id

database = Database("najotkutubxona","xazratbek","1967","localhost",5432)
kutubxona = NajotKutubxona(database,"Najot Kutubxona")

saved_user_id = 0
saved_user_email = ""
user_role = ""
saved_author_id = 0

while True:
    role = int(input("Rolingizni tanlang:\n1.Foydalanuvchi\n2.Author\nTanlang: "))
    login_or_signup = int(input("1.Tizimga kirish\n2.Ro'yxatdan o'tish\nTanlash: "))
    if login_or_signup == 1:
        email = input_nonempty("Emailni kiriting: ")
        parol = getpass.getpass("Parolni kiriting: ")

        if kutubxona.check_user_login(email,parol):
            print("Tizimga muvaffaqiyatli kirdingiz :)")
            user_data = kutubxona.get_user_id_and_role_by_email(email)
            saved_user_id = user_data[0]
            saved_user_email = email
            user_role = user_data[1]
            break

        else:
            print("Notog'ri email yoki parol kiritildi")

    elif login_or_signup == 2 and role == 1:
        user_id = kutubxona.register_user("user" if role == 1 else "author")
        saved_user_id = user_id
        break


    elif login_or_signup == 2 and role == 2:
        author_id = kutubxona.register_author()
        saved_author_id = author_id
        break



while True:
    if user_role == "user":
        user_menu = int(input("1.Kitoblarni ko'rish\n2.Izox qoldirish\n3.Kitob qidirish\n4.Kitob haqida batafsil ma'lumot"))
        if user_menu == 1:
            print(kutubxona.get_available_books())

        elif user_menu == 2:
            print(kutubxona.add_comment(saved_user_id))

        elif user_menu == 3:
            print(kutubxona.search_books())

        elif user_menu == 4:
            print(kutubxona.get_book_detail_info())

        elif user_menu == 0:
            print("Dastur to'xtadi :)")
            break


    elif user_role == "author":
        author_menu = int(input("1.Kitob qo'shish\n2.Janr qo'shish\n0.Chiqish"))
        if author_menu == 1:
            print(kutubxona.add_book(saved_author_id))

        elif author_menu == 2:
            print(kutubxona.add_genre())

        elif author_menu == 0:
            print("Dastur to'xtadi")
            break