# 1 — Sinflar & Instanslar (Class & Instance) — Boshlang‘ich

# TZ: UserProfile sinfi (in-memory). Maydonlar: username, email, balance. Metodlar: deposit(amount), withdraw(amount). withdraw balans yetmasa InsufficientFundsError tashlashi kerak.

# Detallar / qadamlar:

# Konstruktorda validatsiya: username/email format (eng oddiy regex yoki contains('@') yetadi).

# deposit — musbat son tekshiruvi, return yangi balans.

# withdraw — atomic bo‘lmasa ham unit testda ketma-ket chaqirish to‘g‘ri ishlashini tekshir.

# Qoida: hech qachon balance ni to‘g‘ridan-to‘g‘ri tashqaridan o‘zgartirishga ruxsat bermaymiz — private atribut (convention: _balance yoki __balance).

# OOP konseptlar: sinflar, instanslar, enkapsulyatsiya, istisnolar.

# Agar bunday narsalar noma’lum bo‘lsa (izoh):

# Enkapsulyatsiya — sinf ichidagi holatni (state) bevosita tashqaridan o‘zgartirishni cheklash.

# Exception class — class InsufficientFundsError(Exception): ... yozish — bundan keyin test va caller try/except bilan tutadi.

# Mentor note: oddiy, lekin hamma narsa shu yerda boshlanadi. Agar bu vazifada testsiz boshlasang, keyingilari qiyin bo‘ladi.

class InsufficientFundsError(Exception):
    pass

class UserProfile:
    def __init__(self, username, email):
        if "@" in email:
            self.username = username
            self.email = email
            self.__balance = 0

        else:
            raise ValueError("Email is not contains @")

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Musbat son yoki 0 kiritish mumkin emas")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Manfiy va 0 sonini kiritish mumkin emas")

        if amount <= self.__balance:
            self.__balance -= amount
            return self.__balance
        else:
            raise InsufficientFundsError("Mablag' yetarli emas!")

user_1 = UserProfile("@xazratbek","xazratbek123@gmail.com")
print(user_1.balance)
print(user_1.deposit(15.0))
print(user_1.balance)
print(user_1.withdraw(10))
print(user_1.balance)