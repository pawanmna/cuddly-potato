"""
Core modules for blockchain and IPFS functionality
"""

from .blockchain import Block, Blockchain
from .ipfs_manager import IPFSManager

__all__ = ['Block', 'Blockchain', 'IPFSManager', 'IPFSFileManager']

# IPFSFileManager imported lazily to avoid circular import issues
def get_ipfs_file_manager():
    from .ipfs_file_manager import IPFSFileManager
    return IPFSFileManager
