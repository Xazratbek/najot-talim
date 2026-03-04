import psycopg2
import getpass

conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="magazin",
        user="xazratbek",
        password=1967
)

cur = conn.cursor()
def search_books():
    kitob_nomi = input("Kitob nomini kiriting: ")
    cur.execute("SELECT * FROM books JOIN authors ON books.authord_id=authors.id WHERE books.title=%s",(kitob_nomi))
    data = cur.fetchall()
    return data


def add_izox():

menu = int(input("1.Kitob qidiirsh. 2. Izox qoldirish "))
while True:
    if menu == 1:
        print(search_books())

# def choose(title, items, ortga=True):
#     print("\n" + title)
#     print("-" * len(title))
#     for i, it in enumerate(items, 1):
#         print(f"{i}) {it}")
#     if ortga:
#         print("0) Ortga")

#     while True:
#         x = input("Tanlang: ").strip()
#         if ortga and x == "0":
#             return None
#         if x.isdigit():
#             n = int(x)
#             if 1 <= n <= len(items):
#                 return items[n - 1]
#         print("Noto'g'ri tanlov.")


# def input_nonempty(msg):
#     while True:
#         s = input(msg).strip()
#         if s:
#             return s
#         print("Bo'sh bo'lmasin.")


# def parse_value(s):
#     s = s.strip()
#     if s == "":
#         return ""
#     if s.upper() == "NULL":
#         return None
#     if s.lower() in ("true", "t", "yes", "y", "ha"):
#         return True
#     if s.lower() in ("false", "f", "no", "n", "yoq", "yo'q", "yo‘q"):
#         return False
#     if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
#         return int(s)
#     try:
#         if "." in s or "e" in s.lower():
#             return float(s)
#     except Exception:
#         pass
#     return s


# def get_dbs(conn):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT datname
#             FROM pg_database
#             WHERE datistemplate = false
#             ORDER BY datname
#         """)
#         return [r[0] for r in cur.fetchall()]


# def get_tables(conn):
#     with conn.cursor() as cur:
#         cur.execute
#         cur.execute("""
#             SELECT table_name
#             FROM information_schema.tables
#             WHERE table_schema = 'public'
#               AND table_type = 'BASE TABLE'
#             ORDER BY table_name
#         """)
#         return [r[0] for r in cur.fetchall()]


# def get_cols(conn, table):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT a.attname, format_type(a.atttypid, a.atttypmod)
#             FROM pg_attribute a
#             JOIN pg_class c ON c.oid = a.attrelid
#             JOIN pg_namespace n ON n.oid = c.relnamespace
#             WHERE n.nspname = 'public'
#               AND c.relname = %s
#               AND a.attnum > 0
#               AND NOT a.attisdropped
#             ORDER BY a.attnum
#         """, (table,))
#         return cur.fetchall()


# def get_pk(conn, table):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT kcu.column_name
#             FROM information_schema.table_constraints tc
#             JOIN information_schema.key_column_usage kcu
#               ON tc.constraint_name = kcu.constraint_name
#              AND tc.table_schema = kcu.table_schema
#             WHERE tc.table_schema = 'public'
#               AND tc.table_name = %s
#               AND tc.constraint_type = 'PRIMARY KEY'
#             ORDER BY kcu.ordinal_position
#         """, (table,))
#         return [r[0] for r in cur.fetchall()]


# def show_tables(conn):
#     tables = get_tables(conn)
#     if not tables:
#         print("Table yo'q.")
#         return
#     for t in tables:
#         print("-", t)


# def safe_table(conn):
#     tables = get_tables(conn)
#     t = choose("Table tanlang", tables, ortga=True)
#     return t


# def safe_column(conn, table):
#     cols = get_cols(conn, table)
#     names = [c[0] for c in cols]
#     c = choose("Column tanlang", names, ortga=True)
#     return c


# def select_rows(conn):
#     t = safe_table(conn)
#     if not t:
#         return

#     menu = ["LIMIT bilan ko'rish", "Column bo'yicha filter", "PK bo'yicha topish"]
#     act = choose("SELECT", menu, ortga=True)
#     if not act:
#         return

#     pk = get_pk(conn, t)

#     with conn.cursor() as cur:
#         if act == "LIMIT bilan ko'rish":
#             x = input("LIMIT (default 10): ").strip()
#             limit = int(x) if x.isdigit() else 10
#             q = f"SELECT * FROM public.{t} LIMIT %s"
#             cur.execute(q, (limit,))
#             rows = cur.fetchall()
#             names = [d[0] for d in cur.description]
#             print(names)
#             for r in rows:
#                 print(r)

