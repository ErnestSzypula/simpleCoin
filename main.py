import uuid
from simplecoin import Transaction, Block


def main():
    miner_id = str(uuid.uuid4())
    mining_difficulty_level = 2

    print(f"Start program with miner {miner_id}")

    initial_block = Block("", Transaction(), miner_id)
    initial_block.dig_block(mining_difficulty_level)

    print(initial_block)


if __name__ == '__main__':
    main()
