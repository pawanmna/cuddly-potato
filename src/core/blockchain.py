import hashlib
import json
import time


class Block:
    
    """
    Represents a single block in the blockchain
    Contains file metadata and cryptographic links
    """
    
    def __init__(self, index, timestamp, data, previous_hash):
        """
        Initialize a new block
        
        Args:
            index: Position in the blockchain
            timestamp: When the block was created
            data: File metadata (dict)
            previous_hash: Hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of block contents
        
        Returns:
            64-character hexadecimal hash string
        """
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        # Sort keys for consistent hashing
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine the block by finding valid hash
        
        Args:
            difficulty: Number of leading zeros required (0 = instant)
        """
        if difficulty == 0:
            return  # No mining needed
        
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
    
    def to_dict(self):
        """
        Convert block to dictionary for serialization
        
        Returns:
            Dictionary representation of block
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @staticmethod
    def from_dict(block_dict):
        """
        Create Block instance from dictionary
        
        Args:
            block_dict: Dictionary with block data
            
        Returns:
            Block instance
        """
        block = Block(
            index=block_dict["index"],
            timestamp=block_dict["timestamp"],
            data=block_dict["data"],
            previous_hash=block_dict["previous_hash"]
        )
        block.nonce = block_dict["nonce"]
        block.hash = block_dict["hash"]
        return block


class Blockchain:
    """
    Manages the blockchain and validates integrity
    """
    
    def __init__(self, difficulty=0):
        """
        Initialize blockchain with genesis block
        
        Args:
            difficulty: Mining difficulty (0 for instant)
        """
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """
        Create the first block in the chain
        """
        genesis = Block(0, time.time(), {"message": "Genesis Block"}, "0")
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)
        print("Genesis block created")
    
    def get_latest_block(self):
        """
        Get the most recent block
        
        Returns:
            Latest Block instance
        """
        return self.chain[-1]
    
    def add_block(self, data):
        """
        Add new block to the chain
        
        Args:
            data: File metadata dictionary
            
        Returns:
            The newly created Block instance
        """
        latest = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=latest.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        print(f"Block #{new_block.index} added to chain")
        return new_block
    
    def remove_block(self, index):
        """
        Remove block at specified index
        
        Args:
            index: Block index to remove
            
        Returns:
            True if successful, False otherwise
        """
        if index <= 0 or index >= len(self.chain):
            return False
        
        self.chain.pop(index)
        # Reindex remaining blocks
        for i in range(index, len(self.chain)):
            self.chain[i].index = i
            if i > 0:
                self.chain[i].previous_hash = self.chain[i-1].hash
                self.chain[i].hash = self.chain[i].calculate_hash()
        
        print(f"Block #{index} removed")
        return True
    
    def is_chain_valid(self):
        """
        Validate entire blockchain integrity
        
        Returns:
            True if chain is valid, False if tampered
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify block's hash matches its content
            if current_block.hash != current_block.calculate_hash():
                print(f" Block {i} is tampered!")
                print(f"  Expected: {current_block.hash}")
                print(f"  Got: {current_block.calculate_hash()}")
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f" Chain broken at block {i}!")
                print(f"  Block {i} points to: {current_block.previous_hash}")
                print(f"  Block {i-1} actually is: {previous_block.hash}")
                return False
        
        return True
    
    def to_dict(self):
        """
        Convert blockchain to dictionary for serialization
        
        Returns:
            Dictionary with chain data
        """
        return {
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain]
        }
    
    @staticmethod
    def from_dict(blockchain_dict):
        """
        Create Blockchain instance from dictionary
        
        Args:
            blockchain_dict: Dictionary with blockchain data
            
        Returns:
            Blockchain instance
        """
        blockchain = Blockchain.__new__(Blockchain)
        blockchain.difficulty = blockchain_dict.get("difficulty", 0)
        blockchain.chain = [Block.from_dict(b) for b in blockchain_dict["chain"]]
        return blockchain
    
    def get_block_by_file_id(self, file_id):
        """
        Find block containing specific file ID
        
        Args:
            file_id: Unique file identifier
            
        Returns:
            Block instance or None
        """
        for block in self.chain:
            if isinstance(block.data, dict) and block.data.get("file_id") == file_id:
                return block
        return None
    
    def __len__(self):
        """
        Get number of blocks in chain
        
        Returns:
            Chain length
        """
        return len(self.chain)


if __name__ == "__main__":
    # Test the blockchain
    print("=" * 60)
    print("BLOCKCHAIN TEST")
    print("=" * 60)
    
    # Create blockchain
    bc = Blockchain(difficulty=0)
    
    # Add some blocks
    bc.add_block({
        "type": "ipfs_file_metadata",
        "file_id": "test-123",
        "file_name": "test.txt",
        "ipfs_cid": "QmTest123",
        "file_size": 1024
    })
    
    bc.add_block({
        "type": "ipfs_file_metadata",
        "file_id": "test-456",
        "file_name": "document.pdf",
        "ipfs_cid": "QmTest456",
        "file_size": 2048
    })
    
    # Validate chain
    print("\n" + "=" * 60)
    print("VALIDATION TEST")
    print("=" * 60)
    is_valid = bc.is_chain_valid()
    print(f"Chain valid: {is_valid}")
    
    # Show chain
    print("\n" + "=" * 60)
    print("BLOCKCHAIN CONTENTS")
    print("=" * 60)
    for block in bc.chain:
        print(f"\nBlock #{block.index}")
        print(f"  Hash: {block.hash[:16]}...")
        print(f"  Previous: {block.previous_hash[:16]}...")
        print(f"  Data: {block.data}")
