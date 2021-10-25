from cmd import Cmd

from simplecoin import BlockChain, Transaction
from tools import read


class App(Cmd):
    intro = 'Welcome to the simpleCoin shell.\nType help or ? to list commands.\n'
    prompt = '(simpleCoin)> '

    def __init__(self, miner_id):
        Cmd.__init__(self)
        self.blockchain: BlockChain = BlockChain()
        self.miner_id = miner_id

    def default(self, line: str):
        self.stdout.write("unknown command: %s \n Type help or ? to list commands.\n")

    def do_print_blockchain(self, arg):
        """Print Blockchain"""
        print("**prev block hash-nonce-data-timestamp**")
        print(self.blockchain.chain)

    def do_print_pending_data(self, arg):
        """Print Block Chain Pending Data"""
        print(self.blockchain.pending_data)

    def do_add_transaction(self, arg):
        """Add transaction"""
        try:
            transaction: Transaction = read_transaction()
            self.blockchain.new_data(transaction)
        except ValueError:
            pass

    def do_dig_block(self, arg):
        """Dig block"""
        self.blockchain.dig_block(self.miner_id)

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
