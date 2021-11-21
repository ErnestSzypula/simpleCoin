import json
from cmd import Cmd

from simplecoin import ChainManager, Transaction, User
from tools import read
from typing import Dict


class App(Cmd):
    intro = 'Welcome to the simpleCoin shell.\nType help or ? to list commands.\n'
    prompt = '(simpleCoin)> '

    def __init__(self):
        Cmd.__init__(self)
        self.chain_manager: ChainManager = ChainManager()
        self.users: Dict[str, User] = {}
        print("To build the first block")

    def default(self, line: str):
        self.stdout.write("unknown command: %s \n Type help or ? to list commands.\n")

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
            self.chain_manager.new_data(transaction)
        except ValueError:
            pass

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
        """Add user"""
        user = User(arg[0], self.chain_manager)
        self.users[arg[0]] = user
        self.chain_manager.register_user_callback(user.update_hash)

    def do_show_user_hash(self, arg):
        """Show user hash"""
        print(self.users[arg[0]].hash)

    def cmdloop(self, intro=None):
        print(self.intro)
        try:
            Cmd.cmdloop(self, intro="")
        except KeyboardInterrupt:
            print("^C")


def read_transaction() -> Transaction:
    sender: int = read(int, "sender")
    recipient: int = read(int, "recipient")
    quantity: float = read(float, "quantity")
    return Transaction(sender, recipient, quantity)
