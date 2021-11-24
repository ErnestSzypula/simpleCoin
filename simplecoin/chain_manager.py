import secrets
import random
from typing import List, Dict, Any, Callable

from simplecoin.block import Block
from simplecoin.coin_storage import CoinStorage
from simplecoin.error import CoinNotBelongToUserError, DoubleSpendingError

from simplecoin.json_communication.transaction import Transaction
from simplecoin.json_communication.generic import GenericRequest
from simplecoin.json_communication.request_type import RequestType
from simplecoin.json_communication.createcoin import CreateCoin


class ChainManager:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_data: List[Transaction] = []
        self.coin_store: CoinStorage = CoinStorage()
        self.hash_callback: List[Callable[[str], None]] = []

    def append_block(self, block: Block):
        self.chain.append(block)

    def construct_first_block(self, users: List[str], coin_amount: int):
        for i in range(coin_amount):
            coin_id = self.coin_store.new_coin(random.uniform(0, 10.0))
            self.pending_data.append(Transaction(recipient=random.choice(users),  coin_id=coin_id))
        temporary_block = Block(
            data=self.pending_data)
        self.pending_data = []
        block = ChainManager.proof_of_work(temporary_block)
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
        if not self.has_user_coin(transaction):
            raise CoinNotBelongToUserError

        if self.is_double_spending(transaction):
            raise DoubleSpendingError

        self.pending_data.append(transaction)

    def has_user_coin(self, transaction: Transaction) -> bool:
        return transaction.coin_id in self.checkout(transaction.sender)

    def is_double_spending(self, transaction: Transaction) -> bool:
        for t in  self.pending_data:
            if t.sender == transaction.sender and t.coin_id == transaction.coin_id:
                return True

        return False

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
        return block.calculate_hash.startswith("0" * mining_difficulty_level)

    def dig_block(self) -> Dict[str, Any]:
        prev_block_hash = self.chain[-1].calculate_hash
        temporary_block = Block(
            prev_block_hash=prev_block_hash,
            data=self.pending_data)
        
        block = ChainManager.proof_of_work(temporary_block)

        if ChainManager.check_validity(block, self.chain[-1]):
            print("Validation successful... appending")
            self.chain.append(block)
            self.pending_data = []

        for hc in self.hash_callback:
            hc(block.calculate_hash)

        # self.propagate_transaction_completed(block)

        return vars(block)

    # def propagate_transaction_completed(self, b: Block):
    #     for t in b.data:
    #         if isinstance(t, Transaction):
    #             self.users[t.sender].request(
    #                 GenericRequest(
    #                     RequestType.transactionCompleted,
    #                     t))

    @staticmethod
    def check_validity(block: Block, prev_block: Block) -> bool:
        if prev_block.calculate_hash != block.prev_block_hash:
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

    def checkout(self, user: str) -> List[int]:
        coins = []
        for b in self.chain:
            for t in b.data:
                if t.recipient == user:
                    coins.append(t.coin_id)
                elif t.sender == user:
                    coins.remove(t.coin_id)
        return coins

    def request(self, payload: GenericRequest):
        print(payload)

        if payload.type == RequestType.transactionRequest:
            self.new_data(payload.properties)
            # transactionCompleted will be on block creation
            
        elif payload.type == RequestType.createCoin:
            if isinstance(payload, CreateCoin):
                coin_id = self.coin_store.new_coin(random.uniform(0, 10.0))
                self.pending_data.append(Transaction(recipient=payload.user,  coin_id=coin_id))

        elif payload.type == RequestType.checkout:
            self.checkout(payload.user)

        elif payload.type == RequestType.validateBlockchain:
            self.is_valid()