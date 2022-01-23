import random
import rsa


from typing import List

from simplecoin import ChainManager
from simplecoin.block import Block
from simplecoin.coin_storage import CoinStorage
from simplecoin.identity import sign, newkeys

from simplecoin.json_communication.transaction import Transaction
from simplecoin.json_communication.transaction_data import TransactionData
from simplecoin.json_communication.transaction_type import TransactionType


def construct_genesis_block(coin_store: CoinStorage, identities: List[rsa.PublicKey], coin_amount: int):
    public_key, private_key = newkeys()
    pending_data = []
    for i in range(coin_amount):
        coin_id = coin_store.new_coin(random.uniform(0, 10.0))
        transaction_data = TransactionData(random.choice(identities).n,  coin_id=coin_id,
                                           type=TransactionType.createCoin)
        pending_data.append(Transaction(transaction_data=transaction_data,
                                             signature=sign(transaction_data.to_json(), private_key)))
    temporary_block = Block(data=pending_data)
    block = ChainManager.proof_of_work(temporary_block)

    return block, public_key
