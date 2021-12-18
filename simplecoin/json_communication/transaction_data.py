from simplecoin.json_communication.transaction_type import TransactionType
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TransactionData:
    recipient: str
    coin_id: int
    type: TransactionType = TransactionType.payment

