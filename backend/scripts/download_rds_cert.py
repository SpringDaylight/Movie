"""
Download AWS RDS SSL certificate
"""
import os
import urllib.request
from pathlib import Path


def download_rds_certificate():
    """Download RDS global bundle certificate"""
    cert_url = "https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"
    cert_dir = Path("/certs")
    cert_path = cert_dir / "global-bundle.pem"
    
    # Create directory if it doesn't exist
    cert_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading RDS certificate from {cert_url}...")
    
    try:
        urllib.request.urlretrieve(cert_url, cert_path)
        print(f"✓ Certificate downloaded to {cert_path}")
        
        # Set permissions
        os.chmod(cert_path, 0o644)
        print(f"✓ Permissions set to 644")
        
        return True
    except Exception as e:
        print(f"✗ Failed to download certificate: {e}")
        return False


if __name__ == "__main__":
    import sys
    success = download_rds_certificate()
    sys.exit(0 if success else 1)
