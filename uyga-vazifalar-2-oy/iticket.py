from enum import Enum
from typing import Optional
from uuid import uuid4
from datetime import datetime
import random
import time
import sys
from rich.console import Console
from rich.progress import Progress


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class PaymentType(Enum):
    CARD = "card"
    NAQD_PUL = "naqd pul"
    CLICK = "click"
    PAYME = "payme"


def ticket_generate_animation():
    with Progress() as progress:
        task = progress.add_task("[cyan]Chiptangiz chop etilmoqda...[/]", total=None)
        for _ in range(77):
            progress.update(task, advance=0.6)
            time.sleep(0.1)

def loading_animation():
    animation = "|/-\\"
    for i in range(30):
        sys.stdout.write('\r' + animation[i % len(animation)] + " To'lov amalga oshirilmoqda...")
        sys.stdout.flush()
        time.sleep(0.1)

def payment_process_animation(go_to_payment: bool):
    if go_to_payment:
        console = Console()
        with console.status("[bold green]To'lov tekshirish boshlandi...") as status:
            time.sleep(2)
            console.log(f"To'lov tekshirilmoqda...")
            status.update(status=f"[bold blue]Pullar hisoblanmoqda...", spinner="clock")
            time.sleep(2)

        console.print("[bold cyan]Tekshirish yakuniga yetdi to'lovga o'ting")

    else:
        console = Console()
        with console.status("[bold green]To'lov tekshirish boshlandi...") as status:
            time.sleep(2)
            console.log(f"To'lov tekshirilmoqda...")
            status.update(status=f"[bold blue]Pullar hisoblanmoqda...", spinner="clock")
            time.sleep(2)

        console.print("[bold cyan]Buyurtma uchun berilgan summa yetarli emas, iltimos balansizgizni tekshirib qaytadan urunib ko'ring")


def payment_animation_using_rich(amount,payment_type, payment_status: Optional[PaymentStatus] = None):
    console = Console()

    if payment_status.value == "success":
        with console.status("[bold green]To'lov amalga oshirilmoqda...") as status:
            if payment_type == PaymentType.NAQD_PUL:
                time.sleep(2)
                console.log(f"Pullar hisoblanmoqda...")

                status.update(status=f"[bold blue]{amount}-so'mga bilet 🤨...", spinner="moon")
                time.sleep(2)

            else:
                time.sleep(2)
                console.log(f"{payment_type.value.title()}-so'rov yuborilmoqda...")

                status.update(status=f"[bold blue]{amount}-so'mga bilet 🤨...", spinner="moon")
                time.sleep(2)

        console.print("[bold cyan]To'lov muvaffaqiyatli amalga oshdi, xaridingiz uchun rahmat 😊")

    else:
        with console.status("[bold green]To'lov amalga oshirilmoqda...") as status:
            time.sleep(2)
            console.log(f"{payment_type.value.title()}-so'rov yuborilmoqda...")

            status.update(status=f"[bold blue]{amount}-so'mga bilet 🤨...", spinner="clock")
            time.sleep(2)

        console.print("[bold cyan]To'lovda xatolik yuz berdi, iltimos balansizgizni tekshirib qaytadan urunib ko'ring 🙂")

