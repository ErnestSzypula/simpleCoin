import random

from simplecoin.chain_manager import ChainManager
from simplecoin.identity import sign, newkeys
from simplecoin.block import Block
from simplecoin.json_communication.response_code import ResponseCode
from simplecoin.json_communication.transaction_data import TransactionData
from simplecoin.json_communication.transaction import Transaction
from simplecoin.json_communication.generic import GenericRequest
from simplecoin.json_communication.request_type import RequestType

from typing import List, Callable, Any


class User:
    def __init__(self, name: str):
        self.name = name
        self.public_key, self.private_key = newkeys()
        self.chain_manager = ChainManager()
        self.chain_manager.identities.append(self.public_key)
        self.coins: List[int] = []
        self.hash = None
        self.nodes: List[Callable[[Any], Any]] = []
        self.proposed_block: Block = None

    def set_genesis_block(self, block: Block, public_key):
        self.chain_manager.set_genesis_block(block, public_key)

    def dig_block(self, result_queue):
        self.proposed_block = self.chain_manager.dig_block(self.public_key, self.private_key)
        result_queue.put((self.name, self.proposed_block))

    def update_hash(self, ha: str):
        self.hash = ha

    def register_node(self, n):
        self.nodes.append(n)
        self.chain_manager.identities.append(n.public_key)

    def checkout(self):
        self.coins = self.chain_manager.checkout(self.public_key)

    def get_block_chain_hash(self):
        self.hash = self.chain_manager.last_block.calculate_hash()

    def new_transaction(self, t: TransactionData):
        transaction = Transaction(transaction_data=t,
                    signature=sign(t.to_json(), self.private_key))

        self.chain_manager.pending_data.append(transaction)

        self.broadcast_transaction(transaction)

    def broadcast_transaction(self, t: Transaction):
        for n in self.nodes:
            if random.random() < 0.9:
                n.request(GenericRequest(RequestType.transactionRequest, t))

    def broadcast_proposed_block(self, proposed_block):
        self.proposed_block = proposed_block
        for n in self.nodes:
            response = n.request(GenericRequest(RequestType.proposedBlock, self.proposed_block))
            if response == response.reject:
                print(f"block rejected")
                return

        print("block successfully broadcasted")
        if self.chain_manager.check_validity(proposed_block, self.chain_manager.chain[-1]):
            self.chain_manager.append_block(proposed_block)
        else:
            print("faild to validate")



    def append_proposed_block(self, block: Block):
        if not self.validate_proposed_block(block):
            return ResponseCode.reject
        self.chain_manager.append_block(block)
        return ResponseCode.accept

    def validate_proposed_block(self, block: Block):
        print(self.name, "is validating proposed block")
        if not self.chain_manager.block_transactions_validation(block):
            return False
        return True

    def request(self, payload: GenericRequest):
        if payload.type == RequestType.updateHash:
            self.update_hash(payload.properties)

        elif payload.type == RequestType.transactionRequest:
            self.chain_manager.pending_data.append(payload.properties)

        elif payload.type == RequestType.proposedBlock:
            return self.append_proposed_block(payload.properties)

        elif payload.type == RequestType.transactionCompleted:
            print(payload)

        elif payload.type == RequestType.checkout:
            print(payload)

        elif payload.type == RequestType.validateBlockchain:
            print(payload)
        
