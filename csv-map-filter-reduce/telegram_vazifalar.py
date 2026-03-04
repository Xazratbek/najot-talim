# Telegramda berilgan qo'shimcha uyga vazifalar ham ishlandi https://t.me/c/3419657169/1278:

# 1️⃣ Berilgan sonlar ro‘yxatidagi har bir songa 2 qo‘shing.
# 📌 Input: [1, 2, 3, 4]
# 📌 Output: [3, 4, 5, 6]
# Yechim:
# nums = [1, 2, 3, 4]
# data = map(lambda x: x + 2,nums)
# print(list(data))

# 2️⃣ Berilgan sonlar ro‘yxatidan faqat juft sonlarni ajrating.
# 📌 Input: [1, 2, 3, 4, 5, 6]
# 📌 Output: [2, 4, 6]
# Yechim:
# nums = [1, 2, 3, 4, 5, 6]
# juft_sonlar = filter(lambda x: x % 2 == 0, nums)
# print(list(juft_sonlar))

# 3️⃣ Berilgan sonlar ro‘yxatidagi barcha sonlar yig‘indisini toping.
# 📌 Input: [10, 20, 30]
# 📌 Output: 60
# Yechim:
# from functools import reduce

# nums = [10, 20, 30]
# print(sum(nums))
# yigindi = reduce(lambda x, y: x + y, nums)
# print(yigindi)

# 4️⃣ Ismlar ro‘yxatini katta harflarga o‘tkazing.
# 📌 Input: ["ali", "vali", "hasan"]
# 📌 Output: ["ALI", "VALI", "HASAN"]
# Yechim:
# ismlar = ["ali", "vali", "hasan"]
# katta_ismlar = map(lambda ism: ism.upper(), ismlar)
# print(list(katta_ismlar))

# 5️⃣ Ikki ro‘yxat berilgan: ismlar va yoshlar.
# Ularni juftlab chiqaring.
# 📌 Input:
# ["Ali", "Vali"]
# [18, 20]
# 📌 Output: [("Ali", 18), ("Vali", 20)]
# Yechim:
# ismlar = ["Ali", "Vali"]
# yoshlar = [18, 20]
# mixed = zip(ismlar,yoshlar)
# print(list(mixed))

# 6️⃣ Berilgan sonlar ro‘yxatidan manfiy bo‘lmaganlarni olib, ularning kvadratini chiqaring.
# Yechim:

# sonlar = [1,2,3,4,-1,5,6,-4,7,8,-12,9]
# res = map(lambda x: x**2,filter(lambda x: x > 0,sonlar))
# print(list(res))

# 7️⃣ Ballar ro‘yxatidan 60 dan o‘tganlarni olib, har biriga 5 ball qo‘shing.
# Yechim:

# ballar = [15,16,74,100,60,77,88,55]
# res = map(lambda x: x + 5,filter(lambda x: x > 60,ballar))
# print(list(res))

# 8️⃣ Narxlar ro‘yxatiga 10% chegirma qo‘llang va yangi narxlar ro‘yxatini chiqaring.

# narxlar = [155,124,121,189,156,742,1235,135,1633,613]
# chegirma_narxlar = list(map(lambda x: round(x * 0.9,2), narxlar))
# print(chegirma_narxlar)

# 9️⃣ Ismlar ro‘yxatidan faqat uzunligi 5 ta va undan katta bo‘lgan ismlarni ajrating.

# ismlar = ["xazratbek","nozimjon","abbos","jasmina","alisher","bek"]
# res = filter(lambda ism: len(ism) >= 5,ismlar)
# print(list(res))

# 🔟 Berilgan sonlar ro‘yxatidagi eng katta sonni toping (❗️ max() ishlatmasdan).

# Birinchi yechim:
# sonlar = [1,2,3,4,12412412,5,-1,6,7,8,9,12,15,124,15,19,4412]
# eng_kattasi = 0
# for son in sonlar:
#     if son < 0:
#         pass
#     if son > eng_kattasi:
#         eng_kattasi = son
# print(eng_kattasi)

# Ikkinchi yechim:
# from functools import reduce

# sonlar = [1,2,3,4,12412412,5,6,7,8,9,12,15,124,15,19,4412]

# eng_kattasi = reduce(lambda a, b: a if a > b else b, sonlar)

# print(eng_kattasi)

# 1️⃣1️⃣ Ikki ro‘yxat berilgan: mahsulot nomlari va narxlari.
# Narxi 50000 dan katta mahsulotlarni (nom, narx) ko‘rinishida chiqaring.
# Yechim:
# mahsulotlar = ["olma","anor","bexi","sabzi","sharbat"]
# narxlar = [14555,51000,42122,1242,52000]
# res = zip(mahsulotlar,narxlar)
# filtered = filter(lambda x: x[1] > 50000,res)
# print(list(filtered))

# 1️⃣2️⃣ Sonlar ro‘yxatidagi toq sonlar yig‘indisini toping
# # Yechim:
# sonlar = [1,2,3,4,12412412,5,6,7,8,9,12,15,124,155,19,4412]
# toq_sonlar = filter(lambda son: son % 2 == 1,sonlar)
# print(list(toq_sonlar))

# 1️⃣3️⃣ Ismlar ro‘yxatini ularning uzunligiga aylantiring.
# 📌 ["Ali", "Hasan"] → [3, 5]

# ismlar = ["Ali", "Hasan","Xazratbek","Kozimjon"]
# len_ismlar = map(lambda ism: len(ism),ismlar)
# print(list(len_ismlar))

