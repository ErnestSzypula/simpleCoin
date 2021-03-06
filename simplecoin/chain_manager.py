from logging import error
import secrets
import rsa

from typing import List

from simplecoin.block import Block
from simplecoin.coin_storage import CoinStorage
from simplecoin.error import CoinNotBelongToUserError, DoubleSpendingError
from simplecoin.identity import is_key_signature, sign

from simplecoin.json_communication.transaction import Transaction
from simplecoin.json_communication.generic import GenericRequest
from simplecoin.json_communication.request_type import RequestType
from simplecoin.json_communication.createcoin import CreateCoin
from simplecoin.json_communication.transaction_data import TransactionData
from simplecoin.json_communication.transaction_type import TransactionType


class ChainManager:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_data: List[Transaction] = []
        self.coin_store: CoinStorage = CoinStorage()
        self.identities: List[rsa.PublicKey] = []
        self.public_key = None

    def set_genesis_block(self, block: Block, public_key):
        self.chain.append(block)
        self.public_key = public_key

    def append_block(self, block: Block):
        self.pending_data = []
        self.chain.append(block)

    def last_block(self) -> Block:
        return self.chain[-1]

    def new_data(self, transaction: Transaction):
        if not self.has_user_coin(transaction):
            raise CoinNotBelongToUserError

        if self.is_double_spending(transaction):
            raise DoubleSpendingError

        self.pending_data.append(transaction)

    def has_user_coin(self, t: Transaction) -> bool:
        for iden in self.identities:
            if is_key_signature(t.transaction_data.to_json(), t.signature, iden):
                # print("Coin", t.transaction_data.coi÷n_id, "belongs to", iden.n)
                if(t.transaction_data.type == TransactionType.createCoin):
                    return True
                return t.transaction_data.coin_id in self.checkout(iden)
        return False

    def is_double_spending(self, transaction: Transaction, block_transactions: List[Transaction]) -> bool:
        identity = self.get_transaction_identity(transaction)
        for t in block_transactions:
            t_identity = self.get_transaction_identity(t)
            if identity == t_identity and t.transaction_data.coin_id == transaction.transaction_data.coin_id:
                return True

        return False

    def get_transaction_identity(self, transaction: Transaction):
        for iden in self.identities:
            if is_key_signature(transaction.transaction_data.to_json(), transaction.signature, iden):
                return iden
        return None

    @staticmethod
    def proof_of_work(block: Block) -> Block:
        rounds = 0
        block.nonce = secrets.randbits(32)
        while ChainManager.verifying_proof(block) is False:
            block.nonce = secrets.randbits(32)
            rounds += 1

        print("Someone took", rounds, "rounds to dig")

        return block

    @staticmethod
    def verifying_proof(block: Block) -> bool:
        mining_difficulty_level = 2
        return block.calculate_hash.startswith("0" * mining_difficulty_level)

    def dig_block(self, diggerPublickKey, diggerPrivateKey ) -> Block:
        prev_block_hash = self.chain[-1].calculate_hash

        # adding reward
        
        self.updateCoinStorage()
        
        coin_id = self.coin_store.new_coin()
        transaction_data = TransactionData(diggerPublickKey.n,  coin_id=coin_id,
                                           type=TransactionType.createCoin)
        self.pending_data.append(Transaction(transaction_data=transaction_data,
                                             signature=sign(transaction_data.to_json(), diggerPrivateKey)))
        temporary_block = Block(
            prev_block_hash=prev_block_hash,
            data=self.pending_data)
        
        block = ChainManager.proof_of_work(temporary_block)

        return block

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
                error(self.chain[i])
                error(self.chain[i-1])
                return False
        return True

    def genesis_validation(self) -> bool:
        for transaction in self.chain[0].data:
            if not is_key_signature(transaction.transaction_data.to_json(), transaction.signature, self.public_key):
                error(transaction.transaction_data.to_json())
                return False
        return True

    def coin_owner(self, coin_id: int, block_id: int) -> rsa.PublicKey:
        owner: rsa.PublicKey
        for b in self.chain[:block_id]:
            for t in b.data:
                if t.transaction_data.coin_id == coin_id:
                    owner = rsa.PublicKey(t.transaction_data.recipient, 65537)
        return owner

    def transactions_validation(self) -> bool:
        for block_id, block in enumerate(self.chain[1:], start=1):
            for transaction in block.data:
                if not is_key_signature(transaction.transaction_data.to_json(), 
                                        transaction.signature, 
                                        self.coin_owner(transaction.transaction_data.coin_id, block_id)):
                    error(transaction.transaction_data.to_json())
                    return False
            return True

    def checkout(self, identity: rsa.PublicKey) -> List[int]:
        coins = []
        for b in self.chain:
            for t in b.data:
                if t.transaction_data.recipient == identity.n:
                    coins.append(t.transaction_data.coin_id)
                elif is_key_signature(t.transaction_data.to_json(), t.signature, identity):
                    coins.remove(t.transaction_data.coin_id)
        return coins



    def block_transactions_validation(self, block: Block):
        createCoinCounter = 0
        for i, t in enumerate(block.data):
            # print("Checking ", t.transaction_data)
            if not self.has_user_coin(t):
                return False

            if self.is_double_spending(t, block.data[:i]):
                return False 

            if(t.transaction_data.type == TransactionType.createCoin):
                createCoinCounter = createCoinCounter + 1
        

        # there must be only one coin created
        if (createCoinCounter != 1):
            return False
        
        return True

    def request(self, payload: GenericRequest):
        print(payload)

        if payload.type == RequestType.transactionRequest:
            self.new_data(payload.properties)
            # transactionCompleted will be on block creation
            
        elif payload.type == RequestType.createCoin:
            if isinstance(payload, CreateCoin):
                coin_id = self.coin_store.new_coin()
                self.pending_data.append(Transaction(recipient=payload.user,  coin_id=coin_id))

        elif payload.type == RequestType.checkout:
            self.checkout(payload.user)

        elif payload.type == RequestType.validateBlockchain:
            self.is_valid()

    def updateCoinStorage(self):
        maxCoinId = 0
        for block in self.chain:
            for transaction in block.data:
                maxCoinId = max(maxCoinId, transaction.transaction_data.coin_id)
        self.coin_store.set_counter(maxCoinId+1)
        