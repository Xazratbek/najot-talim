# ==============================
# TZ: RESTORAN BUYURTMA TIZIMI
# (RESTAURANT MANAGEMENT SYSTEM)
# ==============================

# Vazifa:
# Restorandagi menyu, buyurtmalar va to‘lov jarayonlarini
# boshqaruvchi tizim yozish.
# Dastur OOP asosida va real loyiha arxitekturasi ko‘rinishida bo‘lishi shart.

# --------------------------------
# 1. MenuItem class
# --------------------------------
# Atributlar:
# - name          : taom nomi
# - price         : taom narxi
# - is_available  : taom hozir mavjud yoki yo‘qligi (True / False)

# Metodlar:
# - make_available()
#   # Taomni yana sotuvga ochish uchun ishlatiladi
#   # Masalan: oshpaz taomni qayta tayyorlab qo‘yganda

# - make_unavailable()
#   # Taom vaqtincha mavjud bo‘lmaganda chaqiriladi
#   # Masalan: mahsulot tugab qolganda

# --------------------------------
# 2. Order class
# --------------------------------
# Atributlar:
# - order_id : buyurtma raqami
# - items    : buyurtmadagi taomlar ro‘yxati
# - status   : buyurtma holati
#              (new, cooking, done)

# Metodlar:
# - add_item(item)
#   # Buyurtmaga yangi taom qo‘shadi
#   # Faqat taom mavjud (is_available=True) bo‘lsa qo‘shilishi kerak

# - remove_item(item)
#   # Buyurtmadan berilgan taomni olib tashlaydi
#   # Agar taom buyurtmada mavjud bo‘lsa

# - get_total()
#   # Buyurtmadagi barcha taomlarning umumiy narxini hisoblab qaytaradi

# - change_status(new_status)
#   # Buyurtma holatini o‘zgartiradi
#   # Masalan: new -> cooking -> done

# --------------------------------
# 3. Cashier class
# --------------------------------
# Atributlar:
# - name : kassir ismi

# Metodlar:
# - accept_payment(order)
#   # Buyurtma uchun to‘lov qabul qiladi
#   # Odatda buyurtma "done" holatiga o‘tganda chaqiriladi

# - print_receipt(order)
#   # Chek chiqarib beradi:
#   # - buyurtma raqami
#   # - barcha taomlar
#   # - umumiy summa

# --------------------------------
# 4. Restaurant class
# --------------------------------
# Atributlar:
# - menu   : restorandagi barcha taomlar ro‘yxati
# - orders : hozirgi barcha buyurtmalar

# Metodlar:
# - add_menu_item(item)
#   # Restoran menyusiga yangi taom qo‘shadi

# - show_menu()
#   # Faqat mavjud (is_available=True) taomlarni ekranga chiqaradi

# - create_order(order_id)
#   # Yangi buyurtma yaratadi
#   # Uni orders ro‘yxatiga qo‘shib, obyektni qaytaradi

# - show_orders()
#   # Restorandagi barcha buyurtmalarni
#   # ularning holati bilan birga chiqaradi

# --------------------------------
# Qo‘shimcha talablar:
# --------------------------------
# - Har bir class alohida faylda yozilishi tavsiya etiladi
# - Kodda print orqali foydalanuvchi uchun tushunarli xabarlar chiqarilsin
# - OOP tamoyillariga amal qilinsin
# - Keraksiz global o‘zgaruvchilardan foydalanilmasin

from enum import Enum
import random
from dataclasses import dataclass
from datetime import datetime


class MenuItem:
    def __init__(self,name,price):
        self.id = random.randint(1,10000)
        self.name = name
        self.price = price
        self.__is_available = True

    def __str__(self):
        return f"ID: {self.id} | Taom: {self.name} | Narxi: {self.price} | Xolati: {'Mavjud' if self.__is_available else 'Mavjud emas'}"

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_menu_item_id(self):
        return self.id

    @property
    def is_available(self):
        return self.__is_available

    def make_available(self):
        if not self.__is_available:
            self.__is_available = True

    def make_unavailable(self):
        if self.__is_available:
            self.__is_available = False


class OrderStatus(Enum):
    NEW = "new"
    COOKING = "cooking"
    DONE = "done"

@dataclass
class OrderStatusChanges:
    order_id: int
    old_status: OrderStatus
    new_status: OrderStatus | None
    changed_at: datetime

