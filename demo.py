"""
Demo script to test detection without full monitoring.
Useful for testing camera and detection setup.
"""

import cv2
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from detector import DeviceDetector
from utils import load_config


def run_demo():
    """Run a simple detection demo."""
    print("="*60)
    print("Screen Time Monitor - Detection Demo")
    print("="*60)
    print("\nThis demo shows real-time detection without time tracking.")
    print("Press 'q' to quit\n")
    
    # Load config
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return
    
    # Initialize detector
    print("Initializing detector...")
    try:
        detector = DeviceDetector(config)
    except Exception as e:
        print(f"Error initializing detector: {e}")
        return
    
    # Initialize camera
    print("Opening camera...")
    cap = cv2.VideoCapture(config['camera']['device_id'])
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera']['width'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera']['height'])
    
    print("\nDemo running! Point camera at phone or laptop to test detection.")
    print("Press 'q' to quit\n")
    
    frame_count = 0
    start_time = time.time()
    detection_counts = {'phone': 0, 'laptop': 0}
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            frame_count += 1
            
            # Detect devices
            detections = detector.detect(frame)
            
            # Count detections
            if detections['phone']:
                detection_counts['phone'] += 1
            if detections['laptop']:
                detection_counts['laptop'] += 1
            
            # Draw detections
            display_frame = detector.draw_detections(frame, detections)
            
            # Add demo info
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            
            # Info overlay
            cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Frames: {frame_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Detection status
            phone_status = "✓ PHONE DETECTED" if detections['phone'] else "✗ No phone"
            laptop_status = "✓ LAPTOP DETECTED" if detections['laptop'] else "✗ No laptop"
            
            color_phone = (0, 255, 0) if detections['phone'] else (0, 0, 255)
            color_laptop = (0, 255, 0) if detections['laptop'] else (0, 0, 255)
            
            cv2.putText(display_frame, phone_status, (10, display_frame.shape[0] - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_phone, 2)
            cv2.putText(display_frame, laptop_status, (10, display_frame.shape[0] - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_laptop, 2)
            
            # Show frame
            cv2.imshow('Detection Demo - Press Q to quit', display_frame)
            
            # Handle keyboard
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n\nDemo interrupted")
    
    finally:
        # Cleanup and stats
        cap.release()
        cv2.destroyAllWindows()
        
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed if elapsed > 0 else 0
        
        print("\n" + "="*60)
        print("Demo Summary")
        print("="*60)
        print(f"Duration:         {elapsed:.1f}s")
        print(f"Frames Processed: {frame_count}")
        print(f"Average FPS:      {avg_fps:.1f}")
        print(f"Phone Detections: {detection_counts['phone']}")
        print(f"Laptop Detections: {detection_counts['laptop']}")
        print("="*60)
        
        if detection_counts['phone'] > 0 or detection_counts['laptop'] > 0:
            print("\n✓ Detection is working!")
            print("You can now run the full monitor: python src/main.py")
        else:
            print("\nℹ No devices detected during demo")
            print("Try adjusting:")
            print("  - Camera angle and position")
            print("  - Lighting conditions")
            print("  - confidence_threshold in config.yaml")


if __name__ == "__main__":
    run_demo()
