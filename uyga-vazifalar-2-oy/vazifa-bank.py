# TZ-2: BANK HISOB TIZIMI
# ==============================

# Vazifa:
# Bankdagi mijoz va uning hisob raqamini boshqaruvchi dastur yozish.
# Dastur OOP asosida bo‘lishi shart.

# --------------------------------
# 1. BankAccount class
# --------------------------------
# Atributlar:
# - account_number : hisob raqami
# - balance        : balans (boshlang‘ich 0)

# Metodlar:
# - deposit(amount)
#   Berilgan miqdorni balansga qo‘shsin.

# - withdraw(amount)
#   Agar balans yetarli bo‘lsa:
#     - pul yechilsin
#   Aks holda:
#     - "Balans yetarli emas" degan xabar chiqsin.

# - show_balance()
#   Joriy balansni ekranga chiqarsin.

# --------------------------------
# 2. Client class
# --------------------------------
# Atributlar:
# - name    : mijoz ismi
# - account : BankAccount obyekti

# Metodlar:
# - show_info()
#   Mijoz ismi, hisob raqami va balansni chiqarib bersin.

# --------------------------------
# Classlar o‘rtasidagi bog‘lanish:
# --------------------------------
# - Client class ichida 1 ta BankAccount obyekti bo‘ladi

from datetime import datetime
from uuid import uuid4


class Transaction:
    def __init__(
        self,
        *,
        account_id: str,
        client_id: str,
        amount: float,
        currency: str,
        transaction_type: str,   # DEPOSIT | WITHDRAW | TRANSFER | REVERSAL
    ):
        self.transaction_id = str(uuid4())
        self.account_id = account_id
        self.client_id = client_id
        self.amount = amount
        self.currency = currency
        self.transaction_type = transaction_type
        self.status = "PENDING"          # PENDING | SUCCESS | FAILED | CANCELLED
        self.failure_reason = None
        self.created_at = datetime.now()
        self.completed_at = None

    @staticmethod
    def create(account, client_id, amount, transaction_type,currency="UZS"):
        transaction = Transaction(account_id=account.account_number,client_id=client_id,currency=currency,amount=amount,transaction_type=transaction_type)
        if amount < 0:
            transaction.status = "FAILED"
            transaction.failure_reason = "Manfiy qiymat taqiqlanadi!"
            transaction.completed_at = datetime.now()

        else:
            transaction.status = "SUCCESS"
            transaction.completed_at = datetime.now()

        return transaction

