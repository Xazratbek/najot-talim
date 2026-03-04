# Vazifa 1:

# filepath = "hello.txt"
# vazifa_1 = open(filepath,"w")
# vazifa_1.write("Salom Python")
# vazifa_1.close()

# Vazifa 2:
# vazifa_2 = open("hello.txt","r")
# natija = vazifa_2.read()
# print(natija)
# vazifa_2.close()

# Vazifa 3:
# vazifa_2 = open("names.txt","r")
# natija = len(vazifa_2.readlines())
# print(natija)
# vazifa_2.close()

# Vazifa 4:
# from datetime import datetime
# vazifa_4 = open("log.txt","a")
# vazifa_4.write(f"Dastur ishga tushdi || Ishga tushgan vaqt: {datetime.now()}\n")
# vazifa_4.close()

# Vazifa 5:
# from pathlib import Path

# file_path = Path("names.txt")

# if file_path.exists():
#     print("Fayl mavjud")
# else:
#     print("Fayl mavjud emas")

# Vazifa 6:

# vazifa_6 = open("names.txt","r")
# natija = vazifa_6.read()
# natija = natija.replace("\n"," ")
# word_count = natija.split(" ")
# print("So'zlar soni",len(word_count))

# natija = vazifa_6.read()
# print(len(natija.split()))

# Vazifa 7:
# vazifa_7 = open("names.txt","r")
# natija = vazifa_7.readlines()
# uzun_qator = 0
# uzun_qator_index = 0
# for index, value in enumerate(natija):
#     if len(value) > uzun_qator:
#         uzun_qator = len(value)
#         uzun_qator_index = index
# vazifa_7.close()
# print(uzun_qator_index)

# print(f"Eng uzun qator uzungligi: {uzun_qator}, osha qatordagi content: {natija[uzun_qator_index]}")
# vazifa_7 = open("names.txt","r")
# natija = vazifa_7.readlines()
# vazifa_7.close()
# print(max(natija,key=len))

# Vazifa 8:
# vazifa_8 = open("numbers.txt","r")
# yigindi = 0
# natija = vazifa_8.readlines()
# print(sum([int(num) for num in natija]))

# Vazifa 9:
# vazifa_9 = open("input.txt","r")
# natija = vazifa_9.readlines()
# natija = [word.upper() for word in natija]
# vazifa_9 = open("output.txt","a")
# vazifa_9.writelines(natija)
# vazifa_9.close()

# Vazifa 10:
# with open("data.txt","r") as data, open("clean.txt","a") as cleanfile:
#     for line in data:
#         if line.strip():
#             cleanfile.write(line)

# Vazifa 11:
# with open("story.txt","r") as file:
#     natija = file.read()
#     natija = natija.split()
#     hisob = {}
#     for soz in natija:
#         hisob[soz] = hisob.get(soz,0) + 1
#     data = hisob.values()
#     print(max(data))

# Vazifa 12:
# with open("mixed.txt","r") as mixed, open("numbers.txt","a") as numbers:
#     natija = mixed.read()
#     natija = natija.split()
#     for num in natija:
#         if num.isdigit():
#             numbers.writelines(f"{num}\n")

# Vazifa 13:
# with open("source.txt","r") as source, open("backup.txt","a") as backup:
#     source_copy = source.read()
#     backup.writelines(source_copy)

# Vazifa 14:

# with open("words.txt","r") as file:
#     natija = file.read()
#     natija = natija.split()
#     eng_uzun_soz = 0
#     soz_index = 0
#     for index, soz in enumerate(natija):
#         if len(soz) > eng_uzun_soz:
#             eng_uzun_soz = len(soz)
#             soz_index = index

#     print(f"eng uzun so'z: {natija[soz_index]}")

# with open("numbers.txt","r") as file:
#     natija = file.read()
#     file.writelines()
#     natija = natija.split()
#     eng_katta = max([int(son) for son in natija])
#     eng_kichik = min([int(son) for son in natija])
#     average = sum([int(son) for son in natija])/len([int(son) for son in natija])
#     print(f"Eng kattasi: {eng_katta} | Eng kichigi: {eng_kichik} | O'rtachasi: {average}")


# import time

# start = time.time()

# for i in range(1_000_000):
#     pass

# end = time.time()

# print("Kod ishlash vaqti:", end - start)