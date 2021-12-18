from dataclasses import dataclass
from dataclasses_json import dataclass_json
from simplecoin.json_communication.transaction_data import TransactionData


@dataclass_json
@dataclass
class Transaction:
    transaction_data: TransactionData
    signature: bytes = None