class BankAccount:
    def __init__(self, privacy_code, currency="UZS"):
        self.__account_id = str(uuid4())
        self.account_number = str(uuid4().int)[:16]
        self.__balance = 0.0
        self.currency = currency
        self.is_active = True
        self.is_blocked = False
        self.transaction_history = []
        self.bank_account_created_at = datetime.now()
        self.bank_account_closed_at = None
        self.privacy_code = privacy_code

    def check_privacy_code(self, privacy_code):
        return self.privacy_code == privacy_code

    def set_privacy_code(self, new_privacy_code: int):
        data = {}
        if self.privacy_code == new_privacy_code:
            data['reject_reason'] = "Iltimos eski parolni qayta kiritmang"
            data['is_rejected'] = True
            return data

        if len(str(new_privacy_code)) < 4 or len(str(new_privacy_code)) > 10:
            data['reject_reason'] = "Parol uzunligi kamida 4-ta, maksimum 10-ta belgidan iborat bo'lishi kerak"
            data['is_rejected'] = True
            return data

        self.privacy_code = new_privacy_code
        data['reject_reason'] = None
        data['is_rejected'] = False
        return data

    def get_account_currency(self):
        return self.currency

    def get_account_number(self,privacy_code):
        return self.account_number if self.check_privacy_code(privacy_code) else None

    def show_balance(self, privacy_code):
        return self.__balance if self.check_privacy_code(privacy_code) else None


    def get_account_id(self, privacy_code):
        return self.__account_id if self.check_privacy_code(privacy_code) else None

    def deposit(self, summa, privacy_code, client_id=None):
        if self.check_privacy_code(privacy_code) and summa > 0:
            self.__balance += summa
            transaction = Transaction.create(self, client_id, summa, "DEPOSIT")
            self.transaction_history.append(transaction)
            return True
        return False

    def confirm_money_from_another_account(self, summa,client_id=None):
        self.__balance += summa
        transaction = Transaction.create(self, client_id, summa, "DEPOSIT")
        self.transaction_history.append(transaction)
        return True

    def withdraw(self, summa, privacy_code, client_id=None):
        if self.check_privacy_code(privacy_code) and summa <= self.__balance:
            self.__balance -= summa
            transaction = Transaction.create(self, client_id, summa, "WITHDRAW")
            self.transaction_history.append(transaction)
            return True
        return False


    def get_detail_info(self,account_number, privacy_code):
        if self.account_number == account_number and self.check_privacy_code(privacy_code):
            closed_info = f"Bank account yopilgan sana: {self.bank_account_closed_at}" if self.bank_account_closed_at else "Bank akkaunt yopilmagan"
            return f"Account ID: {self.__account_id}\nAccount number: {self.account_number}\nBalance: {self.__balance}\nCurrency: {self.currency}\nBank account created at: {self.bank_account_created_at}\nStatus: {closed_info}"


    def get_account_status(self):
        return self.is_active

    def close_bank_account(self,privacy_code):
        data = {}
        if self.privacy_code == privacy_code:
            self.bank_account_closed_at  = datetime.now()
            self.is_active = False
            self.is_blocked = True
            data['reject_reason'] = None
            data['is_rejected'] = False
            return data
        data['reject_reason'] = "Xavfsizlik paroli notog'ri"
        data['is_rejected'] = True
        return data

    def transfer_to(self,target_account,amount,privacy_code):
        data = {}
        if self.check_privacy_code(privacy_code) and (amount > 0 and amount <= self.__balance):
            target_account.confirm_money_from_another_account(amount)
            self.__balance -= amount
            data['is_rejected'] = False
            data['reject_reason'] = None

            return data

        data['is_rejected'] = True
        data['reject_reason'] = "Parol yoki summa notog'ri kiritildi iltimos tekshirib qaytadan kiriting!"

        return data

class Client:
    def __init__(
        self,
        name: str,
        account,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
    ):
        self.client_id = str(uuid4())
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.is_verified = False
        self.is_active = True
        self.account = account
        self.client_created_at = datetime.now()

    def get_client_name(self):
        return self.name

    def show_info(self,privacy_code):
        return f"{self.account.get_detail_info(self.account.account_number, privacy_code)}\nIsm: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nAdress: {self.address if self.address is not None else 'Mavjud emas'}\nClient ID: {self.client_id}\nCreated at: {self.client_created_at}"

    def get_my_balance(self, privacy_code):
        balance = self.account.show_balance(privacy_code)
        if balance is not None:
            return balance
        return "Iltimos tog'ri parol kiriting!"

    def client_deposit(self,summa, privacy_code):
        deposit = self.account.deposit(summa, privacy_code, self.client_id)

        if deposit:
            return f"Xurmatli: {self.name} {summa}-balansingizga muvaffaqiyatli qo'shildi.\nBalansdagi qoldiq: {self.get_my_balance(privacy_code)}"
        return "Parol yoki summa notog'ri kiritildi iltimos ma'lumotlarni tekshirib qaytadan kiriting!\nMinimum deposit 0-dan katta bo'lishi kerak"

    def client_withdraw(self, summa, privacy_code):
        withdraw = self.account.withdraw(summa, privacy_code, self.client_id)

        if withdraw:
            return f"Xurmatli: {self.name} balansingizdan muvaffaqiyatli {summa} pul yechildi.\nBalansdagi qoldiq: {self.get_my_balance(privacy_code)}"
        return "Parol yoki summa notog'ri iltimos ma'lumotlarni tekshirib qaytadan kiriting!\nPul yechishda balansingizdagi summadan ortiq pul yecha olmaysiz!"

    def client_set_privacy_code(self,new_privacy_code):
        result = self.account.set_privacy_code(new_privacy_code)

        if result['is_rejected']:
            return result['reject_reason']
        return "Yangi parol muvaffaqiyatli o'rnatildi"


    def get_my_account_number(self,privacy_code):
        result = self.account.get_account_number(privacy_code)
        if result is not None:
            return result
        return "Iltimos xavfsizlik kodini tog'ri kiriting!"

    def client_close_bank_account(self,privacy_code):
        result = self.account.close_bank_account(privacy_code)
        if result['is_rejected']:
            return result['reject_reason']

        return f"Bank aaccount muvaffaqiyatli yopildi\n{self.account.get_detail_info(self.account.account_number,privacy_code)}"

    def client_transfer_money(self,target_account, amount,privacy_code):
        data = self.account.transfer_to(target_account,amount,privacy_code)

        if data['is_rejected']:
            return data['reject_reason']

        return f"Pul muvaffaqiyatli {target_account.account_number}-ga yuborildi\nSumma: {amount}\nBalans qoldiq: {self.get_my_balance(privacy_code)}"

