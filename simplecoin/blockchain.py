import secrets
import hashlib

from simplecoin.block import Block
from simplecoin.transaction import Transaction


class BlockChain:
    def __init__(self):
        self.chain:Block = []
        self.pending_data:Transaction = []
        self.construct_first_block()


    def append_block(self, block: Block):
        self.chain.append(block)

    def construct_first_block(self):
        self.construct_block(prev_block_hash="", nonce="")

    def construct_block(self, prev_block_hash, nonce):
        block = Block(
            prev_block_hash=prev_block_hash,
            nonce=nonce,
            data=self.pending_data)
        self.pending_data = []

        self.chain.append(block)
        return block

    def last_block(self) -> Block:
        return self.chain[-1]

    def new_data(self, transaction:Transaction):
        self.pending_data.append(transaction)
        return True

    @staticmethod
    def proof_of_work(hash: str):
        hash_digest = hashlib.sha256(f'{hash}{secrets.randbits(32)}'.encode()).hexdigest()
        mining_difficulty_level=2
        rounds = 0

        while not hash_digest.startswith("0" * mining_difficulty_level):
            hash_digest = hashlib.sha256(f'{hash}{secrets.randbits(32)}'.encode()).hexdigest()
            rounds += 1

        return hash_digest


    def dig_block(self, miner_id):
        last_hash = self.chain[-1].calculate_hash
        nonce = BlockChain.proof_of_work(last_hash)
        self.new_data(Transaction(0,miner_id, 1.)) # Reward for the miner
        block = self.construct_block(last_hash, nonce)

        return vars(block)