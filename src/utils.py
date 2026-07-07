"""
Utility functions for the screen time monitor.
"""

import yaml
from pathlib import Path
from typing import Dict
import cv2
import numpy as np


def load_config(config_path: str = "config.yaml") -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def draw_stats_overlay(frame: np.ndarray, stats: Dict, tracker) -> np.ndarray:
    """
    Draw usage statistics overlay on frame.
    
    Args:
        frame: Input frame
        stats: Statistics dictionary
        tracker: UsageTracker instance for formatting
        
    Returns:
        Frame with stats overlay
    """
    overlay = frame.copy()
    height, width = frame.shape[:2]
    
    # Semi-transparent background
    cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Title
    cv2.putText(
        frame,
        "Screen Time Monitor",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    
    # Phone time
    phone_text = f"Phone:  {tracker.format_time(stats['phone_time'])}"
    cv2.putText(
        frame,
        phone_text,
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )
    
    # Laptop time
    laptop_text = f"Laptop: {tracker.format_time(stats['laptop_time'])}"
    cv2.putText(
        frame,
        laptop_text,
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )
    
    # Session duration
    session_text = f"Session: {tracker.format_time(stats['session_duration'])}"
    cv2.putText(
        frame,
        session_text,
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )
    
    return frame


def draw_help_text(frame: np.ndarray) -> np.ndarray:
    """
    Draw help text with keyboard shortcuts.
    
    Args:
        frame: Input frame
        
    Returns:
        Frame with help text
    """
    height, width = frame.shape[:2]
    
    help_texts = [
        "Q: Quit",
        "S: Save",
        "R: Reset"
    ]
    
    y_offset = height - 80
    for i, text in enumerate(help_texts):
        cv2.putText(
            frame,
            text,
            (width - 120, y_offset + i * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1
        )
    
    return frame


def check_camera_available(device_id: int = 0) -> bool:
    """
    Check if camera is available.
    
    Args:
        device_id: Camera device ID
        
    Returns:
        True if camera is available
    """
    cap = cv2.VideoCapture(device_id)
    if cap.isOpened():
        cap.release()
        return True
    return False


def get_optimal_frame_size(width: int, height: int, max_size: int = 640) -> tuple:
    """
    Calculate optimal frame size maintaining aspect ratio.
    
    Args:
        width: Original width
        height: Original height
        max_size: Maximum dimension
        
    Returns:
        Tuple of (new_width, new_height)
    """
    if width > height:
        if width > max_size:
            ratio = max_size / width
            return (max_size, int(height * ratio))
    else:
        if height > max_size:
            ratio = max_size / height
            return (int(width * ratio), max_size)
    
    return (width, height)
