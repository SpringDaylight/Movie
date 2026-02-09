"""
Check and fix RDS public accessibility
"""
import os
import sys
from pathlib import Path
import boto3
from dotenv import load_dotenv

# Load environment variables
sys.path.append(str(Path(__file__).resolve().parents[1]))
load_dotenv(Path(__file__).resolve().parents[1] / '.env')

def main():
    """Check and fix RDS public accessibility"""
    
    # Get AWS credentials from environment
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
    
    if not aws_access_key or not aws_secret_key:
        print("❌ AWS credentials not found in .env file")
        sys.exit(1)
    
    print("=" * 70)
    print("RDS Public Accessibility Check & Fix")
    print("=" * 70)
    
    try:
        # Create RDS client
        rds = boto3.client(
            'rds',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        db_instance_id = 'movie-dev-db'
        
        print(f"\n[1] Fetching RDS instance: {db_instance_id}")
        
        # Get RDS instance details
        response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
        db_instance = response['DBInstances'][0]
        
        print(f"✓ Instance found: {db_instance['DBInstanceIdentifier']}")
        print(f"  Status: {db_instance['DBInstanceStatus']}")
        print(f"  Engine: {db_instance['Engine']} {db_instance['EngineVersion']}")
        print(f"  Endpoint: {db_instance['Endpoint']['Address']}:{db_instance['Endpoint']['Port']}")
        
        # Check public accessibility
        is_public = db_instance['PubliclyAccessible']
        
        print(f"\n[2] Public Accessibility Check:")
        print("-" * 70)
        print(f"  Current setting: {'YES (Public)' if is_public else 'NO (Private)'}")
        
        if is_public:
            print("  ✓ RDS is publicly accessible")
            print("\n  The security group is configured correctly.")
            print("  If connection still fails, check:")
            print("  1. Network ACLs in the VPC")
            print("  2. Route tables")
            print("  3. Local firewall settings")
        else:
            print("  ❌ RDS is NOT publicly accessible")
            print("  This is why the connection is failing!")
            print("\n  To fix this, we need to modify the RDS instance.")
            
            # Ask user for confirmation
            print("\n" + "=" * 70)
            print("IMPORTANT: Modifying RDS instance")
            print("=" * 70)
            print("This will enable public access to the RDS instance.")
            print("The change will be applied immediately and may cause a brief downtime.")
            print()
            
            user_input = input("Do you want to proceed? (yes/no): ").strip().lower()
            
            if user_input == 'yes':
                print("\n[3] Modifying RDS instance...")
                print("-" * 70)
                
                # Modify RDS instance to enable public access
                modify_response = rds.modify_db_instance(
                    DBInstanceIdentifier=db_instance_id,
                    PubliclyAccessible=True,
                    ApplyImmediately=True
                )
                
                print("✓ Modification request submitted!")
                print(f"  New status: {modify_response['DBInstance']['DBInstanceStatus']}")
                print("\n  The change is being applied...")
                print("  This may take a few minutes.")
                print("\n  Once the status changes to 'available', you can connect to the database.")
                print("\n  Check status with:")
                print(f"  python backend/scripts/fix_rds_access.py")
            else:
                print("\n  Modification cancelled.")
                print("  You can modify it manually in AWS Console:")
                print("  1. Go to RDS → Databases → movie-dev-db")
                print("  2. Click 'Modify'")
                print("  3. Under 'Connectivity', set 'Public access' to 'Yes'")
                print("  4. Click 'Continue' → 'Apply immediately' → 'Modify DB instance'")
        
        # Check VPC and Subnet info
        print(f"\n[4] Network Configuration:")
        print("-" * 70)
        print(f"  VPC ID: {db_instance['DBSubnetGroup']['VpcId']}")
        print(f"  Subnet Group: {db_instance['DBSubnetGroup']['DBSubnetGroupName']}")
        print(f"  Availability Zone: {db_instance['AvailabilityZone']}")
        
        # Check security groups
        print(f"\n[5] Security Groups:")
        print("-" * 70)
        for sg in db_instance['VpcSecurityGroups']:
            print(f"  - {sg['VpcSecurityGroupId']} ({sg['Status']})")
        
        print("\n" + "=" * 70)
        print("✓ Check completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
