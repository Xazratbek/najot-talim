from collections import namedtuple

Car = namedtuple("Car", ["id", "name", "brand", "color", "price", "year"])

cars = []

def add_car():
    car_id = int(input("ID: "))
    name = input("Nomi: ")
    brand = input("Brand: ")
    color = input("Rangi: ")
    price = float(input("Narxi: "))
    year = int(input("Yili: "))

    car = Car(car_id, name, brand, color, price, year)
    cars.append(car)

    print("Mashina qo'shildi.")


def get_all_cars():
    for car in cars:
        print(car)


def update_car():
    car_id = int(input("Yangilash uchun ID kiriting: "))

    for i, car in enumerate(cars):
        if car.id == car_id:
            name = input("Yangi nomni kiriting: ")
            brand = input("Yangi brand nomini kiriting: ")
            color = input("Yangi rangni kiriting: ")
            price = float(input("Yangi narxni kiriting: "))
            year = int(input("Yangi mashina yilini kiriting: "))

            cars[i] = Car(car_id, name, brand, color, price, year)

            print("Mashina yangilandi.")
            return

    print("Mashina topilmadi.")


def delete_car():
    car_id = int(input("O'chirish uchun ID kiriting: "))

    for car in cars:
        if car.id == car_id:
            cars.remove(car)
            print("Mashina o'chirildi.")
            return

    print("Mashina topilmadi.")


while True:
    print("""
        1. Mashina qo'shish
        2. Mashinalarni ko'rsatish
        3. Mashinani yangilash
        4. Mashinani o'chirish
        0. Chiqish
        """)

    choice = input("Tanlang: ")

    if choice == "1":
        add_car()

    elif choice == "2":
        get_all_cars()

    elif choice == "3":
        update_car()

    elif choice == "4":
        delete_car()

    elif choice == "0":
        break

    else:
        print("Noto'g'ri tanlov")