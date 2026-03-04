import psycopg2
from prettytable import PrettyTable
import getpass
import bcrypt
from datetime import datetime

from prettytable import PrettyTable
table = PrettyTable()

dori_turlari = ["tabletka","kapsula","sirop","sprey","gel"]
xodim_roles = ["Farmatsevt","Kassir","Menejer","Omborchi"]

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

class DorixonaTizimi:
    def __init__(self, database: Database, name: str):
        self.database = database
        self.name = name
        self.conn = psycopg2.connect(**database.get_db())
        self.cur = self.conn.cursor()

    def __str__(self):
        return f"{self.name.title()}-tizimiga xush kelibsiz"

    def add_dorixona(self, dorixona_nomi: str, address: str, aloqa_raqami: str, description: str, login: str, password_hash: str) -> bool:
        try:
            self.cur.execute("""
                INSERT INTO dorixonalar
                (name, address, aloqa_raqami, description, login, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (dorixona_nomi, address, aloqa_raqami,
                description, login, password_hash))

            self.conn.commit()

            return True

        except Exception as e:
            print(e)
            self.conn.rollback()
            return False


    def check_login(self, login: str, password: str) -> bool:
        self.cur.execute(
            "SELECT password_hash FROM dorixonalar WHERE login=%s",
            (login,)
        )
        row = self.cur.fetchone()

        if not row:
            return False

        stored_hash = row[0]

        return bcrypt.checkpw(
            password.encode(),
            stored_hash.encode()
        )


    def get_categories(self):
        self.cur.execute("SELECT * FROM categories")
        data = self.cur.fetchall()
        return data


    def get_dorixona_id_by_login(self, login: str) -> int | None:
        self.cur.execute("SELECT id FROM dorixonalar WHERE login=%s;", (login,))
        row = self.cur.fetchone()
        return row[0] if row else None


    def add_dori(self, dorixona_id: int):
        if dorixona_id is None:
            print("Dorixona ID yo'q. Avval tizimga kiring.")
            return

        cats = self.get_categories()
        print("-" * 60)
        for cid, cname, desc in cats:
            print(f"{cid:>2} | {cname:<20} | {desc}")

        cat_ids = {c[0] for c in cats}
        while True:
            kategoriya_id = input("Kategoriya ID: ").strip()
            if kategoriya_id.isdigit() and int(kategoriya_id) in cat_ids:
                kategoriya_id = int(kategoriya_id)
                break
            print("Noto'g'ri kategoriya ID.")

        name = input_nonempty("Dori nomi: ")
        ishlab_chiqarilgan_davlat = input("Ishlab chiqarilgan davlat (bo'sh bo'lishi mumkin): ").strip() or None
        doza = input("Doza (masalan 500mg) (bo'sh bo'lishi mumkin): ").strip() or None

        for i, t in enumerate(dori_turlari, 1):
            print(f"{i}) {t}")
        while True:
            dori_turi = input("Dori turini tanlang (1-5): ").strip()
            if dori_turi.isdigit() and 1 <= int(dori_turi) <= len(dori_turlari):
                dori_turi_val = dori_turlari[int(dori_turi) - 1]
                break
            print("Noto'g'ri tanlov.")

        while True:
            narxi = input("Narxi (UZS): ").strip()
            if narxi.isdigit() and int(narxi) > 0:
                narxi = int(narxi)
                break
            print("Narx musbat son bo'lishi kerak.")

        while True:
            qty = input("Miqdor (quantity): ").strip()
            if qty.isdigit() and int(qty) >= 0:
                qty = int(qty)
                break
            print("Miqdor 0 yoki undan katta bo'lishi kerak.")

        try:
            self.cur.execute("""
                INSERT INTO dorilar
                (dorixona_id, category_id, name, ishlab_chiqarilgan_davlat, doza, dori_turi, narxi, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (dorixona_id, kategoriya_id, name, ishlab_chiqarilgan_davlat, doza, dori_turi_val, narxi, qty))

            self.conn.commit()
            print(f"Dori '{name}' muvaffaqiyatli qo'shildi.")

        except Exception as e:
            self.conn.rollback()
            print("Xatolik:", e)

    def get_dori_quantity(self,dorixona_id: int,dori_id: int) -> int:
        self.cur.execute("SELECT quantity FROM dorilar WHERE dorixona_id=%s AND id=%s",(dorixona_id,dori_id,))
        data = self.cur.fetchone()
        return list(data)[0]

    def sotib_olish(self, dorixona_id: int):
        miqdori = int(input("Nechta sotib olasiz: "))
        print(self.get_available_dorilar(dorixona_id))
        dori_id = int(input("Sotib oladigan doringiz idsini tanlang: "))

        if miqdori <= 0:
            return "Miqdor musbat bo'lishi kerak."

        self.cur.execute("""
            UPDATE dorilar SET quantity = quantity - %s WHERE dorixona_id = %s AND id = %s AND quantity >= %s RETURNING quantity;
        """, (miqdori, dorixona_id, dori_id, miqdori))

        row = self.cur.fetchone()
        if not row:
            self.conn.rollback()
            return "Yetarli miqdor yo'q."

        self.conn.commit()
        return f"Xarid uchun rahmat :) Qoldiq: {row[0]}"

    def search_dori(self,dorixona_id: int):
        search_menu = int(input("1.Dori nomi bo'yicha\n2.Kategoriya bo'yicha\n3.Dori turi bo'yicha qidirish\nMenudan birini tanlang: "))
        if search_menu == 1:
            dori_nomi = input_nonempty("Dori nomini kiriting: ")
            self.cur.execute("""SELECT
                dorixonalar.name AS dorixona,
                categories.name AS kategoriya,
                dorilar.id AS ID,
                dorilar.name AS dori,
                dorilar.ishlab_chiqarilgan_davlat,
                dorilar.doza,
                dorilar.dori_turi,
                dorilar.narxi,
                dorilar.quantity AS miqdori
            FROM dorilar
            JOIN dorixonalar ON dorilar.dorixona_id = dorixonalar.id
            JOIN categories  ON dorilar.category_id  = categories.category_id
            WHERE dorilar.dorixona_id = %s AND dorilar.name ILIKE %s ORDER BY dorilar.name;""",(dorixona_id,dori_nomi))
            dorilar = self.cur.fetchall()

            table = PrettyTable()
            table.field_names = [d.name for d in self.cur.description]

            for r in dorilar:
                table.add_row(r)

            return table

        elif search_menu == 2:
            print(f"Mavjud kategoriyalardan birini tanlang")
            for i, cat in enumerate(self.get_categories(), 1):
                cat, name, description = cat
                print(f"{i}) {name} - {description}")

            category = input_nonempty("Kategoriya nomini tanlang: ")
            self.cur.execute("""SELECT dorixonalar.name AS dorixona,
                categories.name AS kategoriya,
                dorilar.id AS ID,
                dorilar.name AS dori,
                dorilar.ishlab_chiqarilgan_davlat,
                dorilar.doza,
                dorilar.dori_turi,
                dorilar.narxi,
                dorilar.quantity AS miqdori
            FROM dorilar
            JOIN dorixonalar ON dorilar.dorixona_id = dorixonalar.id
            JOIN categories  ON dorilar.category_id  = categories.category_id
            WHERE dorilar.dorixona_id = %s AND categories.category_id=%s ORDER BY dorilar.name;""",(dorixona_id,int(category)))
            category_dorilar = self.cur.fetchall()
            table = PrettyTable()
            table.field_names = [d.name for d in self.cur.description]

            for r in category_dorilar:
                table.add_row(r)

            return table

        elif search_menu == 3:
            for i, t in enumerate(dori_turlari, 1):
                        print(f"{i}) {t}")
            dori_type = int(input("Dori turlaridan birini tanlang: "))
            self.cur.execute("""SELECT dorixonalar.name AS dorixona,
                            categories.name AS kategoriya,
                            dorilar.id AS ID,
                            dorilar.name AS dori,
                            dorilar.ishlab_chiqarilgan_davlat,
                            dorilar.doza,
                            dorilar.dori_turi,
                            dorilar.narxi,
                            dorilar.quantity AS miqdori
                        FROM dorilar
                        JOIN dorixonalar ON dorilar.dorixona_id = dorixonalar.id
                        JOIN categories  ON dorilar.category_id  = categories.category_id
                        WHERE dorilar.dorixona_id = %s AND dorilar.dori_turi ILIKE %s ORDER BY dorilar.name;""",(dorixona_id,dori_turlari[dori_type]))

            dori_type_dorilar = self.cur.fetchall()
            table = PrettyTable()
            table.field_names = [d.name for d in self.cur.description]

            for r in dori_type_dorilar:
                table.add_row(r)

            return table


    def get_available_dorilar(self, dorixona_id: int):
        self.cur.execute("""
            SELECT
                dorixonalar.name AS dorixona,
                categories.name AS kategoriya,
                dorilar.id AS ID,
                dorilar.name AS dori,
                dorilar.ishlab_chiqarilgan_davlat,
                dorilar.doza,
                dorilar.dori_turi,
                dorilar.narxi,
                dorilar.quantity AS miqdori
            FROM dorilar
            JOIN dorixonalar ON dorilar.dorixona_id = dorixonalar.id
            JOIN categories  ON dorilar.category_id  = categories.category_id
            WHERE dorilar.dorixona_id = %s
            ORDER BY dorilar.name;
        """, (dorixona_id,))

        dorilar = self.cur.fetchall()

        table = PrettyTable()
        table.field_names = [d.name for d in self.cur.description]

        for r in dorilar:
            table.add_row(r)

        return table

    def get_xodimlar(self,dorixona_id):
        self.cur.execute("SELECT * FROM xodimlar WHERE dorixona_id=%s",(dorixona_id,))
        xodimlar = self.cur.fetchall()
        table = PrettyTable()
        table.field_names = [d.name for d in self.cur.description]

        for r in xodimlar:
            table.add_row(r)

        return table

    def delete_xodimlar(self,dorixona_id):
        xodimlar = self.get_xodimlar()
        xodim_id = int(input(f"Xodimlar: \n{xodimlar}\nXodim idsini kiriting: "))
        self.cur.execute("DELETE FROM xodimlar WHERE dorixona_id=%s AND id=%s",(dorixona_id,xodim_id,))
        self.conn.commit()
        return f"{xodim_id}-lik xodim muvaffaqiyatli o'chirildi"

    def add_xodimlar(self,dorixona_id):
        full_name = input_nonempty("Xodim to'liq ismini kiriting: ")
        for i, t in enumerate(xodim_roles,1):
            print(f"{i}. {t}")
        role = input_nonempty("Xodim rolini tanlang: ")
        phone = input_nonempty("Xodim telefon raqamini kiriting: ")
        oylik = input_nonempty("Xodim oyligini kiriting: ")
        hired_at = datetime.now()

        self.cur.execute("INSERT INTO xodimlar(dorixona_id,full_name,role,phone,salary_uzs,hired_at) VALUES(%s,%s,%s,%s,%s,%s)",(dorixona_id,full_name,xodim_roles[int(role)],phone,oylik,hired_at))
        self.conn.commit()

        return f"Xodim: {full_name} muvaffaqiyatli qo'shildi"



    def get_tugagan_dorilar(self,dorixona_id: int):
        self.cur.execute("SELECT categories.name AS kategoriya, dorilar.id, dorilar.name, dorilar.dori_turi, dorilar.doza FROM dorilar JOIN categories ON dorilar.category_id=categories.category_id WHERE quantity = 0 AND dorixona_id=%s",(dorixona_id,))

        tugagan_dorilar = self.cur.fetchall()
        table = PrettyTable()
        table.field_names = [d.name for d in self.cur.description]

        for r in tugagan_dorilar:
            table.add_row(r)

        return table

database = Database("dorixona_db","xazratbek","1967","localhost",5432)
dorixona = DorixonaTizimi(database=database,name="AptekaUz")

saqlangan_login = ""
saqlangan_parol = ""
dorixona_id = 0

while True:
    auth_menu = int(input("Assalomu Alaykum apteka.uz tizimiga Xush kelibsiz\n1.Tizimga kirish\n2.Ro'yxatdan o'tish\n0. Dasturni to'xtatish\nMenudan tanlang: "))
    try:
        if auth_menu == 2:
            while True:
                dorixona_nomi = input("Dorixonangiz nomini kiriting: ")
                address = input("Dorixona manzilini kiriting: ")
                aloqa_raqami = input("Aloqa uchun telefon raqamini kiriting: ")
                description = input("Tavsifni kiriting: ")
                login = input("Tizimga kirish uchun loginni kiriting: ")
                parol = getpass.getpass("Parolni kiriting: ")
                hashlangan_parol = hash_password(parol)

                yangi_dorixona = dorixona.add_dorixona(dorixona_nomi,address,aloqa_raqami,description,login,hashlangan_parol)
                print(yangi_dorixona)
                if yangi_dorixona:
                    saqlangan_login = login
                    saqlangan_parol = parol
                    dorixona_id = dorixona.get_dorixona_id_by_login(saqlangan_login)
                    if dorixona_id is None:
                        print("Dorixona topilmadi (login bazada yo'q).")
                        continue
                    print("Tizimda muvaffaqiyatli ro'yxatdan o'tdingiz")
                    break
                else:
                    print("Ma'lumotlarni notog'ri to'ldirdingiz qayta urunib ko'ring")
                    auth_menu = int(auth_menu)
                    continue

        elif auth_menu == 1:
            login = input("Loginni kiriting: ")
            parol = getpass.getpass("Parolni kiriting: ")
            saqlangan_login = login
            saqlangan_parol = parol
            dorixona_id = dorixona.get_dorixona_id_by_login(saqlangan_login)
            if dorixona_id is None:
                print("Dorixona topilmadi (login bazada yo'q).")
                continue

            elif dorixona:
                print("Tizimga muvaffaqiyatli kirdingiz")
                dorixona_id = dorixona.get_dorixona_id_by_login(saqlangan_login)
                break

            else:
                print("Login yoki parol xato qayta urunib ko'ring")
                continue

    except KeyboardInterrupt:
        print("\nDastur to'xtadi foydalanganingiz uchun rahmat :)")
        break

while True:
    try:
        dorixona_tizimi_menu = input("""
        1. Dori qo'shish
        2. Dorilarni qidirish
        3. Mavjud dorilarni ko'rish
        4. Xodim qo'shish
        5. Xodimni o'chirish
        6. Tugagan dorilarni ko'rish
        7. Sotib olish
        8. Xodimlarni ko'rish
        0. Chiqish
        Tanlang: """).strip()

        if not dorixona_tizimi_menu.isdigit():
            print("Son kiriting.")
            continue

        dorixona_tizimi_menu = int(dorixona_tizimi_menu)

        if dorixona_tizimi_menu == 1:
            dorixona.add_dori(dorixona_id)

        elif dorixona_tizimi_menu == 2:
            dorilar = dorixona.search_dori(dorixona_id)
            print(dorilar)

        elif dorixona_tizimi_menu == 3:
            dorilar = dorixona.get_available_dorilar(dorixona_id)
            print(dorilar)

        elif dorixona_tizimi_menu == 4:
            print(dorixona.add_xodimlar(dorixona_id))

        elif dorixona_tizimi_menu == 5:
            print(dorixona.delete_xodimlar(dorixona_id))

        elif dorixona_tizimi_menu == 6:
            tugagan_dorilar = dorixona.get_tugagan_dorilar(dorixona_id)
            print(tugagan_dorilar)

        elif dorixona_tizimi_menu == 7:
            data = dorixona.sotib_olish(dorixona_id)
            print(data)

        elif dorixona_tizimi_menu == 8:
            data = dorixona.get_xodimlar(dorixona_id)
            print(data)

        elif dorixona_tizimi_menu == 0:
            print("Dastur to'xtadi rahmat :)")
            break

    except KeyboardInterrupt:
        print("\nDastur to'xtadi foydalanganingiz uchun rahmat :)")
        break