class TicketNotFoundError(Exception):
    pass

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class User:
    def __init__(self,ism: str,familiya: str,phone: int,role: UserRole, adress: Optional[str]):
        self.id = uuid4()
        self.ism = ism
        self.familiya = familiya
        self.phone = phone
        self.role = role
        self.address = adress
        self.__is_active = True

    def __str__(self):
        address = f"Yashash manzili:  + {str(self.address) if self.address is not None else 'Mavjud emas'}"
        return f"ID: {self.id} | Foydalanuvchi: {self.ism.title()}-{self.familiya.title()} | Telefono raqami: {self.phone} | Role: {self.role.value} | Adress: {address}"

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self,new_activity):
        if self.__is_active != new_activity:
            self.__is_active = new_activity
        return "Hech narsa o'zgarmadi"

    def get_name(self):
        return self.ism

    def change_status(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True

    def view_events(self, ticket_system: TicketSystem):
        data = []
        for event in ticket_system.events.values():
            if event.is_active:
                data.append(event)

        return data

    def view_orders(self,ticket_system: "TicketSystem"):
        data = []
        for order in ticket_system.orders.values():
            if order.user.id == self.id:
                data.append(order)

        return data

class Event:
    def __init__(self,title: str,description: str,date_time: datetime, hall: Hall):
        self.id = uuid4()
        self.title = title
        self.description = description
        self.date_time = date_time
        self.hall = hall
        self.__is_active = True

    def __str__(self):
        return f"Tadbir: {self.title} | Tadbir haqida: {self.description} | Tadbir bo'lib o'tadi: {self.hall.name} | Sanasi: {self.date_time.strftime("%c")}"

    @property
    def is_active(self):
        return self.__is_active

    def get_price(self,orindiq_id):
        for orindiq in self.hall.seats:
            if orindiq.id == orindiq_id:
                return orindiq.price
        return None

    def is_available(self):
        today = datetime.now()
        if self.__is_active and self.date_time > today:
            return True
        else:
            return False

class Hall:
    def __init__(self,name: str):
        self.id = random.randint(1,1000)
        self.name = name
        self.seats = []

    def __str__(self):

        return f"ID: {self.id} | Zall: {self.name} | Zaldagi umumiy o'rindiqlar soni: {len(self.seats)} | Bo'sh joylar soni: {len(self.get_free_seats())} | Band joylar soni: {len(self.get_busy_seats())}"

    def add_seats(self, orindiq: Orindiq):
        self.seats.append(orindiq)

    def get_seat_by_id(self,seat_id):
        for seat in self.seats:
            if seat.id == seat_id:
                return seat
        return None

    def get_free_seats(self):
        free_seats = []
        for seat in self.seats:
            if seat.is_booked == False:
                free_seats.append(seat)

        return free_seats

    def get_busy_seats(self):
        busy_seats = []
        for seat in self.seats:
            if seat.is_booked == True:
                busy_seats.append(seat)

        return busy_seats


class Orindiq:
    def __init__(self,qator,joy):
        self.id = random.randint(1,10000)
        self.qator = qator
        self.joy = joy
        self.__price = 0
        self.is_booked = False

    def __str__(self):
        return f"ID: {self.id} | O'rindiq: {self.qator}-qator {self.joy}-joyda joylashgan | Narxi: {self.__price} | {'Band' if self.is_booked else 'Bo\'sh'}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,new_price):
        if new_price > 0:
            self.__price = new_price

    def book(self):
        if self.is_booked:
            raise Exception("Joy allaqachon band qilingan")
        else:
            self.is_booked = True

    def release(self):
        if self.is_booked:
            self.is_booked = False
        else:
            raise Exception("Joy allaqachon bo'sh")

    def is_available(self):
        return not self.is_booked

class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    CANCELED = "canceled"

class Order:
    def __init__(self,user: User, event: Event, status: OrderStatus):
        self.id = uuid4()
        self.user = user
        self.event = event
        self.orindiqlar = []
        self.status = status
        self.total_price = 0

    def __str__(self):
        return f"Zakaz id: {self.id} | Zakaz beruvchi: {self.user.ism} | Tadbir: {self.event.title} | Status: {self.status.value.title()}"

    def add_orindiq(self,*orindiqlar):
        for orindiq in orindiqlar:
            if self.status != OrderStatus.CREATED:
                raise Exception("Buyurtma yaratilmagan!")

            if orindiq.is_booked:
                raise Exception("Tanlangan joy band qilingan")

            if orindiq not in self.orindiqlar:
                if orindiq in self.event.hall.seats:
                    self.orindiqlar.append(orindiq)
                else:
                    raise Exception(f"O'rindiq: {orindiq.id}, bu o'tayotgan tadbirga tegishli emas")
            else:
                raise Exception(f"Orindiq {orindiq.id}, allaqachon buyurtma ro'yxatiga qo'shilgan")

        return self.orindiqlar

    def calculate_total(self):
        self.total_price = sum(seat.price for seat in self.orindiqlar)
        return self.total_price

    def confirm(self):
        try:
            for orindiq in self.orindiqlar:
                orindiq.book()

        except Exception as e:
            print(f"Exception: {e}")

    def cancel(self):
        try:
            for orindiq in self.orindiqlar:
                orindiq.release()

        except Exception as e:
            print(f"Exception: {e}")

        finally:
            self.status = OrderStatus.CANCELED

class Payment:
    def __init__(self, order: Order, amount: int, status: PaymentStatus, payment_type: PaymentType):
        self.id = uuid4()
        self.order = order
        self.amount = amount
        self.status = status
        self.payment_type = payment_type

    def __str__(self):
        return f"To'lov: {self.id} | Summa: {self.amount} | Xolati: {self.status.value} | To'lov turi: {self.payment_type.value}"

    def process(self):
        if self.amount == self.order.calculate_total():
            self.success()
            return PaymentStatus.SUCCESS

        else:
            self.fail()
            return PaymentStatus.FAILED

    def fail(self):
        self.status = PaymentStatus.FAILED
        payment_animation_using_rich(self.amount,self.payment_type,self.status)
        self.order.cancel()
        self.order.status = OrderStatus.CANCELED

    def success(self):
        self.status = PaymentStatus.SUCCESS
        payment_animation_using_rich(self.amount,self.payment_type,self.status)
        self.order.confirm()
        self.order.status = OrderStatus.PAID

class Ticket:
    def __init__(self, event: Event, seat_info: Orindiq, price, user: User):
        self.id = uuid4()
        self.ticket_number = random.randint(1,10000)
        self.event = event
        self.seat_info = seat_info
        self.price = price
        self.user = user

    def __str__(self):
        return f"Chipta: {self.ticket_number} | Tadbir nomi: {self.event.title} | Jo'y: {self.seat_info} | Chipta egasi: {self.user.ism}"

    def get_ticket(self):
        today = datetime.now()
        data = "Sizning chiptangiz: "
        data += f"Chipta ID: {self.id}\n{self.ticket_number}\nChipta raqami: {self.ticket_number}\nTadbir nomi: {self.event.title}\nJoyingiz: {self.seat_info}\nChipta narxi: {self.price}\nChipta egasi: {self.user.ism}\nSana: {today}"
        return data

class TicketSystem:
    def __init__(self):
        self.users = {}
        self.events =  {}
        self.orders =   {}
        self.payments = {}

    def add_event(self,event):
        self.events[event.id] = event

    def register_user(self,user: User):
        self.users[user.id] = user

    def add_payment(self,payment: Payment):
        self.payments[payment.id] = payment

    def login(self,user_id, phone):
        user_data = self.users.get(user_id)
        if phone ==  user_data.phone:
            user_data.is_active = True
            return "User tizimga kirdi"
        else:
            user_data.is_active = False
            return "Notog'ri telefon raqam yoki id kiritildi iltimos tekshirib qaytadan kiriting..."

    def create_order(self,user: User, event_id: str, seat_ids: list[str]):
        if event_id not in self.events:
            raise ValueError("Event topilmadi")

        event = self.events[event_id]


        tanlangan_joylar = []
        for seat_id in seat_ids:
            seat = event.hall.get_seat_by_id(seat_id)
            if seat is None:
                raise ValueError(f"{seat_id}-id si bilan mavjud joy topilmadi")

            if not seat.is_available():
                raise ValueError({f"{seat_id}-idlik joy band"})

            tanlangan_joylar.append(seat)

        order = Order(user=user,event=event, status=OrderStatus.CREATED)
        order.add_orindiq(*tanlangan_joylar)

        order.calculate_total()
        self.orders[order.id] = order

        return order

    def pay_order(self,order_id,payment_type: PaymentType, amount: int):
        order = self.orders.get(order_id)
        if not order:
            raise ValueError("Order topilmadi")

        order_payment = Payment(order,amount,PaymentStatus.PENDING,payment_type)
        order_payment.process()
        self.payments[order_payment.id] = order_payment

        return order_payment


    def print_ticket(self, payment_id):
        if payment_id not in self.payments:
            raise ValueError("Payment topilmadi")

        payment = self.payments[payment_id]
        if payment.status != PaymentStatus.SUCCESS:
            raise ValueError("To'lov muvaffaqiyatli emas, chipta chiqarib bo'lmaydi")

        order = payment.order
        if order.status != OrderStatus.PAID:
            raise ValueError("Order hali PAID holatida emas")

        tickets = []

        for seat in order.orindiqlar:
            ticket = Ticket(
                event=order.event,
                seat_info=seat,
                price=seat.price,
                user=order.user
            )
            tickets.append(ticket)

        ticket_generate_animation()
        for ticket in tickets:
            print(ticket.get_ticket())

        return tickets

    def run(self):
        pass

system = TicketSystem()

user1 = User(
    ism="Xazratbek",
    familiya="Turdaliyev",
    phone=998939498849,
    role=UserRole.USER,
    adress="Andijon"
)
system.register_user(user1)

hall = Hall("Humo Arena")
print(hall)
seat1 = Orindiq(qator=1, joy=1)
seat2 = Orindiq(qator=1, joy=2)
seat3 = Orindiq(qator=1, joy=3)
seat4 = Orindiq(qator=1, joy=4)
seat5 = Orindiq(qator=1, joy=5)
seat5 = Orindiq(qator=1, joy=5)
seat6 = Orindiq(qator=1, joy=6)
seat7 = Orindiq(qator=1, joy=7)
seat8 = Orindiq(qator=1, joy=8)
seat9 = Orindiq(qator=1, joy=9)
seat10 = Orindiq(qator=1, joy=10)
seat11 = Orindiq(qator=1, joy=11)
seat12 = Orindiq(qator=1, joy=12)
print(f"O'rindiq 1: {seat1}")
seat1.price = 100_000
seat2.price = 100_000
seat3.price = 150_000
seat4.price = 80_000
seat5.price = 120_000
seat6.price = 140_000
seat7.price = 135_000
seat8.price = 122_000
seat9.price = 150_000
seat10.price = 150_00
seat11.price = 90_000
seat12.price = 144_000

print(f"\n12-joy xolati: {'Bo\'sh' if seat12.is_available() else 'Bo\'sh emas'}")
print(f"\n12-joy narxi: {seat12.price}\n")

hall.add_seats(seat1)
hall.add_seats(seat2)
hall.add_seats(seat3)
hall.add_seats(seat4)
hall.add_seats(seat5)
hall.add_seats(seat6)
hall.add_seats(seat7)
hall.add_seats(seat8)
hall.add_seats(seat9)
hall.add_seats(seat10)
hall.add_seats(seat11)
hall.add_seats(seat12)

print(hall)

print(f"\n{hall.name}-zalidagi band joylar: {[data.__str__() for data in hall.get_busy_seats()]}\n")
print(f"\n{hall.name}-zalidagi bo'sh joylar: \n")
for data in hall.get_free_seats():
    print(data)


event = Event(
    title="Xamdam Sobirov",
    description="Jonli Ijro",
    date_time=datetime(2026, 5, 1, 20, 0),
    hall=hall
)

print(f"\n{event.title}-tadbirining narxi: {event.get_price(seat1.id)}, tadbir haqida ma'lumot: {event.description}\n")

system.add_event(event)

events = user1.view_events(system)
for event in events:
    print(event)

order = system.create_order(
    user=user1,
    event_id=event.id,
    seat_ids=[seat1.id,seat10.id]
)
print(f"\n{user1.ism}-ning buyurtmalari:")
orders = user1.view_orders(system)
for order in orders:
    print(order)

# print(order.id)
# print(order.total_price)

# try:
#     system.create_order(
#         user=user1,
#         event_id=event.id,
#         seat_ids=[seat6.id]
#     )
# except Exception as e:
#     print(e)

payment_fail = system.pay_order(
    order_id=order.id,
    payment_type=PaymentType.CARD,
    amount=50_000
)

# print(payment_fail.status.value)
# print(order.status.value)

order2 = system.create_order(
    user=user1,
    event_id=event.id,
    seat_ids=[seat3.id]
)

payment_success = system.pay_order(
    order_id=order2.id,
    payment_type=PaymentType.CLICK,
    amount=150_000
)

# print(payment_success.status.value)
# print(order2.status.value)
tickets = system.print_ticket(payment_success.id)

print(hall)