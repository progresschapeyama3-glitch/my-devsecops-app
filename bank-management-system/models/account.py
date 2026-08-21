from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from models.customer import Customer
from models.transaction import Transaction


@dataclass
class BankAccount(ABC):
    account_number: str
    owner: Customer
    _balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)

    def __post_init__(self):
        if self._balance < 0:
            raise ValueError("Initial balance cannot be negative.")

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._validate_amount(amount)
        self._balance += amount
        self.transactions.append(
            Transaction("DEPOSIT", amount, "Money deposited")
        )

    def withdraw(self, amount: float) -> None:
        self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Insufficient balance.")

        self._balance -= amount
        self.transactions.append(
            Transaction("WITHDRAWAL", amount, "Money withdrawn")
        )

    def transfer_out(self, amount: float) -> None:
        self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Insufficient balance.")

        self._balance -= amount
        self.transactions.append(
            Transaction("TRANSFER OUT", amount, "Funds transferred")
        )

    def transfer_in(self, amount: float) -> None:
        self._validate_amount(amount)
        self._balance += amount
        self.transactions.append(
            Transaction("TRANSFER IN", amount, "Funds received")
        )

    @staticmethod
    def _validate_amount(amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    @property
    @abstractmethod
    def account_type(self) -> str:
        pass

    @abstractmethod
    def calculate_interest(self) -> float:
        pass


@dataclass
class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.05

    @property
    def account_type(self) -> str:
        return "Savings Account"

    def calculate_interest(self) -> float:
        return self.balance * self.INTEREST_RATE


@dataclass
class CurrentAccount(BankAccount):
    @property
    def account_type(self) -> str:
        return "Current Account"

    def calculate_interest(self) -> float:
        return 0.0


@dataclass
class BusinessAccount(BankAccount):
    INTEREST_RATE = 0.03

    @property
    def account_type(self) -> str:
        return "Business Account"

    def calculate_interest(self) -> float:
        return self.balance * self.INTEREST_RATE
