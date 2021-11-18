import json
from cmd import Cmd

from simplecoin import ChainManager, Transaction
from tools import read


class App(Cmd):
    intro = 'Welcome to the simpleCoin shell.\nType help or ? to list commands.\n'
    prompt = '(simpleCoin)> '

    def __init__(self, miner_id):
        Cmd.__init__(self)
        self.chain_manager: ChainManager = ChainManager()
        print("To build the first block")
        self.miner_id = miner_id

    def default(self, line: str):
        self.stdout.write("unknown command: %s \n Type help or ? to list commands.\n")

    def do_print_blockchain(self, arg):
        """Print Blockchain"""
        print("** prev block hash-nonce-data-timestamp **")
        print(json.dumps(self.chain_manager.chain))

    def do_print_pending_data(self, arg):
        """Print Block Chain Pending Data"""
        print(json.dumps(self.chain_manager.pending_data))

    def do_add_transaction(self, arg):
        """Add transaction"""
        try:
            transaction: Transaction = read_transaction()
            self.chain_manager.new_data(transaction)
        except ValueError:
            pass

    def do_dig_block(self, arg):
        """Dig block"""
        self.chain_manager.dig_block(self.miner_id)

    def do_check_blockchain_validity(self, arg):
        """Check blockchain validity"""
        if self.chain_manager.is_valid():
            print("block chain is valid")
        else:
            print("block chain is invalid!")

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
