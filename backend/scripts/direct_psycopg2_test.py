"""
Direct psycopg2 connection test with detailed error messages
"""
import psycopg2
import sys

def main():
    print("=" * 70)
    print("Direct psycopg2 Connection Test")
    print("=" * 70)
    
    host = "movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com"
    port = 5432
    database = "movie"
    user = "postgres"
    password = "peB63j)hVMvtor8*wPXwK9J[VmEJ"
    
    print(f"\nConnection parameters:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Database: {database}")
    print(f"  User: {user}")
    print(f"  Password: {'*' * len(password)}")
    
    print(f"\n[1] Attempting connection with SSL mode 'require'...")
    print("-" * 70)
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode='require',
            connect_timeout=10
        )
        
        print("✓ Connection successful!")
        
        # Test query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"✓ PostgreSQL version: {version[:60]}...")
        
        cur.execute("SELECT current_database(), current_user;")
        db_name, db_user = cur.fetchone()
        print(f"✓ Connected to database: {db_name}")
        print(f"✓ Connected as user: {db_user}")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ Connection test PASSED!")
        print("=" * 70)
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed!")
        print(f"\nError details:")
        print(f"  {str(e)}")
        
        error_str = str(e).lower()
        
        print(f"\n" + "=" * 70)
        print("Diagnosis:")
        print("=" * 70)
        
        if 'timeout' in error_str or 'timed out' in error_str:
            print("❌ CONNECTION TIMEOUT")
            print("\nThis means the network connection cannot be established.")
            print("\nPossible causes:")
            print("1. Corporate/ISP firewall blocking outbound port 5432")
            print("2. Antivirus software blocking the connection")
            print("3. Windows Firewall blocking Python")
            print("4. Network routing issue")
            print("\nSolutions to try:")
            print("1. Disable Windows Firewall temporarily and test")
            print("2. Try from a different network (mobile hotspot)")
            print("3. Check if your company requires VPN for AWS access")
            print("4. Contact your network administrator")
            
        elif 'authentication' in error_str or 'password' in error_str:
            print("❌ AUTHENTICATION FAILED")
            print("\nThe password is incorrect.")
            print("Check the password in .env file.")
            
        elif 'database' in error_str and 'does not exist' in error_str:
            print("❌ DATABASE NOT FOUND")
            print("\nThe database 'movie' does not exist on the server.")
            
        else:
            print(f"❌ UNKNOWN ERROR")
            print(f"\nError message: {e}")
        
        print("=" * 70)
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
