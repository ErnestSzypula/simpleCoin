from simplecoin.block import Block


class BlockChain:
    def __init__(self, initial_block: Block):
        self.chain = []
        self.append_block(initial_block)

    def append_block(self, block: Block):
        self.chain.append(block)
