import hashlib
import secrets

from simplecoin.transaction import Transaction


class Block:
    def __init__(self, prev_block_hash: str, transaction: Transaction, miner_id: str):
        self.prev_block_hash = prev_block_hash
        self.nonce = 0
        self.transaction = transaction
        self.miner_id = miner_id

    def calculate_hash(self, nonce) -> str:
        self.nonce = nonce
        serialize_block = f"{self.prev_block_hash}{self.nonce}{self.transaction}{self.miner_id}"

        return hashlib.sha256(serialize_block.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"{self.prev_block_hash}-{self.nonce}-{self.transaction}-{self.miner_id}"

    def dig_block(self, mining_difficulty_level: int) -> str:
        hash_digest = self.calculate_hash(secrets.randbits(32))
        print(hash_digest)

        rounds = 0

        # TODO: correct this condition
        while not hash_digest.startswith("0" * mining_difficulty_level):
            hash_digest = self.calculate_hash(secrets.randbits(32))
            print(hash_digest)
            rounds += 1

        print(rounds)

        return hash_digest
