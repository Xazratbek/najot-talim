# ==================================================
# TZ-10: OMBOR VA BUYURTMALAR BOSHQARUV TIZIMI
# ==================================================

# Vazifa:
# Mahsulotlar, ombor va buyurtmalarni
# algoritmik tarzda boshqarish.

# --------------------------------
# 1. Product class
# --------------------------------
# Atributlar:
# - name
# - __price (private)
# - __stock (private)

# Metodlar:
# - @property price
# - @price.setter

# - reduce_stock(quantity)

# --------------------------------
# 2. Order class
# --------------------------------
# Atributlar:
# - products (dict: product -> quantity)

# Metodlar:
# - add_product(product, quantity)

# - calculate_price()

# Algoritm:
# - barcha mahsulot narxlarini
#   ko‘paytirib yig‘ish

# --------------------------------
# 3. Warehouse class
# --------------------------------
# Metodlar:
# - @staticmethod check stock(products)

# Algoritm:
# - Agar bitta mahsulot ham yetarli bo‘lmasa:
#     - buyurtma bekor qilinsin

# --------------------------------
# 4. SmartOrder class (Order dan meros)
# --------------------------------
# Metodlar:
# - apply_discount()

# Algoritm:
# - Agar total > 1 000 000 bo‘lsa:
#     - 10% chegirma

# 📌 inheritance + super() shart

# --------------------------------
# Algoritmik talab:
# --------------------------------
# - summa hisoblash
# - shartli chegirma
# - ombor nazorati

class Product:
    def __init__(self,name,price,stock):
        self.name = name
        self.__price = price
        self.__stock = stock

    def __str__(self):
        return f"Mahsulot: {self.name} | Narxi: {self.__price} | Soni: {self.__stock}"

    @property
    def price(self):
        return int(self.__price)

    @price.setter
    def price(self,new_price):
        eski_narx = self.__price
        if new_price > 0:
            self.__price = new_price

            print(f"Mahsulot: {self.name} | Narxi yangilandi: {eski_narx} -> {new_price}")

    @price.deleter
    def price(self):
        del self.__price

    @property
    def stock(self):
        return int(self.__stock)

    @stock.setter
    def stock(self,qunatity):
        old_stock = self.__stock
        if qunatity <= self.__stock:
            self.__stock -= qunatity
            print(f"Mahsulot: {self.name}-miqdori: {old_stock} dan -> {qunatity}-ga kamaytirildi | Ombordagi qoldiq: {self.__stock}")

        return None

    def mahsulot_ayirish(self,quantity):
        if quantity <= self.__stock:
            self.__stock -= quantity
            return f"Mahsulot {self.name} soni: {quantity}-ga kamaytirildi | Ombordagi qoldiq: {self.__stock}"
        else:
            return f"Mahsulot {self.__stock}-ta mavjud!\nOrtiqcha mahsulot sonini kiritmang!"

    def reduce_stock(self,quantity):
        if quantity > 0:
            eski_qoldiq = self.__stock
            self.__stock += quantity

            return f"Mahsulot: {self.name} soni: {eski_qoldiq}-dan -> {quantity}-ga ortdi | Ombordagi qoldiq: {self.__stock}"

        return f"Iltimos musbat son kiriting"

class Order:
    def __init__(self):
        self.products = {}

    def add_product(self,product,quantity):
        if quantity <= product.stock:
            self.products[product] = quantity

            return f"Mahsulot: {product.name} korzinkaga muvaffaqiyatli qo'shildi"
        else:
            return f"Omborda {product.name}-dan {product.stock}-ta qolgan {quantity}-ta olma omborda mavjud emas"

    def calculate_price(self):
        summa = 0
        for product, quantity in self.products.items():
            summa += product.price * quantity

        return summa

    def get_orders(self):
        data = f"Savatdagi mahsulotlar soni: {len(self.products)}\nKorzinkangizga qo'shilgan mahsulotlar ro'yxati:\n"
        for product, quantity in self.products.items():
            data += f"Mahsulot: {product.name} | Qiymati: {quantity} | Narxi: {product.price * quantity}\n"

        return data + f"Savatga qo'shilgan mahsulotlaringiz uchun umumiy tolov: {self.calculate_price()}"

class Warehouse:
    @staticmethod
    def check_stock(order):
        data = {}
        for product, quantity in order.products.items():
            if quantity <= product.stock:
                data["product"] = product
                data['quantity'] = quantity
                data["is_rejected"] = False
                data["reject_reason"] = None

            else:
                data["product"] = product
                data["quantity"] = quantity
                data["is_rejected"] = True
                data["reject_reason"] = f"{product.name}-mahsuloti omborda yetarli emas | Siz olmoqchi bo'lgan qiymat: {quantity} | Ombordagi qoldiq: {product.stock}"
                del order.products[product]

        return data

class SmartOrder(Order):
    def __init__(self):
        super().__init__()

    def apply_discount(self):
        total = super().calculate_price()
        if total > 1000000:
            total = total * 0.9
            return total

        return None

print("Mahsulotlar yaratish va ular ustida amallar boshlandi...\n")
olma = Product("Olma",10000,100)
banan = Product("Banan",20000,200)
non = Product("Non",5600,1000)

non.stock = 500
print(olma.reduce_stock(10))
print(olma.mahsulot_ayirish(50))
print("\nMahsulotlar yaratish va ular ustidagi amallar tugadi...\n")

print("Birinchi buyurtmani yaratish va ular ustida amallar boshlandi\n")
zakaz_1 = Order()
smart_order = SmartOrder()
smart_order.products = zakaz_1.products

print(zakaz_1.add_product(olma,25))
print(zakaz_1.add_product(banan,2))
print(zakaz_1.add_product(olma,60))
print(zakaz_1.add_product(non,150))
print(zakaz_1.get_orders())

result = Warehouse.check_stock(zakaz_1)
chegirma = smart_order.apply_discount()
if result['is_rejected']:
    print(result['reject_reason'])
else:
    print(f"Umumiy buyurtmangiz uchun to'lov: {zakaz_1.calculate_price()} {'10 foiz chegirmadagi narx: ' + str(chegirma) if chegirma is not None else ' '}")

print("\nBirinchi buyurtmani yaratish va ular ustida amallar tugadi\n")

print("Ikkinchi buyurtmani yaratish va ular ustida amallar boshlandi\n")
zakaz_2 = Order()
smart_order_2 = SmartOrder()
zakaz_2.add_product(olma,100)
zakaz_2.add_product(banan,50)
print(zakaz_2.get_orders())

result_2 = Warehouse.check_stock(zakaz_2)
chegirma = smart_order_2.apply_discount()
if result_2['is_rejected']:
    print(result_2['reject_reason'])
else:
    print(f"Umumiy buyurtmangiz uchun to'lov: {zakaz_2.calculate_price()} {'10 foiz chegirmadagi narx: ' + str(chegirma) if chegirma is not None else ' '}")

print("\nIkkinchi buyurtmani yaratish va ular ustida amallar tugadi\n")