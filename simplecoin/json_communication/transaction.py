from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Transaction:
    recipient: str
    coin_id: int
    sender: str = None