class Order:
    def __init__(self,order_status: OrderStatus):
        self.order_id = random.randint(1,10000)
        self.orders = {}
        self.status = order_status
        self.order_statuses_history = []

    def __str__(self):
        return f"Buyurtma: {self.order_id} | Statusi: {self.status.value}"

    def get_order_id(self):
        return self.order_id

    def get_order_count(self):
        yigindi = 0
        for data in self.orders.values():
            yigindi += data['count']

        return yigindi

    def get_order_status(self):
        return self.status

    def add_item(self,new_item: MenuItem):
        if not new_item.is_available:
            return f"Mahsulot {new_item.name} mavjud emas!"

        if new_item.id in self.orders:
            self.orders[new_item.id]["count"] += 1

        else:
            self.orders[new_item.id] = {
                "item": new_item,
                "status": self.status,
                "order_id": self.order_id,
                "count": 1
            }
            history = OrderStatusChanges(self.order_id,self.status,None,datetime.now())
            self.add_order_status_history(history)

        return f"Taom: {new_item.name} savatchaga qo'shildi"

    def remove_item(self,item):
        if item.id in self.orders:
            self.orders.pop(item.id)
            return f"Mahsulot: {item.name} savatdan olib tashlandi!"
        else:
            return f"Savatdan {item.name} mahsuloti mavhud emas!"

    def calculate_price(self):
        summa = 0
        for key in self.orders.keys():
            summa += self.orders[key]['item'].price * self.orders[key]['count']

        return summa

    def add_order_status_history(self,change_history: OrderStatusChanges):
        self.order_statuses_history.append(change_history)

    def change_status(self, new_status):
        togri_xolat_ozgarishi = {
            OrderStatus.NEW: OrderStatus.COOKING,
            OrderStatus.COOKING: OrderStatus.DONE
        }

        if togri_xolat_ozgarishi.get(self.status) != new_status:
            raise ValueError("Notog'ri status o'zgarishi")

        old_status = self.status
        self.status = new_status
        order_status_history = OrderStatusChanges(self.order_id,old_status,new_status,datetime.now())

        self.add_order_status_history(order_status_history)
        return f"Buyurtma: {self.order_id} xolati {old_status.value} -> dan {new_status.value}-ga o'zgartirildi"

    def get_orders(self):
        data = "Savatga qo'shilgan buyurtmalaringiz: \n"
        if self.orders:
            for data in self.orders.values():
                data += f"Buyurtma: {data['item'].name} | Buyurtma xolati: {data['item'].status.value}\n"
        else:
            return "Buyurtmalar mavjud emas"

        return data

    def get_order_statuses_history(self):
        if self.order_statuses_history:
            data = "Buyurtma xolatlari tarixi: \n"
            for buyurtma in self.order_statuses_history:
                data += f"\nOrder id: {buyurtma.order_id} | Oldingi xolati: {buyurtma.old_status.value} | Yangi xolati: {buyurtma.new_status.value if buyurtma.new_status is not None else 'Mavjud emas'} | O'zgartirilgan vaqt: {buyurtma.changed_at}\n"

            return data

        return "Buyurtmalar tarixi mavjud emas!"

