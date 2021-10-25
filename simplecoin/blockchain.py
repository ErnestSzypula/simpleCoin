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
    def proof_of_work(last_nonce: str):
       
        rounds = 0
        secret = secrets.randbits(32)
        while BlockChain.verifying_proof(last_nonce, secret) is False:
            secret = secrets.randbits(32)
            rounds += 1

        print("It took ", rounds," rounds")

        return secret

    @staticmethod
    def verifying_proof(last_nonce, nonce):
        mining_difficulty_level=2
        hash_digest = hashlib.sha256(f'{last_nonce}{nonce}'.encode()).hexdigest()
        return hash_digest.startswith("0" * mining_difficulty_level)

    def dig_block(self, miner_id):
        last_nonce = self.chain[-1].nonce
        nonce = BlockChain.proof_of_work(last_nonce)
        self.new_data(Transaction(0,miner_id, 1.)) # Reward for the miner
        block = self.construct_block(last_nonce, nonce)

        return vars(block)

    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.calculate_hash != block.prev_block_hash:
            return False

        elif prev_block.timestamp >= block.timestamp:
            return False

        elif BlockChain.verifying_proof(prev_block.nonce, block.nonce):
            return False

