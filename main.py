import multiprocessing
import threading

from simplecoin.chain_manager import ChainManager
from simplecoin.coin_storage import CoinStorage
from simplecoin.construct_genesis_block import construct_genesis_block
from simplecoin.user import ChainManager, User
from simplecoin.json_communication.transaction import TransactionData
from simplecoin import CoinNotBelongToUserError, DoubleSpendingError
from queue import Queue

from typing import Dict

COIN_AMOUNT = 10


def main():
    coin_storage: CoinStorage = CoinStorage()

    # CREATE IDENTITY
    users = {
        "bob": User("bob"),
        "ala": User("ala"),
        "john": User("john")
    }

    # CREATE BLOCKCHAIN, CREATE COINS
    genesis_block, genesis_block_public_key = construct_genesis_block(coin_storage, [users[key].public_key for key in users],
                                                                      COIN_AMOUNT)

    for key in users:
        users[key].set_genesis_block(genesis_block, genesis_block_public_key)

    # INITIALIZE NETWORK
    for key in users:
        for k in users:
            if key != k:
                users[key].register_node(users[k])

    # CHECKOUT
    for key in users:
        users[key].checkout()
        print("User {} coins: {} {}".format(users[key].name, users[key].coins, users[key].public_key.n))

    # # TRANSACTION EXAMPLES
    users["bob"].new_transaction(TransactionData(recipient=users["john"].public_key.n, coin_id=users["bob"].coins[0]))
    users["ala"].new_transaction(TransactionData(recipient=users["john"].public_key.n, coin_id=users["ala"].coins[0]))
    users["john"].new_transaction(TransactionData(recipient=users["bob"].public_key.n, coin_id=users["john"].coins[0]))

    # MAKE TURN
    threads = []
    result_queue = Queue()

    print("Start digging")
    for key in users:
        thread = threading.Thread(target=users[key].dig_block, args=[result_queue])
        thread.start()
        threads.append(thread)

    winning_results = result_queue.get()
    print("End digging")

    for thread in threads:
        thread.join()

    print(f"Digging won by {winning_results[0]}")

    users[winning_results[0]].broadcast_proposed_block(winning_results[1])

    # CHECKOUT
    for key in users:
        users[key].checkout()
        print("User {} coins: {} {}".format(users[key].name, users[key].coins, users[key].public_key.n))


if __name__ == '__main__':
    main()
