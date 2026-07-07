"""
Quick start script to test the system and verify everything is working.
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed."""
    print("Checking dependencies...")
    
    required = {
        'cv2': 'opencv-python',
        'torch': 'torch',
        'ultralytics': 'ultralytics',
        'yaml': 'PyYAML',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\nPlease install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\nAll dependencies installed!")
    return True


def check_camera():
    """Check if camera is available."""
    print("\nChecking camera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("  ✓ Camera is available")
            cap.release()
            return True
        else:
            print("  ✗ Camera not found")
            print("  Make sure your webcam is connected and not in use")
            return False
    except Exception as e:
        print(f"  ✗ Error checking camera: {e}")
        return False


def check_gpu():
    """Check if GPU is available for acceleration."""
    print("\nChecking GPU support...")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"  ✓ GPU available: {gpu_name}")
            print("  You can use GPU acceleration by setting device: 'cuda' in config.yaml")
            return True
        else:
            print("  ℹ No GPU detected (will use CPU)")
            print("  This is fine - the system will work with CPU")
            return False
    except Exception as e:
        print(f"  ℹ GPU check failed: {e}")
        return False


def download_model():
    """Test model download."""
    print("\nTesting model download...")
    
    try:
        from ultralytics import YOLO
        import numpy as np
        
        print("  Downloading YOLOv8 nano model (first time only)...")
        model = YOLO('yolov8n.pt')
        
        # Test inference
        print("  Testing inference...")
        dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
        _ = model(dummy_img, verbose=False)
        
        print("  ✓ Model ready!")
        return True
    except Exception as e:
        print(f"  ✗ Model test failed: {e}")
        return False


def create_data_directory():
    """Create data directory if it doesn't exist."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"\n✓ Data directory ready: {data_dir.absolute()}")




def main():
    """Run all checks."""
    print("="*60)
    print("Screen Time Monitor - Quick Start Check")
    print("="*60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Camera", check_camera),
        ("GPU", check_gpu),
        ("Model", download_model),
    ]
    
    results = {}
    for name, check_func in checks:
        results[name] = check_func()
    
    create_data_directory()
    
    # Summary
    print("\n" + "="*60)
    print("SETUP SUMMARY")
    print("="*60)
    
    critical_checks = ["Dependencies", "Camera", "Model"]
    all_critical_passed = all(results.get(name, False) for name in critical_checks)
    
    if all_critical_passed:
        print("✓ All critical checks passed!")
        print("\nYou're ready to start monitoring!")
        print("\nRun the monitor with:")
        print("  python src/main.py")
        print("\nOr on Windows:")
        print("  run_monitor.bat")
    else:
        print("✗ Some critical checks failed")
        print("\nPlease fix the issues above before running the monitor")
    
    print("="*60)


if __name__ == "__main__":
    main()
