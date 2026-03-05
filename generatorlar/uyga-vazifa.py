
# 1.  Fayldagi satrlarni generator orqali o‘qish data.txt fayli berilgan.
    # Generator yozing, u fayldagi har bir satrni bittadan qaytarsin.

# def read_file_generator(file_path: str):
#     with open(file_path,"r") as file:
#         while True:
#             try:
#                 if data == "":
#                     break
#                 data = file.readline().replace("\n","")
#                 yield data
#             except StopIteration:
#                 break

# data = read_file_generator("data.txt")
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))

# 2.  Fayldagi sonlardan juftlarini qaytarish numbers.txt faylida sonlar
#     yozilgan. Generator yozing, u faqat juft sonlarni qaytarsin.

# def get_juft_sonlar_generator(file_path: str):
#     with open(file_path,"r") as file:
#         while True:
#             try:
#                 data = file.readline().replace("\n","")
#                 if data == "":
#                     break

#                 if int(data) % 2 == 0:
#                     yield data

#             except StopIteration:
#                 break

# data = get_juft_sonlar_generator("numbers.txt")
# for son in data:
#     print(son)

# 3.  Fayldagi uzun satrlarni topish text.txt fayl berilgan. Generator
#     yozing, u 5 ta belgidan uzun satrlarni qaytarsin.

# def get_uzun_satr_generator(file_path: str):
#     with open(file_path,"r") as file:
#         while True:
#             try:
#                 data = file.readline().replace("\n","")
#                 if data == "":
#                     break

#                 if len(data) > 5:
#                     yield data

#             except StopIteration:
#                 break

# data = get_uzun_satr_generator("data.txt")
# for satr in data:
#     print(satr)

# 4.  Fayldagi sonlarning kvadratini qaytarish nums.txt faylida sonlar
#     bor. Generator yozing, u har bir sonning kvadratini qaytarsin.

# def get_sonlar_kvadrati(file_path: str):
#     with open(file_path,"r") as file:
#         while True:
#             try:
#                 data = file.readline().replace("\n","")
#                 if data == "":
#                     break

#                 yield int(data) ** 2

#             except StopIteration:
#                 break

# data = get_sonlar_kvadrati("numbers.txt")
# for son in data:
#     print(son)


# 5.  Fayldagi barcha so‘zlarni generator orqali ajratish words.txt fayl
#     berilgan. Generator yozing, u fayldagi barcha so‘zlarni bittadan
#     qaytarsin.

# Misol: Python juda kuchli til

# Natija: Python juda kuchli til

# def get_barcha_sozlar(file_path: str):
#     with open(file_path,"r") as file:
#         while True:
#             try:
#                 data = file.readline().replace("\n","")
#                 if data == "":
#                     break

#                 if data.isalpha():
#                     yield data

#             except StopIteration:
#                 break

# data = get_barcha_sozlar("data.txt")
# for soz in data:
#     print(soz)

# 6.  Database dan user nomlarini generator orqali olish users jadvali
#     berilgan. id | name 1 | Ali 2 | Vali 3 | Sami

# Generator yozing, u user nomlarini bittadan qaytarsin.

# import psycopg2

# conn = psycopg2.connect(
#         host="localhost",
#         port=5432,
#         dbname="joinuygavazifa",
#         user="xazratbek",
#         password=1967
# )

# cur = conn.cursor()

# def get_user_generator():
#     cur.execute("SELECT full_name FROM customers;")
#     while True:
#         try:
#             users = cur.fetchone()
#             if users == None:
#                 break

#             yield users

#         except StopIteration:
#             break

# users = get_user_generator()
# for user in users:
#     print(user)

# 7.  Database dan narxi katta mahsulotlarni chiqarish products jadvali
#     berilgan.
# id | name | price 1 | olma | 5000 2 | banan | 12000 3 | nok | 8000
# Generator yozing, u narxi 10000 dan katta mahsulotlarni qaytarsin.

# def get_mahsulotlar_by_price(price: int):
#     cur.execute("SELECT * FROM orders JOIN customers on orders.customer_id=customers.id WHERE price >= %s",(price,))
#     while True:
#         try:
#             mahsulot = cur.fetchone()
#             if mahsulot == None:
#                 break

#             yield mahsulot

#         except StopIteration:
#             break

# mahsulotlar = get_mahsulotlar_by_price(10000)
# print(mahsulotlar)
# for mahsulot in mahsulotlar:
#     print(mahsulot)

# 8. Database dan faqat email larni olish users jadvali berilgan.
# id | name | email Generator yozing, u faqat email larni bittadan qaytarsin.

# import psycopg2

# conn = psycopg2.connect(
#         host="localhost",
#         port=5432,
#         dbname="najottalimerp",
#         user="xazratbek",
#         password=1967
# )

# cur = conn.cursor()
# def get_user_email_generator():
#     cur.execute("SELECT email FROM profiles WHERE email IS NOT NULL")
#     while True:
#         try:
#             email = cur.fetchone()
#             if email == None:
#                 break
#             yield email

#         except StopIteration:
#             break

# emails = get_user_email_generator()
# for email in emails:
#     print(email)



# 9.  Database dan eng uzun ismli userni topish Generator yozing, u
#     database dagi userlarni bittadan olib, eng uzun ismni topishga
#     yordam bersin.
# import psycopg2

# conn = psycopg2.connect(
#         host="localhost",
#         port=5432,
#         dbname="najottalimerp",
#         user="xazratbek",
#         password=1967
# )

# cur = conn.cursor()

# def get_long_username():
#     cur.execute("SELECT ism FROM profiles")
#     eng_uzun_ism_length = 0
#     eng_uzun_ism = ""
#     user_names = cur.fetchall()
#     for index, _ in enumerate(user_names):
#         if len(user_names[index][0]) > eng_uzun_ism_length:
#             eng_uzun_ism_length = len(user_names[index][0])
#             eng_uzun_ism = user_names[index][0]

#         else:
#             pass

#     yield eng_uzun_ism, eng_uzun_ism_length

# user_names = get_long_username()
# print(next(user_names))


# 10. Database dan pagination generator products jadvali berilgan.

# Generator yozing, u mahsulotlarni 5 tadan qilib qaytarsin.

# Misol: 1-5 6-10 11-15

# import psycopg2

# conn = psycopg2.connect(
#         host="localhost",
#         port=5432,
#         dbname="joinuygavazifa",
#         user="xazratbek",
#         password=1967
# )

# cur = conn.cursor()

# def get_orders_by_pagination(pagination: int):
#     current_page = 0
#     while True:
#         cur.execute("SELECT * FROM orders LIMIT %s OFFSET %s",(pagination, current_page))
#         orders = cur.fetchall()
#         try:
#             if orders == None:
#                 break

#             yield orders
#             current_page += 5

#         except StopIteration:
#             break

# orders = get_orders_by_pagination(5)
# print(next(orders))
# print(next(orders))
# print(next(orders))