"""
Quick API health check test
"""
import requests
import sys

def test_api_health():
    """Test if API is running and responding"""
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        print(f"✓ Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Test docs endpoint
        response = requests.get("http://localhost:8000/docs")
        print(f"✓ Docs endpoint: {response.status_code}")
        
        print("\n✓ API is running successfully!")
        print("  Swagger UI: http://localhost:8000/docs")
        print("  ReDoc: http://localhost:8000/redoc")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API at http://localhost:8000")
        print("  Make sure the server is running:")
        print("  cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api_health()
    sys.exit(0 if success else 1)
