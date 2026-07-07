"""
Main application for screen time monitoring.
Real-time device usage tracking using computer vision.
"""

import cv2
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from detector import DeviceDetector
from tracker import UsageTracker
from utils import load_config, draw_stats_overlay, draw_help_text, check_camera_available


class ScreenTimeMonitor:
    """Main application class for screen time monitoring."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the monitor.
        
        Args:
            config_path: Path to configuration file
        """
        print("Initializing Screen Time Monitor...")
        
        # Load configuration
        self.config = load_config(config_path)
        
        # Check camera availability
        camera_id = self.config['camera']['device_id']
        if not check_camera_available(camera_id):
            raise RuntimeError(f"Camera {camera_id} not available!")
        
        # Initialize components
        self.detector = DeviceDetector(self.config)
        self.tracker = UsageTracker(self.config)
        
        # Frame processing optimization
        self.frame_skip = self.config['detection']['process_every_n_frames']
        self.frame_counter = 0
        self.last_detections = {'phone': [], 'laptop': []}
        
        print("Initialization complete!")
    
    def run(self) -> None:
        """Run the main monitoring loop."""
        # Initialize camera
        cap = cv2.VideoCapture(self.config['camera']['device_id'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera']['width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera']['height'])
        
        print("\n" + "="*50)
        print("Screen Time Monitor Running")
        print("="*50)
        print("\nControls:")
        print("  Q - Quit and save")
        print("  S - Save current session")
        print("  R - Reset timers")
        print("\nMonitoring started...\n")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Process frame for detection (with frame skipping for optimization)
                if self.frame_counter % self.frame_skip == 0:
                    self.last_detections = self.detector.detect(frame)
                    self.tracker.update(self.last_detections)
                
                self.frame_counter += 1
                
                # Draw visualizations if enabled
                if self.config['display']['show_feed']:
                    display_frame = frame.copy()
                    
                    # Draw bounding boxes
                    if self.config['display']['show_boxes']:
                        display_frame = self.detector.draw_detections(
                            display_frame,
                            self.last_detections
                        )
                    
                    # Draw statistics overlay
                    if self.config['display']['show_timer']:
                        stats = self.tracker.get_usage_stats()
                        display_frame = draw_stats_overlay(
                            display_frame,
                            stats,
                            self.tracker
                        )
                    
                    # Draw help text
                    display_frame = draw_help_text(display_frame)
                    
                    # Show frame
                    cv2.imshow('Screen Time Monitor', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\nQuitting...")
                    break
                elif key == ord('s'):
                    print("\nSaving session...")
                    self.tracker.save_current_session()
                    print("Session saved!")
                elif key == ord('r'):
                    print("\nResetting timers...")
                    self.tracker.reset()
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        finally:
            # Cleanup
            print("\nCleaning up...")
            self.tracker.save_and_archive_session()
            
            # Print final stats
            stats = self.tracker.get_usage_stats()
            print("\n" + "="*50)
            print("Session Summary")
            print("="*50)
            print(f"Session Duration: {self.tracker.format_time(stats['session_duration'])}")
            print(f"Phone Time:       {self.tracker.format_time(stats['phone_time'])} ({stats['phone_percentage']:.1f}%)")
            print(f"Laptop Time:      {self.tracker.format_time(stats['laptop_time'])} ({stats['laptop_percentage']:.1f}%)")
            print("="*50)
            
            cap.release()
            cv2.destroyAllWindows()
            print("\nGoodbye!")


def main():
    """Entry point for the application."""
    try:
        monitor = ScreenTimeMonitor()
        monitor.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
