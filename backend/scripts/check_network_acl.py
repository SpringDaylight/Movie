"""
Check VPC Network ACLs
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
    """Check Network ACLs"""
    
    # Get AWS credentials from environment
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
    
    if not aws_access_key or not aws_secret_key:
        print("❌ AWS credentials not found in .env file")
        sys.exit(1)
    
    print("=" * 70)
    print("VPC Network ACL Check")
    print("=" * 70)
    
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
        
        # Get RDS instance to find VPC and subnets
        print("\n[1] Getting RDS instance details...")
        db_response = rds.describe_db_instances(DBInstanceIdentifier='movie-dev-db')
        db_instance = db_response['DBInstances'][0]
        
        vpc_id = db_instance['DBSubnetGroup']['VpcId']
        subnet_ids = [subnet['SubnetIdentifier'] for subnet in db_instance['DBSubnetGroup']['Subnets']]
        
        print(f"✓ VPC ID: {vpc_id}")
        print(f"✓ Subnets: {', '.join(subnet_ids)}")
        
        # Get Network ACLs for the VPC
        print(f"\n[2] Checking Network ACLs for VPC {vpc_id}...")
        print("-" * 70)
        
        acl_response = ec2.describe_network_acls(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]}
            ]
        )
        
        for acl in acl_response['NetworkAcls']:
            acl_id = acl['NetworkAclId']
            is_default = acl['IsDefault']
            
            print(f"\nNetwork ACL: {acl_id} {'(Default)' if is_default else ''}")
            
            # Check if this ACL is associated with RDS subnets
            associated_subnets = [assoc['SubnetId'] for assoc in acl['Associations']]
            rds_subnets = [s for s in associated_subnets if s in subnet_ids]
            
            if rds_subnets:
                print(f"  ✓ Associated with RDS subnets: {', '.join(rds_subnets)}")
            
            # Check Inbound rules
            print(f"\n  Inbound Rules:")
            inbound_entries = sorted([e for e in acl['Entries'] if not e['Egress']], 
                                    key=lambda x: x['RuleNumber'])
            
            postgres_allowed = False
            for entry in inbound_entries:
                rule_num = entry['RuleNumber']
                protocol = entry['Protocol']
                action = entry['RuleAction']
                cidr = entry.get('CidrBlock', entry.get('Ipv6CidrBlock', 'N/A'))
                
                # Protocol -1 means all, 6 means TCP
                port_range = ""
                if 'PortRange' in entry:
                    from_port = entry['PortRange']['From']
                    to_port = entry['PortRange']['To']
                    port_range = f" (Ports: {from_port}-{to_port})"
                    
                    # Check if port 5432 is allowed
                    if protocol in ['-1', '6'] and from_port <= 5432 <= to_port and action == 'allow':
                        postgres_allowed = True
                
                protocol_name = {'-1': 'ALL', '6': 'TCP', '17': 'UDP'}.get(protocol, protocol)
                
                print(f"    Rule {rule_num}: {action.upper()} {protocol_name}{port_range} from {cidr}")
            
            if postgres_allowed or any(e['Protocol'] == '-1' and e['RuleAction'] == 'allow' for e in inbound_entries):
                print(f"  ✓ PostgreSQL port 5432 is ALLOWED")
            else:
                print(f"  ❌ PostgreSQL port 5432 may be BLOCKED")
            
            # Check Outbound rules
            print(f"\n  Outbound Rules:")
            outbound_entries = sorted([e for e in acl['Entries'] if e['Egress']], 
                                     key=lambda x: x['RuleNumber'])
            
            for entry in outbound_entries:
                rule_num = entry['RuleNumber']
                protocol = entry['Protocol']
                action = entry['RuleAction']
                cidr = entry.get('CidrBlock', entry.get('Ipv6CidrBlock', 'N/A'))
                
                port_range = ""
                if 'PortRange' in entry:
                    from_port = entry['PortRange']['From']
                    to_port = entry['PortRange']['To']
                    port_range = f" (Ports: {from_port}-{to_port})"
                
                protocol_name = {'-1': 'ALL', '6': 'TCP', '17': 'UDP'}.get(protocol, protocol)
                
                print(f"    Rule {rule_num}: {action.upper()} {protocol_name}{port_range} to {cidr}")
        
        print("\n" + "=" * 70)
        print("✓ Network ACL check completed!")
        print("=" * 70)
        print("\nIf all rules look correct but connection still fails:")
        print("1. Check if there's a corporate firewall blocking outbound connections")
        print("2. Try connecting from a different network")
        print("3. Check if the RDS endpoint DNS resolves correctly")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
