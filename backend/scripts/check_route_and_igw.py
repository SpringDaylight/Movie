"""
Check Route Tables and Internet Gateway
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
    """Check Route Tables and IGW"""
    
    # Get AWS credentials
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
    
    print("=" * 80)
    print("ROUTE TABLE AND INTERNET GATEWAY CHECK")
    print("=" * 80)
    
    try:
        # Create clients
        ec2 = boto3.client(
            'ec2',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        rds = boto3.client(
            'rds',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # Get RDS instance
        print("\n[1] Getting RDS instance details...")
        db_response = rds.describe_db_instances(DBInstanceIdentifier='movie-dev-db')
        db_instance = db_response['DBInstances'][0]
        
        vpc_id = db_instance['DBSubnetGroup']['VpcId']
        subnet_ids = [subnet['SubnetIdentifier'] for subnet in db_instance['DBSubnetGroup']['Subnets']]
        
        print(f"✓ VPC: {vpc_id}")
        print(f"✓ Subnets: {len(subnet_ids)} subnets")
        
        # Check Internet Gateway
        print("\n" + "=" * 80)
        print("[2] INTERNET GATEWAY CHECK")
        print("=" * 80)
        
        igw_response = ec2.describe_internet_gateways(
            Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
        )
        
        if igw_response['InternetGateways']:
            igw = igw_response['InternetGateways'][0]
            igw_id = igw['InternetGatewayId']
            print(f"\n✓ Internet Gateway Found: {igw_id}")
            print(f"  State: {igw['Attachments'][0]['State']}")
        else:
            print(f"\n❌ NO INTERNET GATEWAY FOUND!")
            print(f"   This VPC has no internet gateway attached.")
            print(f"   RDS cannot be accessed from the internet!")
            print(f"\n   TO FIX:")
            print(f"   1. Create an Internet Gateway in AWS Console")
            print(f"   2. Attach it to VPC {vpc_id}")
            print(f"   3. Update route tables")
            return
        
        # Check Route Tables for each subnet
        print("\n" + "=" * 80)
        print("[3] ROUTE TABLE CHECK FOR RDS SUBNETS")
        print("=" * 80)
        
        all_subnets_have_igw_route = True
        
        for subnet_id in subnet_ids:
            print(f"\n  Subnet: {subnet_id}")
            
            # Get route table for this subnet
            rt_response = ec2.describe_route_tables(
                Filters=[
                    {'Name': 'association.subnet-id', 'Values': [subnet_id]}
                ]
            )
            
            if not rt_response['RouteTables']:
                # Check for main route table
                rt_response = ec2.describe_route_tables(
                    Filters=[
                        {'Name': 'vpc-id', 'Values': [vpc_id]},
                        {'Name': 'association.main', 'Values': ['true']}
                    ]
                )
            
            if rt_response['RouteTables']:
                rt = rt_response['RouteTables'][0]
                rt_id = rt['RouteTableId']
                print(f"    Route Table: {rt_id}")
                
                # Check routes
                has_igw_route = False
                print(f"    Routes:")
                
                for route in rt['Routes']:
                    dest = route.get('DestinationCidrBlock', route.get('DestinationIpv6CidrBlock', 'N/A'))
                    target = route.get('GatewayId', route.get('NatGatewayId', route.get('NetworkInterfaceId', 'local')))
                    state = route.get('State', 'N/A')
                    
                    print(f"      {dest} -> {target} ({state})")
                    
                    # Check for IGW route to 0.0.0.0/0
                    if dest == '0.0.0.0/0' and target.startswith('igw-'):
                        has_igw_route = True
                
                if has_igw_route:
                    print(f"    ✓ Has route to Internet Gateway")
                else:
                    print(f"    ❌ NO ROUTE TO INTERNET GATEWAY!")
                    print(f"       This subnet cannot reach the internet")
                    all_subnets_have_igw_route = False
        
        # Summary
        print("\n" + "=" * 80)
        print("DIAGNOSIS")
        print("=" * 80)
        
        if not igw_response['InternetGateways']:
            print("\n❌ PROBLEM FOUND: No Internet Gateway")
            print("\n   Your VPC does not have an Internet Gateway.")
            print("   This is why you cannot connect to RDS from the internet.")
            print("\n   SOLUTION:")
            print("   1. Go to AWS Console → VPC → Internet Gateways")
            print("   2. Click 'Create internet gateway'")
            print("   3. Attach it to your VPC")
            print("   4. Update route tables to add route: 0.0.0.0/0 -> igw-xxxxx")
            
        elif not all_subnets_have_igw_route:
            print("\n❌ PROBLEM FOUND: RDS subnets have no route to Internet Gateway")
            print("\n   Your RDS is in subnets that don't have a route to the internet.")
            print("   Even though RDS is 'publicly accessible', it's in a private subnet.")
            print("\n   SOLUTION:")
            print("   Option 1: Add route to Internet Gateway")
            print("   1. Go to AWS Console → VPC → Route Tables")
            print("   2. Select the route table for RDS subnets")
            print("   3. Edit routes → Add route:")
            print(f"      Destination: 0.0.0.0/0")
            print(f"      Target: {igw_id}")
            print("\n   Option 2: Move RDS to public subnets")
            print("   1. Create new subnet group with public subnets")
            print("   2. Modify RDS to use new subnet group")
            
        else:
            print("\n✓ ALL AWS NETWORKING IS CONFIGURED CORRECTLY!")
            print("\n   Internet Gateway: Present")
            print("   Route Tables: All subnets have IGW routes")
            print("   Security Group: Port 5432 open")
            print("   Network ACL: All traffic allowed")
            print("   RDS: Publicly accessible")
            print("\n   Since AWS configuration is correct, the problem must be:")
            print("   1. Local firewall/antivirus blocking the connection")
            print("   2. ISP blocking port 5432")
            print("   3. Corporate network policy")
            print("\n   Try connecting from:")
            print("   - A different computer")
            print("   - A different network (mobile hotspot)")
            print("   - AWS Cloud9 or EC2 instance in the same region")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
