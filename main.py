import multiprocessing

from simplecoin.chain_manager import ChainManager
from simplecoin.coin_storage import CoinStorage
from simplecoin.construct_genesis_block import construct_genesis_block
from simplecoin.user import ChainManager, User
from simplecoin.json_communication.transaction import TransactionData
from simplecoin import CoinNotBelongToUserError, DoubleSpendingError

from typing import Dict

COIN_AMOUNT = 10


def main():
    coin_storage: CoinStorage = CoinStorage()

    # CREATE IDENTITY
    users = [User("bob"), User("ala"), User("john")]

    # CREATE BLOCKCHAIN, CREATE COINS
    genesis_block, genesis_block_public_key = construct_genesis_block(coin_storage, [u.public_key for u in users],
                                                                      COIN_AMOUNT)

    for i in range(len(users)):
        users[i].set_genesis_block(genesis_block, genesis_block_public_key)

    # INITIALIZE NETWORK
    for i in range(len(users)):
        for j in range(len(users)):
            if i != j:
                users[i].register_node(users[j])

    # CHECKOUT
    for i in range(len(users)):
        users[i].checkout()
        print("User {} coins: {} {}".format(users[i].name, users[i].coins, users[i].public_key.n))

    # # TRANSACTION EXAMPLES
    users[0].new_transaction(TransactionData(recipient=users[2].public_key.n, coin_id=users[0].coins[0]))
    users[1].new_transaction(TransactionData(recipient=users[2].public_key.n, coin_id=users[1].coins[0]))
    users[2].new_transaction(TransactionData(recipient=users[1].public_key.n, coin_id=users[2].coins[0]))

    # MAKE TURN

    processs = []
    result_queue = multiprocessing.Queue()

    print("Start dig")
    for i in range(len(users)):
        process = multiprocessing.Process(target=users[i].dig_block, args=[result_queue])
        process.start()
        processs.append(process)

    winning_user = result_queue.get()
    print("End dig")
    print(f"digging win by {winning_user.name}")

    for process in processs:
        process.terminate()

    winning_user.broadcast_proposed_block()

    # CHECKOUT
    for i in range(len(users)):
        users[i].checkout()
        print("User {} coins: {} {}".format(users[i].name, users[i].coins, users[i].public_key.n))


if __name__ == '__main__':
    main()
