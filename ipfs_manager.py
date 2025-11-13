"""
IPFS Manager for Decentralized File Storage
Handles IPFS operations: add, get, publish to IPNS, resolve IPNS
"""

import requests
import os
import json


class IPFSManager:
    """
    Manages interactions with IPFS daemon via HTTP API
    """
    
    def __init__(self, api_url="http://127.0.0.1:5001"):
        """
        Initialize IPFS manager
        
        Args:
            api_url: IPFS API endpoint (default: localhost:5001)
        """
        self.api_url = api_url
        self._check_connection()
    
    def _check_connection(self):
        """
        Verify IPFS daemon is running
        
        Raises:
            ConnectionError: If IPFS daemon is not accessible
        """
        try:
            response = requests.post(f"{self.api_url}/api/v0/version", timeout=5)
            if response.status_code == 200:
                version_info = response.json()
                print(f"Connected to IPFS (version {version_info.get('Version', 'unknown')})")
            else:
                raise ConnectionError("IPFS daemon not responding correctly")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Cannot connect to IPFS daemon at {self.api_url}\n"
                f"Make sure IPFS is running: 'ipfs daemon'\n"
                f"Error: {e}"
            )
    
    def add_file(self, file_path):
        """
        Add file to IPFS
        
        Args:
            file_path: Path to file to upload
            
        Returns:
            CID (Content Identifier) of uploaded file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If upload fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.api_url}/api/v0/add",
                    files=files,
                    timeout=300  # 5 minutes for large files
                )
            
            if response.status_code == 200:
                result = response.json()
                cid = result['Hash']
                size = result.get('Size', 0)
                print(f"Added to IPFS: {cid} ({size} bytes)")
                return cid
            else:
                raise Exception(f"IPFS add failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to add file to IPFS: {e}")
    
    def get_file(self, cid, output_path):
        """
        Download file from IPFS
        
        Args:
            cid: Content Identifier of file to download
            output_path: Where to save the downloaded file
            
        Returns:
            Path to downloaded file
            
        Raises:
            Exception: If download fails
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/v0/cat",
                params={'arg': cid},
                timeout=300,
                stream=True
            )
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = os.path.getsize(output_path)
                print(f"Downloaded from IPFS: {cid} ({file_size} bytes)")
                return output_path
            else:
                raise Exception(f"IPFS get failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download from IPFS: {e}")
    
    def publish_to_ipns(self, cid, key_name='self', lifetime='24h'):
        """
        Publish CID to IPNS (InterPlanetary Name System)
        
        Args:
            cid: Content Identifier to publish
            key_name: IPNS key to use (default: 'self' = peer ID)
            lifetime: How long the record is valid (default: 24h)
            
        Returns:
            IPNS name (e.g., /ipns/12D3KooW...)
            
        Raises:
            Exception: If publishing fails
        """
        try:
            params = {
                'arg': cid,
                'lifetime': lifetime,
                'allow-offline': 'true'  # Works with few peers
            }
            
            if key_name != 'self':
                params['key'] = key_name
            
            print(f"Publishing to IPNS (this may take 30-60 seconds)...")
            response = requests.post(
                f"{self.api_url}/api/v0/name/publish",
                params=params,
                timeout=90
            )
            
            if response.status_code == 200:
                result = response.json()
                ipns_key = result['Name']
                ipns_name = f"/ipns/{ipns_key}"
                print(f"Published to IPNS: {ipns_name}")
                print(f"  CID: {cid}")
                print(f"  Lifetime: {lifetime}")
                return ipns_name
            else:
                raise Exception(f"IPNS publish failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to publish to IPNS: {e}")
    
    def resolve_ipns(self, ipns_name, nocache=True, timeout=30):
        """
        Resolve IPNS name to current CID
        
        Args:
            ipns_name: IPNS name to resolve (e.g., /ipns/12D3Koo... or just peer ID)
            nocache: Force fresh lookup (default: True)
            timeout: Maximum time to wait in seconds (default: 30)
            
        Returns:
            Current CID for the IPNS name
            
        Raises:
            Exception: If resolution fails
        """
        # Clean the IPNS name
        ipns_key = ipns_name.replace('/ipns/', '').strip()
        
        try:
            params = {
                'arg': ipns_key,
                'nocache': 'true' if nocache else 'false',
                'dht-record-count': '1',  # Only need 1 record, faster
                'dht-timeout': f'{timeout}s'
            }
            
            print(f"Resolving IPNS: {ipns_key[:20]}... (max {timeout}s)")
            response = requests.post(
                f"{self.api_url}/api/v0/name/resolve",
                params=params,
                timeout=timeout + 5  # Allow extra time for HTTP
            )
            
            if response.status_code == 200:
                result = response.json()
                cid = result['Path'].replace('/ipfs/', '')
                print(f"Resolved to CID: {cid[:20]}...")
                return cid
            else:
                raise Exception(f"IPNS resolve failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"IPNS resolution timed out after {timeout} seconds. The peer may be offline or not connected to DHT.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to resolve IPNS: {e}")
    
    def get_peer_id(self):
        """
        Get the peer ID of this IPFS node
        
        Returns:
            Peer ID string (used as IPNS name)
            
        Raises:
            Exception: If unable to get peer ID
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/v0/id",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                peer_id = result['ID']
                return peer_id
            else:
                raise Exception(f"Failed to get peer ID: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get peer ID: {e}")
    
    def get_ipns_name(self):
        """
        Get the full IPNS name for this node
        
        Returns:
            IPNS name string (/ipns/...)
        """
        peer_id = self.get_peer_id()
        return f"/ipns/{peer_id}"
    
    def connect_to_peer(self, peer_address):
        """
        Connect directly to a peer
        
        Args:
            peer_address: Multiaddr of peer (e.g., /ip4/1.2.3.4/tcp/4001/p2p/12D3Koo...)
            
        Returns:
            True if successful
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/v0/swarm/connect",
                params={'arg': peer_address},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Connected to peer")
                return True
            else:
                print(f"Failed to connect to peer: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Peer connection error: {e}")
            return False
    
    def pin_file(self, cid):
        """
        Pin file to ensure it stays in local storage
        
        Args:
            cid: Content Identifier to pin
            
        Returns:
            True if successful
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/v0/pin/add",
                params={'arg': cid},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Pinned: {cid}")
                return True
            else:
                print(f"Pin failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Pin error: {e}")
            return False


if __name__ == "__main__":
    # Test IPFS manager
    print("=" * 60)
    print("IPFS MANAGER TEST")
    print("=" * 60)
    
    try:
        ipfs = IPFSManager()
        
        # Get peer ID
        print("\n" + "=" * 60)
        print("PEER ID")
        print("=" * 60)
        peer_id = ipfs.get_peer_id()
        print(f"Your Peer ID: {peer_id}")
        
        ipns_name = ipfs.get_ipns_name()
        print(f"Your IPNS: {ipns_name}")
        
        # Test with a simple file
        print("\n" + "=" * 60)
        print("FILE OPERATIONS")
        print("=" * 60)
        
        # Create test file
        test_file = "test_ipfs.txt"
        with open(test_file, 'w') as f:
            f.write("Hello IPFS! This is a test file.")
        
        # Add to IPFS
        cid = ipfs.add_file(test_file)
        print(f"File added with CID: {cid}")
        
        # Download from IPFS
        download_path = "test_ipfs_download.txt"
        ipfs.get_file(cid, download_path)
        
        with open(download_path, 'r') as f:
            content = f.read()
            print(f"Downloaded content: {content}")
        
        # Cleanup
        os.remove(test_file)
        os.remove(download_path)
        
        print("\nAll tests passed!")
        
    except ConnectionError as e:
        print(f"\n{e}")
        print("\nMake sure IPFS daemon is running:")
        print("  ipfs daemon")
    except Exception as e:
        print(f"\nError: {e}")
