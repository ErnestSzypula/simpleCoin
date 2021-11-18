import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import hashlib
import time
from typing import List

from simplecoin.transaction import Transaction


@dataclass_json
@dataclass
class Block:
    prev_block_hash: str
    data: List[Transaction]
    nonce: int = 0
    timestamp: float = time.time()


def calculate_hash(b: Block) -> str:
    return hashlib.sha256(b.to_json().encode('utf-8')).hexdigest()
