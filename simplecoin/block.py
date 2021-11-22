import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import hashlib
import time
from typing import List

from simplecoin.transaction import Transaction


class Block:
    def __init__(self, data: List[Transaction], prev_block_hash: str = None, nonce: int = 0, timestamp: float = None):
        self.prev_block_hash = prev_block_hash
        self.nonce = nonce
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self) -> str:
        serialize_block = f"{self.prev_block_hash}{self.nonce}{self.data}{self.timestamp}"

        return hashlib.sha256(serialize_block.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"** {self.prev_block_hash}-{self.nonce}-{self.data}-{self.timestamp} **\n"
