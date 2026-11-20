import hashlib
import json
from time import time


class Block:
    def __init__(self, index, timestamp, candidate_id, vote, voter_id, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.candidate_id = candidate_id
        self.vote = vote
        self.voter_id = voter_id
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2  # Adjust the difficulty as needed
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually create the first block (genesis block)
        genesis_block = Block(0, time(), None, None, None, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, candidate_id, vote, voter_id):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time(), candidate_id, vote, voter_id, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def get_blocks(self):
        return [(block.index, block.timestamp, block.candidate_id, block.vote, block.voter_id) for block in self.chain[1:]]


# Example usage
if __name__ == "__main__":
    # Create a blockchain
    blockchain = Blockchain()

    # Add blocks with candidate ID, vote, and voter ID
    blockchain.add_block("1", "yes", "123")
    blockchain.add_block("1", "no", "456")
    blockchain.add_block("2", "yes", "789")

    # Get blocks from the blockchain
    blocks = blockchain.get_blocks()
    for block in blocks:
        print("Block:", block[0], "Hash:", block[4])
