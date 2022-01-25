from typing import List


class CoinStorage:
    def __init__(self):
        self.counter: int = 0;

    def new_coin(self) -> int:
        self.counter = self.counter + 1;
        return self.counter-1;

    def set_counter(self, value: int):
        self.counter = value;