#         elif act == "Column bo'yicha filter":
#             c = safe_column(conn, t)
#             if not c:
#                 return
#             v = parse_value(input(f"{c} qiymat: "))
#             q = f"SELECT * FROM public.{t} WHERE {c} = %s LIMIT 50"
#             cur.execute(q, (v,))
#             rows = cur.fetchall()
#             names = [d[0] for d in cur.description]
#             print(names)
#             for r in rows:
#                 print(r)

#         elif act == "PK bo'yicha topish":
#             if not pk:
#                 print("PRIMARY KEY yo'q.")
#                 return
#             parts = []
#             params = []
#             for k in pk:
#                 v = parse_value(input(f"{k} (PK) qiymat: "))
#                 parts.append(f"{k} = %s")
#                 params.append(v)
#             where = " AND ".join(parts)
#             q = f"SELECT * FROM public.{t} WHERE {where} LIMIT 1"
#             cur.execute(q, params)
#             row = cur.fetchone()
#             if not row:
#                 print("Topilmadi.")
#                 return
#             names = [d[0] for d in cur.description]
#             print(names)
#             print(row)


# def insert_row(conn):
#     t = safe_table(conn)
#     if not t:
#         return

#     cols = get_cols(conn, t)
#     col_names = [c[0] for c in cols]

#     values = {}
#     i = 0
#     while i < len(col_names):
#         c = col_names[i]
#         s = input(f"{c} (Enter=skip, NULL mumkin): ").strip()
#         if s == "":
#             i += 1
#             continue
#         values[c] = parse_value(s)
#         i += 1

#     if not values:
#         print("Hech narsa kiritilmadi.")
#         return

#     cols_part = ", ".join(values.keys())
#     ph_part = ", ".join(["%s"] * len(values))

#     q = f"INSERT INTO public.{t} ({cols_part}) VALUES ({ph_part}) RETURNING *"

#     try:
#         with conn.cursor() as cur:
#             cur.execute(q, list(values.values()))
#             row = cur.fetchone()
#             names = [d[0] for d in cur.description]

#         conn.commit()
#         print("INSERT OK")
#         print(names)
#         print(row)
#     except Exception as e:
#         conn.rollback()
#         print("INSERT xato:", e)


# def update_row(conn):
#     t = safe_table(conn)
#     if not t:
#         return

#     cols = get_cols(conn, t)
#     col_names = [c[0] for c in cols]
#     pk = get_pk(conn, t)

#     set_col = choose("Qaysi column o'zgaradi?", col_names, ortga=True)
#     if not set_col:
#         return
#     new_val = parse_value(input(f"Yangi qiymat ({set_col}): "))

#     params = [new_val]

#     if pk:
#         parts = []
#         for k in pk:
#             v = parse_value(input(f"{k} (PK) qiymat: "))
#             parts.append(f"{k} = %s")
#             params.append(v)
#         where = " AND ".join(parts)
#     else:
#         fcol = choose("Filter column tanlang", col_names, ortga=True)
#         if not fcol:
#             return
#         fval = parse_value(input(f"{fcol} qiymat: "))
#         where = f"{fcol} = %s"
#         params.append(fval)

#     q = f"UPDATE public.{t} SET {set_col} = %s WHERE {where} RETURNING *"

#     try:
#         with conn.cursor() as cur:
#             cur.execute(q, params)
#             rows = cur.fetchall()
#             names = [d[0] for d in cur.description]
#         if not rows:
#             conn.rollback()
#             print("Hech narsa yangilanmadi.")
#             return
#         conn.commit()
#         print("UPDATE OK", len(rows))
#         print(names)
#         for r in rows[:50]:
#             print(r)
#     except Exception as e:
#         conn.rollback()
#         print("UPDATE xato:", e)


# def delete_row(conn):
#     t = safe_table(conn)
#     if not t:
#         return

#     cols = get_cols(conn, t)
#     col_names = [c[0] for c in cols]
#     pk = get_pk(conn, t)

#     params = []

#     if pk:
#         parts = []
#         for k in pk:
#             v = parse_value(input(f"{k} (PK) qiymat: "))
#             parts.append(f"{k} = %s")
#             params.append(v)
#         where = " AND ".join(parts)
#     else:
#         fcol = choose("Filter column tanlang", col_names, ortga=True)
#         if not fcol:
#             return
#         fval = parse_value(input(f"{fcol} qiymat: "))
#         where = f"{fcol} = %s"
#         params.append(fval)

#     sure = input("DELETE? (ha/yo'q): ").strip().lower()
#     if sure not in ("ha", "y", "yes"):
#         print("Bekor qilindi.")
#         return

#     q = f"DELETE FROM public.{t} WHERE {where} RETURNING *"

