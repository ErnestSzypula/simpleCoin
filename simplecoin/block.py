import hashlib
import time

from simplecoin.transaction import Transaction


class Block:
    def __init__(self, prev_block_hash: str, nonce: str, data: Transaction, timestamp=None):
        self.prev_block_hash = prev_block_hash
        self.nonce = nonce
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self) -> str:
        serialize_block = f"{self.prev_block_hash}{self.nonce}{self.data}{self.timestamp}"

        return hashlib.sha256(serialize_block.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"**{self.prev_block_hash}-{self.nonce}-{self.data}-{self.timestamp}**\n"

