from abc import ABC, abstractmethod
from datetime import datetime
import time
import random


# =========================
# ABSTRACT BASE CLASS
# =========================

class PaymentMethod(ABC):
    def __init__(self, min_amount: float):
        self.min_amount = min_amount

    def validate_amount(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount < self.min_amount:
            raise ValueError(f"Minimum amount is {self.min_amount}")

    @abstractmethod
    def process(self, amount: float) -> bool:
        """
        Process payment.
        Must return True if success, False if failed.
        """
        pass


# =========================
# CREDIT CARD PAYMENT
# =========================

class CreditCardPayment(PaymentMethod):
    def __init__(
        self,
        min_amount: float,
        card_holder: str,
        card_number: str,
        expire_date: datetime,
    ):
        super().__init__(min_amount)
        self.card_holder = card_holder
        self.card_number = card_number
        self.expire_date = expire_date

    def _validate_card(self) -> None:
        if not self.card_number.isdigit() or len(self.card_number) != 16:
            raise ValueError("Invalid card number")

        if self.expire_date <= datetime.now():
            raise ValueError("Card is expired")

    def process(self, amount: float) -> bool:
        # common validation (from base class)
        self.validate_amount(amount)

        # card-specific validation
        self._validate_card()

        print("🔍 Validating credit card...")
        time.sleep(random.uniform(1, 2))

        print(f"💳 Charged {amount} from credit card")
        return True


# =========================
# BANK TRANSFER PAYMENT
# =========================

class BankTransferPayment(PaymentMethod):
    def __init__(self, min_amount: float, account_number: str, bank_name: str):
        super().__init__(min_amount)
        self.account_number = account_number
        self.bank_name = bank_name

    def _validate_account(self) -> None:
        if not self.account_number.isdigit():
            raise ValueError("Invalid bank account number")

    def process(self, amount: float) -> bool:
        # common validation (from base class)
        self.validate_amount(amount)

        # bank-specific validation
        self._validate_account()

        print(f"🏦 Sending transfer request to {self.bank_name}...")
        time.sleep(random.uniform(2, 3))

        print(f"✅ Bank transfer of {amount} completed")
        return True


# =========================
# SIMPLE TESTS (POLYMORPHISM)
# =========================

def run_payment(payment_method: PaymentMethod, amount: float):
    """
    Caller knows ONLY PaymentMethod.
    """
    result = payment_method.process(amount)
    print("RESULT:", result)


if __name__ == "__main__":
    credit_payment = CreditCardPayment(
        min_amount=1000,
        card_holder="Xazratbek",
        card_number="9860030172680750",
        expire_date=datetime(2026, 5, 1),
    )

    bank_payment = BankTransferPayment(
        min_amount=1000,
        account_number="1234567890",
        bank_name="Xazratbek Bank",
    )

    run_payment(credit_payment, 1500)
    print("-" * 40)
    run_payment(bank_payment, 2000)
