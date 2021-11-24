from cmd import Cmd

from simplecoin.chain_manager import ChainManager
from simplecoin.user import ChainManager, User
from simplecoin.json_communication.transaction import Transaction
from simplecoin import CoinNotBelongToUserError, DoubleSpendingError

from tools import read
from typing import Dict


class App(Cmd):
    intro = 'Welcome to the simpleCoin shell.\nType help or ? to list commands.\n'
    prompt = '(simpleCoin)> '

    def __init__(self):
        Cmd.__init__(self)
        self.users: Dict[str, User] = {}
        self.chain_manager: ChainManager = ChainManager()

    def default(self, line: str):
        self.stdout.write("unknown command: %s \n Type help or ? to list commands.\n")

    def do_initialize_blockchain(self, arg):
        """Initialize Blockchain with given coin amount"""
        if arg == "":
            print("error: you need give coin amount")
            return
        self.chain_manager.construct_first_block([u for u in self.users], int(arg))

    def do_print_blockchain(self, arg):
        """Print Blockchain"""
        print("** prev block hash-nonce-data-timestamp **")
        print(self.chain_manager.chain)

    def do_print_pending_data(self, arg):
        """Print Block Chain Pending Data"""
        print(self.chain_manager.pending_data)

    def do_add_transaction(self, arg):
        """Add transaction"""
        try:
            transaction: Transaction = read_transaction()
            if transaction.sender not in self.users:
                print("error: User does not exists")
                return
            self.users[transaction.sender].new_transaction(transaction)
            # self.chain_manager.new_data(transaction)
        except ValueError:
            print("Wrong input value")
        except CoinNotBelongToUserError:
            print("coin not belong to user")
        except DoubleSpendingError:
            print("double spending")

    def do_dig_block(self, arg):
        """Dig block"""
        self.chain_manager.dig_block()

    def do_check_blockchain_validity(self, arg):
        """Check blockchain validity"""
        if self.chain_manager.is_valid():
            print("block chain is valid")
        else:
            print("block chain is invalid!")

    def do_add_user(self, arg):
        """Add user with given name"""
        if arg == "":
            print("error: you need give user name")
            return
        user = User(arg, self.chain_manager)
        self.users[arg] = user
        self.chain_manager.register_user_callback(user.update_hash)

    def do_show_user_hash(self, arg):
        """Show user with given name hash"""
        if arg == "":
            print("error: you need give user name")
            return

        try:
            print(self.users[arg].hash)
        except KeyError:
            print("user not exist")

    def do_user_checkout(self, arg):
        """User with given name checkout"""
        if arg == "":
            print("error: you need give user name")
            return
        try:
            self.users[arg].checkout()
            print(f"User {arg} have coin eith IDs {self.users[arg].coins}")
        except KeyError:
            print("user not exist")

    def cmdloop(self, intro=None):
        print(self.intro)
        try:
            Cmd.cmdloop(self, intro="")
        except KeyboardInterrupt:
            print("^C")


def read_transaction() -> Transaction:
    sender: str = read(str, "sender")
    recipient: str = read(str, "recipient")
    coin_id: int = read(int, "coin_id")
    return Transaction(sender=sender, recipient=recipient, coin_id=coin_id)
