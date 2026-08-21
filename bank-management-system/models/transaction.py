from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    transaction_type: str
    amount: float
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
