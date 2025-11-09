"""
Backend Setup Verification Script
Run this to check if everything is configured correctly
"""

import os
import sys

def check_python_version():
    """Check Python version"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python version too old: {version.major}.{version.minor}")
        return False

def check_model_file():
    """Check if model weights file exists"""
    print("\n✓ Checking model file...")
    if os.path.exists("densepneumo_ace.pt"):
        size_mb = os.path.getsize("densepneumo_ace.pt") / (1024 * 1024)
        print(f"  ✓ Model file found: densepneumo_ace.pt ({size_mb:.1f} MB)")
        return True
    else:
        print("  ✗ Model file not found: densepneumo_ace.pt")
        print("    → Please place your model weights file in the backend directory")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n✓ Checking dependencies...")
    required = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} not installed")
            missing.append(name)
    
    if missing:
        print(f"\n  → Install missing packages: pip install {' '.join(missing.lower())}")
        return False
    return True

def check_main_file():
    """Check if main.py exists and is configured"""
    print("\n✓ Checking main.py...")
    if not os.path.exists("main.py"):
        print("  ✗ main.py not found")
        return False
    
    with open("main.py", "r") as f:
        content = f.read()
        
    checks = {
        'densepneumo_ace.pt': 'Model path configured',
        'FastAPI': 'FastAPI imported',
        '@app.post("/predict")': 'Predict endpoint defined',
    }
    
    all_good = True
    for check, desc in checks.items():
        if check in content:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc}")
            all_good = False
    
    return all_good

def check_gradcam():
    """Check if GradCAM utilities exist"""
    print("\n✓ Checking GradCAM utilities...")
    gradcam_path = "../model/gradcam_utils.py"
    
    if os.path.exists(gradcam_path):
        print(f"  ✓ GradCAM utilities found")
        return True
    else:
        print(f"  ⚠ GradCAM utilities not found at {gradcam_path}")
        print("    → GradCAM endpoint may not work, but basic prediction will work")
        return True  # Not critical

def check_logs_dir():
    """Check/create logs directory"""
    print("\n✓ Checking logs directory...")
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print("  ✓ Created logs directory")
    else:
        print("  ✓ Logs directory exists")
    return True

def test_model_loading():
    """Try to load the model"""
    print("\n✓ Testing model loading...")
    try:
        import torch
        import torch.nn as nn
        from torchvision import models
        
        model = models.densenet121(pretrained=False)
        model.classifier = nn.Linear(model.classifier.in_features, 1)
        
        if os.path.exists("densepneumo_ace.pt"):
            model.load_state_dict(torch.load("densepneumo_ace.pt", map_location='cpu'))
            print("  ✓ Model loaded successfully!")
            return True
        else:
            print("  ✗ Model file not found")
            return False
    except Exception as e:
        print(f"  ✗ Error loading model: {e}")
        return False

def print_next_steps(all_checks_passed):
    """Print what to do next"""
    print("\n" + "="*60)
    if all_checks_passed:
        print("🎉 All checks passed! Your backend is ready.")
        print("="*60)
        print("\nNext steps:")
        print("1. Start the backend:")
        print("   uvicorn main:app --host 0.0.0.0 --port 8000")
        print("\n2. Test in browser:")
        print("   http://localhost:8000")
        print("\n3. Run evaluation:")
        print("   python evaluate_model.py")
        print("\n4. Deploy to AWS:")
        print("   See AWS_DEPLOYMENT_GUIDE.md")
    else:
        print("⚠ Some checks failed. Please fix the issues above.")
        print("="*60)
        print("\nCommon fixes:")
        print("1. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n2. Place model file:")
        print("   Copy densepneumo_ace.pt to backend directory")
        print("\n3. Activate virtual environment:")
        print("   source venv/bin/activate  (Linux/Mac)")
        print("   venv\\Scripts\\activate.bat  (Windows)")

def main():
    print("="*60)
    print("MedBot-AI Backend Setup Verification")
    print("="*60)
    
    checks = [
        check_python_version(),
        check_model_file(),
        check_dependencies(),
        check_main_file(),
        check_gradcam(),
        check_logs_dir(),
        test_model_loading(),
    ]
    
    all_passed = all(checks)
    print_next_steps(all_passed)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
