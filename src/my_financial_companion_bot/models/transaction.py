from typing import Optional
from .transaction_type import TransactionType

class Transaction:

    def __init__(self, date: str, description: str,
                 amount: float, type: TransactionType, original_source: str,
                 category_id: int, tags: str, note: str, installment_series_id: Optional[int]):
        self.date = date
        self.description = description
        self.amount = amount
        self.type = type
        self.original_source = original_source
        self.category_id = category_id
        self.tags = tags
        self.note = note
        self.installment_series_id = installment_series_id

    def to_tuple(self):
        return (
            self.date, self.description, self.amount,
            self.type.value, self.original_source, self.category_id,
            self.tags, self.note, self.installment_series_id
        )

