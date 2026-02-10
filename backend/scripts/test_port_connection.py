"""
Test network connectivity to RDS
"""
import socket
import sys

def test_connection(host, port, timeout=5):
    """Test if a port is open on a host"""
    print(f"Testing connection to {host}:{port}...")
    print(f"Timeout: {timeout} seconds")
    print("-" * 60)
    
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Try to connect
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ SUCCESS: Port {port} is OPEN on {host}")
            print(f"  The port is accessible from your network.")
            return True
        else:
            print(f"❌ FAILED: Port {port} is CLOSED or FILTERED on {host}")
            print(f"  Error code: {result}")
            print(f"\n  Possible reasons:")
            print(f"  1. Security group does not allow port {port}")
            print(f"  2. Network ACL is blocking the connection")
            print(f"  3. RDS is not publicly accessible")
            print(f"  4. Firewall is blocking the connection")
            return False
            
    except socket.gaierror as e:
        print(f"❌ DNS ERROR: Could not resolve hostname {host}")
        print(f"  Error: {e}")
        return False
    except socket.timeout:
        print(f"❌ TIMEOUT: Connection timed out after {timeout} seconds")
        print(f"  The host is not responding on port {port}")
        print(f"\n  This usually means:")
        print(f"  - Security group is blocking the connection")
        print(f"  - Network ACL is blocking the connection")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("=" * 60)
    print("RDS Port Connectivity Test")
    print("=" * 60)
    print()
    
    # RDS details
    host = "movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com"
    port = 5432
    
    # Test connection
    success = test_connection(host, port, timeout=10)
    
    print()
    print("=" * 60)
    if success:
        print("✓ Port is accessible - Database connection should work")
        print("  If DB connection still fails, check:")
        print("  - Database credentials")
        print("  - SSL/TLS configuration")
    else:
        print("❌ Port is NOT accessible - Fix security group first")
        print("\n  To fix:")
        print("  1. Go to AWS Console → EC2 → Security Groups")
        print("  2. Select security group: sg-0ab0cf159872aabb4")
        print("  3. Edit Inbound Rules")
        print("  4. Add rule:")
        print("     - Type: PostgreSQL")
        print("     - Protocol: TCP")
        print("     - Port: 5432")
        print("     - Source: 118.218.200.33/32")
    print("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