# 1️⃣4️⃣ Berilgan sonlar ro‘yxatidan musbat sonlar ko‘paytmasini toping.
# from functools import reduce

# sonlar = [1,2,-4,-1,-14,3,4,12,5,-9,6]
# natija = reduce(lambda x,y: x*y,filter(lambda son: son > 0,sonlar))
# print(natija)

# 1️⃣5️⃣ Ikki ro‘yxat berilgan: talabalar va ularning ballari.
# Faqat 70 dan yuqori olganlarni chiqarish.

# talabalar = ["Ali","Hasan","Husan","Vali"]
# talaba_ballari = [15,77,52,88]

# res = zip(talabalar,talaba_ballari)
# filtered = filter(lambda ball: ball[1] > 70, res)
# print(list(filtered))

# 1️⃣6️⃣ Talabalar ballari berilgan.
# * 60 dan o‘tganlarni tanlang
# * Har biriga 10 ball qo‘shing
# * Yangi o‘rtacha ballni hisoblang
# from functools import reduce

# talaba_ballari = [15,77,52,88]
# otganlar = reduce(lambda x, y: x+y, map(lambda ball: ball + 60, filter(lambda ball: ball > 60,talaba_ballari))) / len(talaba_ballari)
# print(otganlar)

# 1️⃣7️⃣ Sonlar ro‘yxatidan:

# * manfiylarni olib tashlang
# * faqat juftlarni qoldiring
# * ularning kvadratlari yig‘indisini toping
# sonlar = [1,2,-4,-1,-14,3,4,12,5,-9,6]
# natija = map(lambda son: son ** 2, filter(lambda son: son > 0 and son % 2 == 0, sonlar))
# print(list(natija))

# 1️⃣8️⃣ Mahsulotlar va narxlar berilgan.

# * 20% chegirma qo‘llang
# * 100000 dan yuqori bo‘lganlarni chiqaring

# mahsulotlar = ["olma","anor","bexi","sabzi","sharbat","gosh"]
# narxlar = [14555,51000,42122,1242,52000,189000]
# chegirma = filter(lambda son: son > 100000, map(lambda son: son[1] * 0.80, zip(mahsulotlar,narxlar)))
# print(list(chegirma))

# 1️⃣9️⃣ Ismlar ro‘yxatida:

# * uzunligi 4 dan katta bo‘lganlarni oling
# * katta harfga o‘tkazing
# * bitta stringga birlashtiring

# ismlar = ["Ali","Hasan","Husan","Vali"]
# temp_res = map(lambda ism: ism.upper(),filter(lambda ism: len(ism) > 4,ismlar))
# final_res = " ".join(list(temp_res))
# print(final_res)

# 2️⃣0️⃣ Sonlar ro‘yxatidagi eng katta va eng kichik sonlar ayirmasini toping
# (max va min ishlatmasdan).

# from functools import reduce
# sonlar = [1,2,3,4,12,5,9,6,77]
# eng_kattasi = reduce(lambda x, y: x if x > y else y,sonlar)
# eng_kichik = reduce(lambda x, y: x if x < y else y,sonlar)
# print(eng_kattasi - eng_kichik)

# 2️⃣1️⃣ 3 ta ro‘yxat berilgan: ism, yosh, ball.
# Faqat 18 yoshdan katta va 70 balldan yuqori bo‘lganlarni chiqaring.

# ismlar = ["Ali","Hasan","Husan","Vali"]
# yoshlar = [15,16,19,22]
# ballar = [67,51,77,66]
# zipped = zip(ismlar,yoshlar,ballar)
# natija = filter(lambda x: x[1] > 18 and x[2] > 70,zipped)
# print(list(natija))

# 2️⃣2️⃣ Matnlar ro‘yxatidan:

# * bo‘sh stringlarni olib tashlang
# * qolganlarini katta harfga o‘tkazing

# matnlar = ["Ali","Hasan","","Husan","Vali",""]

# natija = map(lambda matn: matn.upper(),filter(lambda matn: len(matn) > 0,matnlar))
# print(list(natija))

# 2️⃣3️⃣ Sonlar ro‘yxatini dictionary ko‘rinishiga o‘tkazing:
# son → uning kvadrati

# sonlar = [1,2,3,4,12,5,9,6,77]
# sonlar_kvadrati = list(map(lambda son: son ** 2,sonlar))
# natija = {}
# for index,son in enumerate(sonlar):
#     natija[son] = sonlar_kvadrati[index]

# print(natija)

# 2️⃣4️⃣ Talabalar ballaridan:

# * eng yuqori 3 tasini tanlang
# * ularning o‘rtacha qiymatini hisoblang
# from functools import reduce

# talaba_ballari = [67,51,77,66]
# ballar_kamayish_tartibida = sorted(talaba_ballari,reverse=True)
# avg_ball = reduce(lambda x,y: x + y,ballar_kamayish_tartibida) / len(ballar_kamayish_tartibida)
# print(avg_ball)

# 2️⃣5️⃣ Berilgan gapdagi so‘zlar ro‘yxatidan:

# * uzunligi 3 dan katta so‘zlarni tanlang
# * ularni bitta gapga birlashtiring
# gaplar = ["salom","nima","alo","gaplar","ok","o'qishlar","yaxshimi"]
# natija = " ".join(sorted(filter(lambda soz: len(soz) > 3,gaplar),key=len))
# print(natija)