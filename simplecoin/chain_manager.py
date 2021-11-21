import secrets
import hashlib
from typing import List, Dict, Any, Callable

from simplecoin.block import Block, calculate_hash
from simplecoin.transaction import Transaction
from simplecoin.coin_storage import CoinStorage


class ChainManager:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_data: List[Transaction] = []
        self.coin_store: CoinStorage = CoinStorage()
        self.hash_callback: List[Callable[[str], None]] = []
        self.construct_first_block()

    def append_block(self, block: Block):
        self.chain.append(block)

    def construct_first_block(self):
        tempolary_block = Block(
            prev_block_hash=hashlib.sha256("0".encode()).hexdigest(),
            data=self.pending_data)
        self.pending_data = []
        block = ChainManager.proof_of_work(tempolary_block)
        self.chain.append(block)

    def construct_block(self, prev_block_hash: str, nonce: int) -> Block:
        block = Block(
            prev_block_hash=prev_block_hash,
            nonce=nonce,
            data=self.pending_data)
        self.pending_data = []

        self.chain.append(block)
        return block

    def last_block(self) -> Block:
        return self.chain[-1]

    def new_data(self, transaction: Transaction):
        self.pending_data.append(transaction)

    @staticmethod
    def proof_of_work(block: Block) -> Block:
       
        rounds = 0
        block.nonce = secrets.randbits(32)
        while ChainManager.verifying_proof(block) is False:
            block.nonce = secrets.randbits(32)
            rounds += 1

        print("It took ", rounds, " rounds")

        return block

    @staticmethod
    def verifying_proof(block: Block) -> bool:
        mining_difficulty_level = 2
        return calculate_hash(block).startswith("0" * mining_difficulty_level)

    def dig_block(self) -> Dict[str, Any]:
        prev_block_hash = calculate_hash(self.chain[-1])
        temporary_block = Block(
            prev_block_hash=prev_block_hash,
            data=self.pending_data)
        
        block = ChainManager.proof_of_work(temporary_block)

        if ChainManager.check_validity(block, self.chain[-1]):
            print("Validation successful... appending")
            self.chain.append(block)
            self.pending_data = []

        for hc in self.hash_callback:
            hc(calculate_hash(block))

        return vars(block)

    @staticmethod
    def check_validity(block: Block, prev_block: Block) -> bool:
        if calculate_hash(prev_block) != block.prev_block_hash:
            return False

        elif prev_block.timestamp >= block.timestamp:
            return False

        elif not ChainManager.verifying_proof(block):
            return False

        return True

    def is_valid(self) -> bool:
        for i in range(len(self.chain) - 1, 0, -1):
            if ChainManager.check_validity(self.chain[i], self.chain[i-1]) is False:
                return False
        return True

    def register_user_callback(self, f: Callable[[str], None]):
        self.hash_callback.append(f)
