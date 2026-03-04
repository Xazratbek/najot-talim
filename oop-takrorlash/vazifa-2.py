# 2 — Atributlar & Properties (Getter/Setter)

# TZ: Product sinfi. price private bo‘ladi. Tashqaridan price ga set qilishda property va @price.setter dan foydalan — price musbat son bo‘lishi kerak. Ayrıca read-only sifatida id beriladi (uuid).

# Detallar:

# __init__ ichida id = uuid4() generatsiya qiling.

# @property price qaytaradi; @price.setter validatsiya qiladi.

# __repr__ foydali matn qaytarsin (debug uchun).

# OOP konseptlar: enkapsulyatsiya, properties, immutability qayerda kerakligi.

# Tushuntirish: property — tashqaridan attribute kabi ko‘rinadi, ammo ichida getter/setter logikasi bor. Bu muhim: keyinroq DB modelga yoki serialization’ga o‘tganingda bu joyni o‘zgartirmasdan foydalanaverasan.
from uuid import uuid4

class Product:
    def __init__(self, name: str):
        self._id = uuid4()
        self.name = name
        self._price = 0

    def __str__(self):
        return f"Product: {self.name} | ID: {self._id}"

    def __repr__(self):
        return f"Product(id={self.id},name={self.name},price={self._price})"

    def get_product_name(self):
        return self.name

    @property
    def id(self):
        return self._id

    def change_name(self,new_name):
        if new_name != self.name:
            self.name = new_name
            return self.name
        else:
            raise ValueError("Ismni o'zgartirish uchun iltimos yangi ism kiriting")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self,new_price: float) -> float:
        if new_price <= 0:
            raise ValueError("Manfiy va 0 soni kiritish mumkin emas!")
        self._price = new_price

product_1 = Product("Kurtka")
print(product_1.get_product_name())
product_1.price = 10000
print(product_1.price)
print(product_1.change_name("Kurtka qishki"))
print(product_1.get_product_id())
print(product_1.get_product_name())
