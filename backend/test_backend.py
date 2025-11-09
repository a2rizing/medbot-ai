"""
Quick test script to verify backend is working correctly
"""

import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test if backend is running"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Backend is running!")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Is it running?")
        print("  Start it with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_predict_endpoint():
    """Test prediction endpoint with a dummy image"""
    print("\nTesting prediction endpoint...")
    try:
        # Create a small test image
        from PIL import Image
        import io
        
        img = Image.new('RGB', (224, 224), color='gray')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/predict", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Prediction endpoint works!")
            print(f"  Prediction: {result.get('prediction')}")
            print(f"  Confidence: {result.get('confidence')}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error testing prediction: {e}")
        return False

def test_model_file():
    """Check if model file exists"""
    print("\nChecking model file...")
    if os.path.exists("densepneumo_ace.pt"):
        size_mb = os.path.getsize("densepneumo_ace.pt") / (1024 * 1024)
        print(f"✓ Model file found: {size_mb:.1f} MB")
        return True
    else:
        print("✗ Model file not found: densepneumo_ace.pt")
        print("  Please place your model weights in the backend directory")
        return False

def main():
    print("="*60)
    print("MedBot-AI Backend Quick Test")
    print("="*60)
    
    results = []
    
    # Test 1: Model file
    results.append(test_model_file())
    
    # Test 2: Health check
    results.append(test_health_check())
    
    # Test 3: Prediction endpoint (only if backend is running)
    if results[-1]:
        results.append(test_predict_endpoint())
    
    # Summary
    print("\n" + "="*60)
    if all(results):
        print("✓ All tests passed! Backend is working correctly.")
        print("\nNext steps:")
        print("1. Test with a real X-ray image")
        print("2. Run evaluation: python evaluate_model.py")
        print("3. Deploy to AWS: see AWS_DEPLOYMENT_GUIDE.md")
    else:
        print("⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Start backend: uvicorn main:app --reload")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Place model file: densepneumo_ace.pt in backend/")
    print("="*60)

if __name__ == "__main__":
    main()
