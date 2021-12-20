from simplecoin.chain_manager import ChainManager
from simplecoin.user import ChainManager, User
from simplecoin.json_communication.transaction import TransactionData
from simplecoin import CoinNotBelongToUserError, DoubleSpendingError

from typing import Dict


COIN_AMOUNT = 10


def main():
    chain_manager: ChainManager = ChainManager()

    # CREATE IDENTITY
    users: Dict[str, User] = {
        "bob": User(chain_manager),
        "ala": User(chain_manager),
        "john": User(chain_manager),
    }

    chain_manager.register_user_callback(users["bob"].update_hash)
    chain_manager.register_user_callback(users["ala"].update_hash)
    chain_manager.register_user_callback(users["john"].update_hash)

    # CREATE BLOCKCHAIN, creating coins
    chain_manager.construct_first_block([users[key].public_key for key in users], COIN_AMOUNT)

    for key in users:
        users[key].checkout()
        print("User {} coins: {}".format(key, users[key].coins))

    # TRANSACTION EXAMPLE

    users["bob"].new_transaction(TransactionData(recipient=users["john"].public_key.__str__(), coin_id=users["bob"].coins[0]))

    chain_manager.dig_block()

    for key in users:
        users[key].checkout()
        print("User {} coins: {}".format(key, users[key].coins))

    # VALIDATE COINS (GENESIS VALIDATION)


    # chain_manager.chain[0].data[0].transaction_data.coin_id = 2
    chain_manager.genesis_validation()


    # VALIDATE TRANSACTIONS (USER SIGN VALIDATION)

    # VALIDATE BLOCKCHAIN

    



if __name__ == '__main__':
    main()
