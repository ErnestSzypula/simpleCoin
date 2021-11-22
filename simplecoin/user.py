from simplecoin.chain_manager import ChainManager
from typing import List


class User:
    def __init__(self, name: str, chain_manager: ChainManager):
        self.name = name
        self.chain_manager = chain_manager
        self.coins: List[int] = []
        self.hash = None

    def update_hash(self, ha: str):
        self.hash = ha

    def checkout(self):
        self.coins = self.chain_manager.checkout(self.name)

    def get_block_chain_hash(self):
        pass
