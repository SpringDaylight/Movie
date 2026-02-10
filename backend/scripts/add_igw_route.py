"""
Add Internet Gateway route to RDS subnet's route table
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
    """Add IGW route to route table"""
    
    # Get AWS credentials
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
    
    print("=" * 80)
    print("ADD INTERNET GATEWAY ROUTE TO RDS SUBNET")
    print("=" * 80)
    
    try:
        # Create EC2 client
        ec2 = boto3.client(
            'ec2',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # RDS subnet and IGW
        rds_subnet_id = 'subnet-0440a26d844a240f2'
        igw_id = 'igw-09dab637e6f89ed2f'
        
        print(f"\n[1] Finding route table for subnet {rds_subnet_id}...")
        
        # Find route table associated with RDS subnet
        rt_response = ec2.describe_route_tables(
            Filters=[
                {'Name': 'association.subnet-id', 'Values': [rds_subnet_id]}
            ]
        )
        
        if not rt_response['RouteTables']:
            # Check for main route table
            print("  No explicit association found. Checking main route table...")
            
            # Get VPC ID from subnet
            subnet_response = ec2.describe_subnets(SubnetIds=[rds_subnet_id])
            vpc_id = subnet_response['Subnets'][0]['VpcId']
            
            rt_response = ec2.describe_route_tables(
                Filters=[
                    {'Name': 'vpc-id', 'Values': [vpc_id]},
                    {'Name': 'association.main', 'Values': ['true']}
                ]
            )
        
        if not rt_response['RouteTables']:
            print("❌ Could not find route table!")
            return
        
        rt = rt_response['RouteTables'][0]
        rt_id = rt['RouteTableId']
        
        print(f"✓ Found route table: {rt_id}")
        
        # Check current routes
        print(f"\n[2] Current routes:")
        for route in rt['Routes']:
            dest = route.get('DestinationCidrBlock', route.get('DestinationIpv6CidrBlock', 'N/A'))
            target = route.get('GatewayId', route.get('NatGatewayId', route.get('NetworkInterfaceId', 'local')))
            state = route.get('State', 'N/A')
            print(f"  {dest} -> {target} ({state})")
        
        # Check if IGW route already exists
        has_igw_route = any(
            route.get('DestinationCidrBlock') == '0.0.0.0/0' and 
            route.get('GatewayId', '').startswith('igw-')
            for route in rt['Routes']
        )
        
        if has_igw_route:
            print(f"\n✓ IGW route already exists!")
            print(f"  No changes needed.")
            return
        
        # Add IGW route
        print(f"\n[3] Adding Internet Gateway route...")
        print(f"  Route: 0.0.0.0/0 -> {igw_id}")
        
        ec2.create_route(
            RouteTableId=rt_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id
        )
        
        print(f"✓ Route added successfully!")
        
        # Verify
        print(f"\n[4] Verifying new routes...")
        rt_response = ec2.describe_route_tables(RouteTableIds=[rt_id])
        rt = rt_response['RouteTables'][0]
        
        for route in rt['Routes']:
            dest = route.get('DestinationCidrBlock', route.get('DestinationIpv6CidrBlock', 'N/A'))
            target = route.get('GatewayId', route.get('NatGatewayId', route.get('NetworkInterfaceId', 'local')))
            state = route.get('State', 'N/A')
            print(f"  {dest} -> {target} ({state})")
        
        print("\n" + "=" * 80)
        print("✓ SUCCESS!")
        print("=" * 80)
        print("\nThe RDS subnet now has internet access via Internet Gateway.")
        print("You can now connect to your RDS instance from the internet.")
        print("\nTest the connection:")
        print("  Test-NetConnection movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com -Port 5432")
        print("\nOr run:")
        print("  python backend/tests/db_connection_check.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
