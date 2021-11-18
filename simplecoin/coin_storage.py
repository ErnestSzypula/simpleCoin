from typing import List


class CoinStorage:
    def __init__(self):
        self.data: List[float] = []

    def new_coin(self, value: float) -> int:
        self.data.append(value)
        return len(self.data) - 1

    def get_value(self, coin_id: int) -> float:
        if coin_id < 0 or coin_id >= len(self.data):
            print('Wrong coin_id')
            return 0
        return self.data[coin_id]