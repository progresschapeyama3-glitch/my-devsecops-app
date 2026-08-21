import pytest

from repositories.account_repository import InMemoryAccountRepository
from services.bank_service import BankService
from services.notification_service import NotificationService


@pytest.fixture
def bank():
    return BankService(
        InMemoryAccountRepository(),
        NotificationService(),
    )


def test_create_account(bank):
    account = bank.create_account(
        "C001",
        "Alice",
        "alice@example.com",
        "SA001",
        "savings",
        1000,
    )

    assert account.balance == 1000
    assert account.account_type == "Savings Account"


def test_deposit(bank):
    bank.create_account(
        "C001", "Alice", "alice@example.com",
        "SA001", "savings", 1000
    )

    bank.deposit("SA001", 500)

    assert bank.get_account("SA001").balance == 1500


def test_withdraw(bank):
    bank.create_account(
        "C001", "Alice", "alice@example.com",
        "SA001", "savings", 1000
    )

    bank.withdraw("SA001", 300)

    assert bank.get_account("SA001").balance == 700


def test_transfer(bank):
    bank.create_account(
        "C001", "Alice", "alice@example.com",
        "SA001", "savings", 1000
    )

    bank.create_account(
        "C002", "Bob", "bob@example.com",
        "CA001", "current", 500
    )

    bank.transfer("SA001", "CA001", 200)

    assert bank.get_account("SA001").balance == 800
    assert bank.get_account("CA001").balance == 700


def test_insufficient_balance(bank):
    bank.create_account(
        "C001", "Alice", "alice@example.com",
        "SA001", "savings", 100
    )

    with pytest.raises(ValueError, match="Insufficient balance"):
        bank.withdraw("SA001", 200)
