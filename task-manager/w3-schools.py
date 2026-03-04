# mylist = ['apple', 'banana', 'cherry']
# mylist[1:2] = ['kiwi', 'mango']
# print(mylist)
# print(mylist[2])
# fruits = ["apple", "banana", "cherry"]
# fruits = iter(fruits)
# print(next(fruits))
# print(next(fruits))

# import random
# import time

# def datchik_malumoti():
#     while True:
#         # Sensor qiymatini simulyatsiya qilamiz
#         qiymat = random.uniform(20.0, 30.0)
#         yield round(qiymat, 2)
#         time.sleep(1) # 1 soniya kutish

# # Ma'lumotni qabul qilish
# for daraja in datchik_malumoti():
#     print(f"Hozirgi harorat: {daraja}°C")
#     if daraja > 28.0:
#         print("Diqqat! Harorat ko'tarilib ketdi.")
#         break # Jarayonni to'xtatish


# import re
# txt = 'The rain in Spain'
# x = re.findall('[a-c]', txt)
# print(x)

import re
txt = 'The rain in Spain'
x = re.search('a', txt)
print(x)
print(x.start())