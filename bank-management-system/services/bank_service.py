from models.account import (
    BankAccount,
    SavingsAccount,
    CurrentAccount,
    BusinessAccount,
)
from models.customer import Customer
from repositories.account_repository import AccountRepository
from services.notification_service import NotificationService


class BankService:
    """
    Application service responsible for coordinating banking operations.

    DIP:
    This service depends on AccountRepository abstraction rather than
    a concrete database implementation.
    """

    def __init__(
        self,
        repository: AccountRepository,
        notification_service: NotificationService,
    ):
        self.repository = repository
        self.notification_service = notification_service

    def create_account(
        self,
        customer_id: str,
        name: str,
        email: str,
        account_number: str,
        account_type: str,
        initial_balance: float,
    ) -> BankAccount:

        if not customer_id or not name or not email or not account_number:
            raise ValueError("All customer and account fields are required.")

        if self.repository.exists(account_number):
            raise ValueError("Account number already exists.")

        customer = Customer(customer_id, name, email)
        normalized_type = account_type.lower()

        account_classes = {
            "savings": SavingsAccount,
            "current": CurrentAccount,
            "business": BusinessAccount,
        }

        account_class = account_classes.get(normalized_type)

        if account_class is None:
            raise ValueError("Invalid account type.")

        account = account_class(
            account_number=account_number,
            owner=customer,
            _balance=initial_balance,
        )

        self.repository.save(account)

        self.notification_service.send(
            customer.email,
            f"Your {account.account_type} was created."
        )

        return account

    def get_account(self, account_number: str) -> BankAccount:
        account = self.repository.find_by_account_number(account_number)

        if account is None:
            raise ValueError("Account not found.")

        return account

    def deposit(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.deposit(amount)

        self.notification_service.send(
            account.owner.email,
            f"AED {amount:,.2f} was deposited into your account."
        )

    def withdraw(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.withdraw(amount)

        self.notification_service.send(
            account.owner.email,
            f"AED {amount:,.2f} was withdrawn from your account."
        )

    def transfer(
        self,
        source_account_number: str,
        destination_account_number: str,
        amount: float,
    ) -> None:

        if source_account_number == destination_account_number:
            raise ValueError("Source and destination accounts must be different.")

        source = self.get_account(source_account_number)
        destination = self.get_account(destination_account_number)

        source.transfer_out(amount)
        destination.transfer_in(amount)

        self.notification_service.send(
            source.owner.email,
            f"AED {amount:,.2f} was transferred to "
            f"{destination.account_number}."
        )

        self.notification_service.send(
            destination.owner.email,
            f"AED {amount:,.2f} was received from "
            f"{source.account_number}."
        )
