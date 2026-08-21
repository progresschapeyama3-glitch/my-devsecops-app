from abc import ABC, abstractmethod
from typing import List, Optional

from models.account import BankAccount


class AccountRepository(ABC):

    @abstractmethod
    def save(self, account: BankAccount) -> None:
        pass

    @abstractmethod
    def find_by_account_number(
        self, account_number: str
    ) -> Optional[BankAccount]:
        pass

    @abstractmethod
    def exists(self, account_number: str) -> bool:
        pass

    @abstractmethod
    def all_accounts(self) -> List[BankAccount]:
        pass


class InMemoryAccountRepository(AccountRepository):

    def __init__(self):
        self._accounts = {}

    def save(self, account: BankAccount) -> None:
        self._accounts[account.account_number] = account

    def find_by_account_number(
        self, account_number: str
    ) -> Optional[BankAccount]:
        return self._accounts.get(account_number)

    def exists(self, account_number: str) -> bool:
        return account_number in self._accounts

    def all_accounts(self) -> List[BankAccount]:
        return list(self._accounts.values())
