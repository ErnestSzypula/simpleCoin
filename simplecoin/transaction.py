from dataclasses import dataclass


@dataclass
class Transaction:
    sender: int
    recipient: int
    quantity: float
