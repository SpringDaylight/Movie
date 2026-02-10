"""
Check RDS Security Group rules
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
    """Check security group rules"""
    
    # Get AWS credentials from environment
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
    
    if not aws_access_key or not aws_secret_key:
        print("❌ AWS credentials not found in .env file")
        sys.exit(1)
    
    print("=" * 70)
    print("RDS Security Group Rules Check")
    print("=" * 70)
    
    try:
        # Create EC2 client
        ec2 = boto3.client(
            'ec2',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # Get security group details
        sg_id = 'sg-0ab0cf159872aabb4'
        print(f"\n[1] Fetching security group: {sg_id}")
        
        response = ec2.describe_security_groups(GroupIds=[sg_id])
        sg = response['SecurityGroups'][0]
        
        print(f"✓ Security Group Name: {sg['GroupName']}")
        print(f"✓ Description: {sg['Description']}")
        print(f"✓ VPC ID: {sg['VpcId']}")
        
        # Check Inbound Rules
        print(f"\n[2] Inbound Rules ({len(sg['IpPermissions'])} rules):")
        print("-" * 70)
        
        if not sg['IpPermissions']:
            print("⚠️  No inbound rules found!")
        
        for idx, rule in enumerate(sg['IpPermissions'], 1):
            protocol = rule.get('IpProtocol', 'N/A')
            from_port = rule.get('FromPort', 'N/A')
            to_port = rule.get('ToPort', 'N/A')
            
            print(f"\nRule #{idx}:")
            print(f"  Protocol: {protocol}")
            print(f"  Port Range: {from_port} - {to_port}")
            
            # Check IP ranges
            if rule.get('IpRanges'):
                print(f"  IP Ranges:")
                for ip_range in rule['IpRanges']:
                    cidr = ip_range.get('CidrIp', 'N/A')
                    desc = ip_range.get('Description', 'No description')
                    print(f"    - {cidr} ({desc})")
            
            # Check IPv6 ranges
            if rule.get('Ipv6Ranges'):
                print(f"  IPv6 Ranges:")
                for ip_range in rule['Ipv6Ranges']:
                    cidr = ip_range.get('CidrIpv6', 'N/A')
                    desc = ip_range.get('Description', 'No description')
                    print(f"    - {cidr} ({desc})")
            
            # Check security group references
            if rule.get('UserIdGroupPairs'):
                print(f"  Security Groups:")
                for sg_ref in rule['UserIdGroupPairs']:
                    sg_ref_id = sg_ref.get('GroupId', 'N/A')
                    print(f"    - {sg_ref_id}")
        
        # Check for PostgreSQL port
        print("\n" + "=" * 70)
        print("[3] PostgreSQL Port 5432 Check:")
        print("-" * 70)
        
        postgres_rules = []
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort')
            to_port = rule.get('ToPort')
            
            if from_port == 5432 or to_port == 5432:
                postgres_rules.append(rule)
        
        if postgres_rules:
            print(f"✓ Found {len(postgres_rules)} rule(s) for PostgreSQL port 5432")
            for rule in postgres_rules:
                if rule.get('IpRanges'):
                    for ip_range in rule['IpRanges']:
                        cidr = ip_range.get('CidrIp')
                        print(f"  ✓ Allowed from: {cidr}")
        else:
            print("❌ No rules found for PostgreSQL port 5432!")
            print("   This is why the connection is failing.")
            print("\n   To fix this, add an inbound rule:")
            print("   - Type: PostgreSQL")
            print("   - Protocol: TCP")
            print("   - Port: 5432")
            print("   - Source: 118.218.200.33/32 (your current IP)")
        
        # Check Outbound Rules
        print(f"\n[4] Outbound Rules ({len(sg['IpPermissionsEgress'])} rules):")
        print("-" * 70)
        
        for idx, rule in enumerate(sg['IpPermissionsEgress'], 1):
            protocol = rule.get('IpProtocol', 'N/A')
            from_port = rule.get('FromPort', 'All')
            to_port = rule.get('ToPort', 'All')
            
            print(f"\nRule #{idx}:")
            print(f"  Protocol: {protocol}")
            print(f"  Port Range: {from_port} - {to_port}")
            
            if rule.get('IpRanges'):
                for ip_range in rule['IpRanges']:
                    cidr = ip_range.get('CidrIp', 'N/A')
                    print(f"  Destination: {cidr}")
        
        print("\n" + "=" * 70)
        print("✓ Security group check completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