#     try:
#         with conn.cursor() as cur:
#             cur.execute(q, params)
#             rows = cur.fetchall()
#             names = [d[0] for d in cur.description]
#         if not rows:
#             conn.rollback()
#             print("Hech narsa o'chmadi.")
#             return
#         conn.commit()
#         print("DELETE OK", len(rows))
#         print(names)
#         for r in rows[:50]:
#             print(r)
#     except Exception as e:
#         conn.rollback()
#         print("DELETE xato:", e)


# def alter_menu(conn):
#     t = safe_table(conn)
#     if not t:
#         return

#     menu = [
#         "Table nomini o'zgartirish",
#         "Column qo'shish",
#         "Column o'chirish",
#         "Column nomini o'zgartirish",
#         "Column type o'zgartirish",
#         "Column default set",
#         "Column default drop",
#         "NOT NULL set",
#         "NOT NULL drop",
#     ]
#     act = choose("ALTER", menu, ortga=True)
#     if not act:
#         return

#     try:
#         with conn.cursor() as cur:
#             if act == "Table nomini o'zgartirish":
#                 new_name = input_nonempty("Yangi table nomi: ")
#                 cur.execute(f"ALTER TABLE public.{t} RENAME TO {new_name}")

#             elif act == "Column qo'shish":
#                 c = input_nonempty("Yangi column nomi: ")
#                 typ = input_nonempty("Type: ")
#                 cur.execute(f"ALTER TABLE public.{t} ADD COLUMN {c} {typ}")

#             elif act == "Column o'chirish":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 cur.execute(f"ALTER TABLE public.{t} DROP COLUMN {c}")

#             elif act == "Column nomini o'zgartirish":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 new_c = input_nonempty("Yangi column nomi: ")
#                 cur.execute(f"ALTER TABLE public.{t} RENAME COLUMN {c} TO {new_c}")

#             elif act == "Column type o'zgartirish":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 new_t = input_nonempty("Yangi type: ")
#                 cur.execute(f"ALTER TABLE public.{t} ALTER COLUMN {c} TYPE {new_t}")

#             elif act == "Column default set":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 expr = input_nonempty("DEFAULT expression: ")
#                 cur.execute(f"ALTER TABLE public.{t} ALTER COLUMN {c} SET DEFAULT {expr}")

#             elif act == "Column default drop":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 cur.execute(f"ALTER TABLE public.{t} ALTER COLUMN {c} DROP DEFAULT")

#             elif act == "NOT NULL set":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 cur.execute(f"ALTER TABLE public.{t} ALTER COLUMN {c} SET NOT NULL")

#             elif act == "NOT NULL drop":
#                 c = safe_column(conn, t)
#                 if not c:
#                     return
#                 cur.execute(f"ALTER TABLE public.{t} ALTER COLUMN {c} DROP NOT NULL")

#         conn.commit()
#         print("OK")
#     except Exception as e:
#         conn.rollback()
#         print("ALTER xato:", e)


# def main():
#     host = input("Host [localhost]: ").strip() or "localhost"
#     port_raw = input("Port [5432]: ").strip()
#     port = int(port_raw) if port_raw.isdigit() else 5432
#     user = input_nonempty("User: ")
#     password = getpass.getpass("Password: ")

#     admin = connect_db("postgres", host, port, user, password)
#     admin.autocommit = True

#     conn = None

#     while True:
#         menu = [
#             "Databaselarni ko'rish",
#             "Database tanlash",
#             "Ulangan database tablelarini ko'rish",
#             "SELECT",
#             "INSERT",
#             "UPDATE",
#             "DELETE",
#             "ALTER",
#             "Chiqish",
#         ]
#         act = choose("Menu", menu, ortga=False)
#         if act == "Chiqish":
#             break

#         if act == "Databaselarni ko'rish":
#             for d in get_dbs(admin):
#                 print("-", d)

#         elif act == "Database tanlash":
#             d = choose("Database tanlang", get_dbs(admin), ortga=True)
#             if not d:
#                 continue
#             if conn:
#                 conn.close()
#             conn = connect_db(d, host, port, user, password)
#             print(f"{d}-databasega ulandingiz")

#         else:
#             if not conn:
#                 print("Avval database tanlang.")
#                 continue

#             if act == "Ulangan database tablelarini ko'rish":
#                 show_tables(conn)
#             elif act == "SELECT":
#                 select_rows(conn)
#             elif act == "INSERT":
#                 insert_row(conn)
#             elif act == "UPDATE":
#                 update_row(conn)
#             elif act == "DELETE":
#                 delete_row(conn)
#             elif act == "ALTER":
#                 alter_menu(conn)

#     if conn:
#         conn.close()
#     admin.close()


# if __name__ == "__main__":
#     main()