class Kassir:
    def __init__(self,name):
        self.id = random.randint(1,10000)
        self.name = name

    def accept_payment(self,charge, order: Order):
        qaytim = 0
        if charge > order.calculate_price():
            qaytim += charge-order.calculate_price()

        if charge >= order.calculate_price() and order.get_order_status().value == OrderStatus.DONE.value:
            chek = self.print_receipt(order)
            data = f"\nTo'lov muvaffaqiyatli amalga oshdi. {'Qaytimingizni oling: ' + str(qaytim)  if qaytim != 0 else ''}"
            return chek + data

        elif order.get_order_status().value != OrderStatus.DONE.value:
            return f"Buyurtma tayyor emas. Buyurtma xolati: {order.get_order_status().value}"

        else:
            return f"To'lov uchun mablag' yetarli emas, to'lanishi kerak bo'lgan summa: {order.calculate_price()}, yetishmayotgan mablag': {order.calculate_price()-charge}"

    def print_receipt(self, order):
        width = 40
        lines = []

        lines.append("=" * width)
        lines.append("Xazratbek Restorani".center(width))
        lines.append("Chek".center(width))
        lines.append("=" * width)

        lines.append(f"Order ID: {order.order_id}")
        lines.append(f"Kassir: {self.name}")
        lines.append(f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-" * width)

        lines.append(f"{'Mahsulot':20}{'Soni':>5}{'Narxi':>7}")
        lines.append("-" * width)

        for data in order.orders.values():
            item = data["item"]
            count = data["count"]
            lines.append(
                f"{item.name:20}"
                f"{count:^5}"
                f"{item.price:>7.2f}"
            )

        lines.append("-" * width)
        lines.append(f"{'Umumiy':25}{order.calculate_price():>7.2f}")
        lines.append("=" * width)
        lines.append("Xaridingiz uchun rahmat )!".center(width))

        chek = "\n".join(lines)
        return chek


class Restoran:
    def __init__(self):
        self.menu = []
        self.orders = []

    def add_menu_item(self,menu: MenuItem):
        self.menu.append(menu)
        return f"Mahsulot: {menu.name} restoran menyusiga qo'shildi"

    def show_menu(self):
        if self.menu:
            data = "Restoranimizdagi mavjud taomlar: \n"
            for taom in self.menu:
                if taom.is_available:
                    data += f"\n{taom}\n"

            return data

        else:
            return "Restoranimizda taomlar mavjud emas!"

    def create_order(self,mahsulot: MenuItem):
        order = Order(OrderStatus.NEW)
        order.add_item(mahsulot)
        self.orders.append(order)
        return order

    def show_orders(self):
        if self.orders:
            data = "Restoranimizdagi barcha buyurtmalar va ularning xolatlari: \n"
            for buyurtma in self.orders:
                data += buyurtma

            return data
        else:
            return "Restoranimizda hali aktiv buyurtmalar yo'q"


print("Taomlar va ular ustidagi amallar boshlandi...\n")
osh = MenuItem("Osh",28000)
shorva = MenuItem("Shorva",25000)
shashlik_oddiy = MenuItem("Shashlik",8000)
somsa_tovuqli = MenuItem("Somsa tovuqli",8000)
somsa_goshtli = MenuItem("Somsa go'shtli",12000)
non = MenuItem("Non",5000)
choy_limonli = MenuItem("Limonli choy",8000)
kok_choy = MenuItem("Ko'k choy",5000)
shashlik_oddiy.make_unavailable()

print("\nTaomlar va ular ustidagi amallar tugadi...\n")

print("Kassir va ular ustidagi amalllar boshlandi...\n")
kassir_xazratbek = Kassir("Xazratbek")
kassir_asror = Kassir("Asror")
print("Kassir va ular ustidagi amalllar tugadi...\n")

print("Buyurtma va ular ustidagi ammalar boshlandi...\n")

buyurtma_1 = Order(OrderStatus.NEW)
print(buyurtma_1.add_item(osh))
print(buyurtma_1.add_item(somsa_goshtli))
print(buyurtma_1.add_item(choy_limonli))
print(buyurtma_1.add_item(kok_choy))
print(buyurtma_1.add_item(non))
print(buyurtma_1.add_item(non))
print(buyurtma_1.remove_item(kok_choy))
print(buyurtma_1.orders)
# print(buyurtma_1.get_order_count())
print(buyurtma_1.change_status(OrderStatus.COOKING))
print(buyurtma_1.change_status(OrderStatus.DONE))
print(f"Buyurtmangiz uchun to'lov: {buyurtma_1.calculate_price()}")
print(kassir_xazratbek.accept_payment(50000,buyurtma_1))
kassir_xazratbek.print_receipt(buyurtma_1)
print("Buyurtma va ular ustidagi ammalar tugadi...\n")
print(buyurtma_1.get_order_statuses_history())

xazratbek_restorani = Restoran()
print(xazratbek_restorani.add_menu_item(osh))
print(xazratbek_restorani.add_menu_item(somsa_goshtli))
print(xazratbek_restorani.add_menu_item(somsa_tovuqli))
print(xazratbek_restorani.add_menu_item(choy_limonli))
print(xazratbek_restorani.add_menu_item(kok_choy))
print(xazratbek_restorani.add_menu_item(non))

print(xazratbek_restorani.show_menu())
print("Restoranimizdagi aktiv buyurtmalar: \n")
print(xazratbek_restorani.create_order(osh))
print(xazratbek_restorani.create_order(somsa_goshtli))
print(xazratbek_restorani.create_order(somsa_tovuqli))
print(xazratbek_restorani.create_order(choy_limonli))
print(xazratbek_restorani.create_order(kok_choy))
print(xazratbek_restorani.create_order(non))
