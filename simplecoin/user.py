from simplecoin.chain_manager import ChainManager
from typing import List


class User:
    def __init__(self, name: str, chain_manager: ChainManager):
        self.name = name
        self.chain_manager = chain_manager
        self.coins: List[str] = []
        self.hash = None

    def update_hash(self, hash: str):
        self.hash = hash

    def checkout(self):
        pass

    def get_block_chain_hash(self):
        pass


