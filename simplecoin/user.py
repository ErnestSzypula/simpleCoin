from simplecoin.chain_manager import ChainManager
from simplecoin.identity import sign, newkeys
from simplecoin.json_communication.transaction_data import TransactionData
from simplecoin.json_communication.transaction import Transaction
from simplecoin.json_communication.generic import GenericRequest
from simplecoin.json_communication.request_type import RequestType
from typing import List


class User:
    def __init__(self, chain_manager: ChainManager):
        self.public_key, self.private_key = newkeys()
        self.chain_manager = chain_manager
        self.coins: List[int] = []
        self.hash = None

    def update_hash(self, ha: str):
        self.hash = ha

    def checkout(self):
        self.coins = self.chain_manager.checkout(self.public_key)

    def get_block_chain_hash(self):
        self.hash = self.chain_manager.last_block.calculate_hash()

    def new_transaction(self, t: TransactionData):
        self.chain_manager.request(
            GenericRequest(
                RequestType.transactionRequest,
                Transaction(transaction_data=t,
                            signature=sign(t.to_json(), self.private_key))))

    def request(self, payload: GenericRequest):
        if payload.type == RequestType.updateHash:
            self.update_hash(payload.properties)

        elif payload.type == RequestType.transactionCompleted:
            print(payload)

        elif payload.type == RequestType.checkout:
            print(payload)

        elif payload.type == RequestType.validateBlockchain:
            print(payload)
        
