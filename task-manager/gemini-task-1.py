# class TelegramUser:
#     def __init__(self,ism,familiya):
#         self.ism = ism
#         self.familiya = familiya
#         self.__status = True

#     def __str__(self):
#         return f"{self.ism}\n{self.familiya}"

#     @property
#     def status(self):
#         return self.__status

#     @status.setter
#     def status(self,new_status: bool):
#         self.__status = new_status
#         return self.__status


#     def get_username(self):
#         return self.ism

#     def get_surname(self):
#         return self.familiya

#     def xabar_yozish(self,xabar):
#         return f"{xabar}"

#     def status_ozgartir(self):
#         if self.__status:
#             self.__status = False
#             return self.__status
#         return None

# user_1 = TelegramUser("xazratbek","turdaliyev")
# print(user_1.xabar_yozish("Salom Dunyo!"))
# print(f"User status: {'Online' if user_1.status else 'Offline'}")
# print(user_1.status_ozgartir())
# print(f"User status: {'Online' if user_1.status is not None else 'Offline'}")
# user_1.status = False

# class Smartfon:
#     def __init__(self,model,protsessor_nomi):
#         self.model = model
#         self.cpu = self.Protsessor(protsessor_nomi)

#     def __str__(self):
#         return f"{self.model} {self.cpu.display_info()}"

#     def show(self):
#         cpu_info = self.cpu.display_info()
#         return f"Telefon nomi: {self.model}\n{cpu_info}"

#     class Protsessor:
#         def __init__(self,nomi):
#             self.nomi = nomi

#         def __str__(self):
#             return self.nomi

#         def display_info(self):
#             return f"Protsessor nomi: {self.nomi}"

# ayfon = Smartfon("Iphone","A17 Bionic")
# print(ayfon.show())

# Tashqi Klass: Buyurtma__init__ metodida mijoz_ismi va sanani qabul qilsin.Ichida mahsulotlar degan bo'sh ro'yxat (list) bo'lsin.qoshish(nomi, narxi, miqdori) degan metod yarating. Bu metod ichida Mahsulot klassidan yangi ob'ekt olib, ro'yxatga qo'shsin.umumiy_hisob() degan metod bo'lsin, u barcha ichki mahsulotlar narxini hisoblab chiqsin.Ichki Klass: Mahsulot (Inner Class)__init__ metodida nomi, narxi va miqdorini qabul qilsin.qaytar_qiymat() degan metod bo'lsin, u bitta mahsulotning umumiy summasini ($narxi \times miqdori$) qaytarsin.

from datetime import datetime

class Buyurtma:
    __buyurtma_soni = 0
    def __init__(self,mijoz_ismi):
        self.mijoz_ismi = mijoz_ismi
        self.sana = datetime.now()
        self.mahsulotlar = []

        Buyurtma.__buyurtma_soni += 1

    def __str__(self):
        return f"{self.mijoz_ismi} | {self.Mahsulot}"

    @classmethod
    def umumiy_buyurtmalar_soni(cls):
        return cls.__buyurtma_soni

    def buyurtmadagi_mahsulotlar_soni(self):
        return len(self.mahsulotlar)

    def qoshish(self,nomi, narxi, miqdori):
        mahsulot = self.Mahsulot(nomi,narxi,miqdori)
        self.mahsulotlar.append(mahsulot)
        return f"Mahsulot: {nomi}, mahsulotlar ro'yxatiga qo'shildi."

    def umumiy_hisob(self):
        umumiy_summa = 0
        for mahsulot in self.mahsulotlar:
            umumiy_summa += int(mahsulot.narxi)

        return umumiy_summa

    class Mahsulot:
        def __init__(self,mahsulot_nomi,narxi,miqdor):
            self.mahsulot_nomi = mahsulot_nomi
            self.narxi = narxi
            self.miqdor = miqdor

        def __str__(self):
            return f"{self.mahsulot_nomi} | {self.narxi} | {self.miqdor}\n"

        def qaytar_qiymat(self):
            return self.narxi * self.miqdor


buyurtma = Buyurtma("Ali")
buyurtma.qoshish("Olma","10000",100)
buyurtma.qoshish("Non","5600",100)
buyurtma.qoshish("Banan","20000",2)
print(f"Buyurtmaning umumiy summasi: {buyurtma.umumiy_hisob()}\nBuyurtmalar soni: {buyurtma.umumiy_buyurtmalar_soni()}\nBuyurtmadagi mahsulotlar soni: {buyurtma.buyurtmadagi_mahsulotlar_soni()}")