print("Bank accountlari yaratish boshlandi...\n")
acc1 = BankAccount(privacy_code=1234)
acc2 = BankAccount(privacy_code=5678)
print("Bank accountlari yaratish tugadi...\n")


print("Client akkaunt yaratish boshlandi...\n")
client1 = Client(name="Ali", account=acc1, email="ali@example.com", phone="+998901234567",address="Andijon Viloyati")
client2 = Client(name="Vali", account=acc2, email="vali@example.com", phone="+998909876543")
print("Client accountlari yaratish tugadi...\n")

print("\nClientlar bank hisoblariga deposit qo'yish boshlandi...")
print(client1.client_deposit(5000, 1234))
print(client2.client_deposit(3000, 5678))
print("Clientlar bank hisoblariga deposit qo'yish tugadi...\n")


print("\nClientlar bank hisoblaridan pul yechish boshlandi...")
print(client1.client_withdraw(2000, 1234))
print(client2.client_withdraw(500, 5678))
print("Clientlar bank hisoblaridan pul yechish boshlandi...\n")

print("\nClientlar aro pul o'tkazish boshlandi...")
print(client1.client_transfer_money(acc2, 1000, 1234))
print("Clientlar aro pul o'tkazish tugadi...\n")

print("Client1 privacy code o'zgartirish:", client1.client_set_privacy_code(4321))
print("Client2 privacy code o'zgartirish:", client2.client_set_privacy_code(8765))

print("Client1 account number:", client1.get_my_account_number(4321))
print("Client2 account number:", client2.get_my_account_number(8765))

print("\nClient1 account info:\n", client1.show_info(4321))
print("\nClient2 account info:\n", client2.show_info(8765))

print("Client1 balance:", client1.get_my_balance(4321))
print("Client2 balance:", client2.get_my_balance(8765))

print("Client1 account close:", client1.client_close_bank_account(4321))
print("Client2 account close:", client2.client_close_bank_account(8765))

print("\nClient1 transaction history:")
for tx in acc1.transaction_history:
    print(f"\nID: {tx.transaction_id}, Type: {tx.transaction_type}, Amount: {tx.amount}, Status: {tx.status}, Completed at: {tx.completed_at}")

print("\nClient2 transaction history:")
for tx in acc2.transaction_history:
    print(f"\nID: {tx.transaction_id}, Type: {tx.transaction_type}, Amount: {tx.amount}, Status: {tx.status}, Completed at: {tx.completed_at}")
