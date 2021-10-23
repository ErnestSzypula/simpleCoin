import uuid
from simplecoin import Transaction, Block, block
from simplecoin.blockchain import BlockChain


def main():
    miner_id = str(uuid.uuid4())

    print(f"\n\nStarting program with miner {miner_id}")

    blockchain = BlockChain()
    print(blockchain.chain)

    # blockchain.dig_block(miner_id)
    blockchain.new_data(Transaction(0,2,1.2))
    blockchain.new_data(Transaction(0,2,1.6))
    print(blockchain.pending_data)
    blockchain.dig_block(miner_id)
    

    print(blockchain.chain)


if __name__ == '__main__':
    main()
