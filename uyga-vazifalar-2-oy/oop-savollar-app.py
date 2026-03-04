import random

class Question:
    def __init__(self, savol, variantlar, togri):
        self.savol = savol
        self.variantlar = variantlar
        self.togri = togri

    def show(self):
        print("\n" + self.savol)
        for key, value in self.variantlar.items():
            print(f"{key}) {value}")

    def check(self, javob):
        return javob.upper() == self.togri


class Quiz:
    def __init__(self, savollar):
        self.savollar = savollar
        self.score = 0

    def start(self):
        random.shuffle(self.savollar)

        for savol in self.savollar:
            savol.show()
            javob = input("Javobingiz (A/B/C/D): ")

            if savol.check(javob):
                print("✅ To‘g‘ri")
                self.score += 1
            else:
                print(f"❌ Noto‘g‘ri. To‘g‘ri javob: {savol.togri}")

        print(f"\nNatija: {self.score} / {len(self.savollar)}")


savollar = [
    Question("OOP nima?",
        {"A":"Oddiy dasturlash","B":"Obyektga yo‘naltirilgan dasturlash","C":"Web dasturlash","D":"Grafik dasturlash"},"B"),

    Question("OOP nechta tamoyildan iborat?",
        {"A":"2","B":"3","C":"4","D":"5"},"C"),

    Question("Class nima?",
        {"A":"Funksiya","B":"O‘zgaruvchi","C":"Shablon","D":"Modul"},"C"),

    Question("Object nima?",
        {"A":"Class nusxasi","B":"Funksiya","C":"Sikl","D":"Modul"},"A"),

    Question("Atribut nima?",
        {"A":"Funksiya","B":"O‘zgaruvchi","C":"Sikl","D":"Kutubxona"},"B"),

    Question("Method nima?",
        {"A":"Class ichidagi funksiya","B":"Oddiy funksiya","C":"Modul","D":"Sikl"},"A"),

    Question("__init__ qachon ishlaydi?",
        {"A":"Class ochilganda","B":"Object yaratilganda","C":"Kod tugaganda","D":"Har doim"},"B"),

    Question("self nima?",
        {"A":"Class","B":"Object","C":"Objectga murojaat","D":"Funksiya"},"C"),

    Question("Encapsulation nima?",
        {"A":"Meros olish","B":"Ma’lumot yashirish","C":"Ko‘p shakllilik","D":"Shablon"},"B"),

    Question("Inheritance nima?",
        {"A":"Yashirish","B":"Meros olish","C":"Xatolik","D":"Sikl"},"B"),

    Question("Parent class nima?",
        {"A":"Meros oluvchi","B":"Meros beruvchi","C":"Object","D":"Funksiya"},"B"),

    Question("Child class nima?",
        {"A":"Meros beruvchi","B":"Meros oluvchi","C":"Asosiy","D":"Oddiy"},"B"),

    Question("Polymorphism nima?",
        {"A":"Bir xil metod","B":"Ko‘p shakllilik","C":"Yashirish","D":"Object"},"B"),

    Question("Abstraction nima?",
        {"A":"Detallarni yashirish","B":"Object yaratish","C":"Sikl","D":"Funksiya"},"A"),

    Question("Abstrakt class nima?",
        {"A":"Object yaratiladi","B":"Object yaratilmaydi","C":"Funksiya","D":"Modul"},"B"),

    Question("@abstractmethod nima?",
        {"A":"Ixtiyoriy","B":"Majburiy method","C":"Oddiy method","D":"Xato"},"B"),

    Question("super() nima uchun?",
        {"A":"Child chaqirish","B":"Parent method chaqirish","C":"Object yaratish","D":"Sikl"},"B"),

    Question("Instance atribut nima?",
        {"A":"Umumiy","B":"Objectga tegishli","C":"Classga","D":"Global"},"B"),

    Question("Class atribut nima?",
        {"A":"Objectga","B":"Hamma objectga umumiy","C":"Local","D":"Private"},"B"),

    Question("Private atribut qanday yoziladi?",
        {"A":"_nom","B":"__nom","C":"nom","D":"#nom"},"B"),

    Question("Method va function farqi?",
        {"A":"Farqi yo‘q","B":"Method class ichida","C":"Function class ichida","D":"Ikkalasi bir xil"},"B"),

    Question("Bitta classdan nechta object?",
        {"A":"1","B":"2","C":"10","D":"Cheksiz"},"D"),

    Question("Class ichida method bo‘lishi shartmi?",
        {"A":"Ha","B":"Yo‘q","C":"Ba’zan","D":"Noma’lum"},"B"),

    Question("OOP nima uchun kerak?",
        {"A":"Chiroyli kod","B":"Tartibli kod","C":"Qayta ishlatish","D":"Hammasi"},"D"),

    Question("Object qanday yaratiladi?",
        {"A":"class bilan","B":"funksiya bilan","C":"Class() bilan","D":"loop bilan"},"C"),

    Question("self qayerda yoziladi?",
        {"A":"Class tashqarisida","B":"Method ichida","C":"Funksiya tashqarisida","D":"Main’da"},"B"),

    Question("Inheritance nimani kamaytiradi?",
        {"A":"Xatoni","B":"Kod takrorini","C":"Tezlikni","D":"Objectni"},"B"),

    Question("Polymorphism qayerda ko‘p?",
        {"A":"Encapsulation","B":"Inheritance","C":"Loop","D":"List"},"B"),

    Question("Class ichidagi o‘zgaruvchi?",
        {"A":"Method","B":"Atribut","C":"Object","D":"Function"},"B"),

    Question("OOP qaysi dasturlash turi?",
        {"A":"Funksional","B":"Protsedurali","C":"Obyektga yo‘naltirilgan","D":"Grafik"},"C")
]

quiz = Quiz(savollar)
quiz.start()