# 1while sikli yordamida 1 dan 10 gacha bo‘lgan sonlarni ekranga chiqaring.

# 2.while sikli yordamida 10 dan 1 gacha bo‘lgan sonlarni kamayish tartibida chiqaring.

# 3.while sikli yordamida 1 dan 20 gacha bo‘lgan juft sonlarni ekranga chiqaring.

# 4.while sikli yordamida 1 dan 5 gacha bo‘lgan sonlar yig‘indisini toping va ekranga chiqaring.

# 5.while sikli yordamida "Salom" so‘zini 5 marta ekranga chiqaring.

# 6.Foydalanuvchi ketma-ket sonlar kiritadi. Agar 0 kiritilsa, sikl to‘xtaydi. while yordamida kiritilgan sonlar yig‘indisini toping.

# 7.Foydalanuvchi bitta butun son kiritadi. while sikli yordamida bu son nechta raqamdan iborat ekanini aniqlang.

# 8.Foydalanuvchi ketma-ket sonlar kiritadi. Agar 0 kiritilsa, sikl to‘xtaydi. while yordamida eng katta sonni toping.

# 9.To‘g‘ri parol "1234" deb berilgan. Foydalanuvchi to‘g‘ri parol kiritmaguncha while sikli ishlasin.

# 10.Foydalanuvchi butun son kiritadi. while sikli yordamida ushbu sonni teskari ko‘rinishda ekranga chiqaring.

# Vazifa 1
# son = 0
# while son < 10:
#     son += 1
#     print(son)

# Vazifa 2
# son = 10
# while True:
#     print(son)
#     son -= 1
#     if son == 0:
#         break

# Vazifa 3
# son = 0
# while son < 20:
#     if son % 2 != 0:
#         son += 1
#         continue
#     else:
#         print(son)
#         son += 1

# Vazifa 4
# yigindi = 0
# sanoq = 0
# while True:
#     yigindi += sanoq
#     sanoq += 1
#     if sanoq > 5:
#         break
# print(f"1-dan 5-gacha sonlar yig'indisi: {yigindi}")

# Vazifa 5
# sanoq = 0
# while sanoq != 5:
#     print("Salom")
#     sanoq += 1

# Vazifa 6
# yigindi = 0
# while True:
#     user_input = int(input("Son kiriting: "))
#     if user_input == 0:
#         break
#     yigindi += user_input

# print(f"Siz kiritgan sonlar yig'indisi: {yigindi}")

# Vazifa 7
# son = int(input("Son kiriting: "))
# raqamlar = 0
# while son > 0:
#     son //= 10
#     raqamlar += 1
# print(f"{raqamlar} ta raqam bor")


# Vazifa 8
# eng_katta_son = 0
# while True:
#     son  = int(input("Son kiriting: "))
#     if son == 0:
#         break

#     if son > eng_katta_son:
#         eng_katta_son = son
# print(f"Siz kiritgan sonlar orasida eng katta son: {eng_katta_son}")

# Vazifa 9
# togri_parol = 1234
# while True:
#     user_input = int(input("Son kiriting: "))
#     if user_input == togri_parol:
#         print("Tog'ri parol kiritdingiz")
#         break
#     else:
#         print("Parol xato!")
#         continue

# Vazifa 10
n = int(input("Son kiriting: "))
while n > 0:
    print(n % 10, end='')
    n //= 10
