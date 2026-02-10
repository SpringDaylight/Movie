import os
import json
import subprocess
import boto3
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ENV = os.getenv("ENV", "local")

DEFAULT_WEIGHTS = {
    "emotion": 0.4,
    "narrative": 0.4,
    "ending": 0.2
}

# AWS RDS Configuration
RDS_SECRET_ARN = os.getenv(
    "RDS_SECRET_ARN",
    "arn:aws:secretsmanager:ap-northeast-2:416963226971:secret:rds!db-f3aa3685-4bca-4982-bae8-c628e185fdf2-078IVh"
)
RDS_HOST = os.getenv("RDS_HOST", "movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com")
RDS_PORT = int(os.getenv("RDS_PORT", "5432"))
RDS_DATABASE = os.getenv("RDS_DATABASE", "movie")
RDS_USER = os.getenv("RDS_USER", "postgres")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")

# SSL Certificate path
SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/certs/global-bundle.pem")


def get_rds_password() -> str:
    """
    Retrieve RDS password from AWS Secrets Manager
    
    Returns:
        str: Database password
    """
    try:
        # Try using AWS CLI (for local development)
        result = subprocess.check_output([
            'bash', '-lc',
            f"aws secretsmanager get-secret-value --secret-id '{RDS_SECRET_ARN}' --query SecretString --output text"
        ]).decode()
        secret = json.loads(result)
        return secret['password']
    except Exception as e:
        print(f"Failed to get password via AWS CLI: {e}")
        
        # Fallback to boto3 (for production)
        try:
            client = boto3.client('secretsmanager', region_name=AWS_REGION)
            response = client.get_secret_value(SecretId=RDS_SECRET_ARN)
            secret = json.loads(response['SecretString'])
            return secret['password']
        except Exception as boto_error:
            print(f"Failed to get password via boto3: {boto_error}")
            raise RuntimeError(f"Could not retrieve RDS password: {boto_error}")


def get_database_url() -> str:
    """
    Construct database URL with password from Secrets Manager
    
    Returns:
        str: SQLAlchemy database URL
    """
    # Check if DATABASE_URL is explicitly set (for local override)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Local fallback without AWS dependencies
    if ENV.lower() == "local":
        return os.getenv(
            "LOCAL_DATABASE_URL",
            "postgresql+psycopg://movie_user:password@localhost:5432/movie_local",
        )
    
    # Get password from Secrets Manager
    password = get_rds_password()
    
    # Construct PostgreSQL URL
    # Format: postgresql://user:password@host:port/database
    return f"postgresql://{RDS_USER}:{password}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}"
