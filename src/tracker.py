"""
Time tracking module for device usage monitoring.
Efficiently tracks and persists usage data.
"""

import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict


class UsageTracker:
    """Track device usage time with persistence."""
    
    def __init__(self, config: Dict):
        """
        Initialize tracker with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.min_detection_time = config['tracking']['min_detection_time']
        self.save_interval = config['tracking']['save_interval']
        
        # Initialize tracking state
        self.phone_time = 0.0
        self.laptop_time = 0.0
        self.phone_last_seen = None
        self.laptop_last_seen = None
        self.session_start = time.time()
        self.last_save_time = time.time()
        
        # Session metadata
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure data directory exists
        data_dir = Path(config['storage']['data_dir'])
        data_dir.mkdir(exist_ok=True)
        
        # Load existing session if available
        self._load_current_session()
    
    def update(self, detections: Dict) -> None:
        """
        Update tracking based on current detections.
        
        Args:
            detections: Detection results from detector
        """
        current_time = time.time()
        
        # Track phone usage
        if detections['phone']:
            if self.phone_last_seen is not None:
                elapsed = current_time - self.phone_last_seen
                if elapsed >= self.min_detection_time:
                    self.phone_time += elapsed
            self.phone_last_seen = current_time
        else:
            self.phone_last_seen = None
        
        # Track laptop usage
        if detections['laptop']:
            if self.laptop_last_seen is not None:
                elapsed = current_time - self.laptop_last_seen
                if elapsed >= self.min_detection_time:
                    self.laptop_time += elapsed
            self.laptop_last_seen = current_time
        else:
            self.laptop_last_seen = None
        
        # Auto-save periodically
        if current_time - self.last_save_time >= self.save_interval:
            self.save_current_session()
            self.last_save_time = current_time
    
    def get_usage_stats(self) -> Dict:
        """
        Get current usage statistics.
        
        Returns:
            Dictionary containing usage stats
        """
        session_duration = time.time() - self.session_start
        
        return {
            'session_id': self.session_id,
            'session_duration': session_duration,
            'phone_time': self.phone_time,
            'laptop_time': self.laptop_time,
            'phone_percentage': (self.phone_time / session_duration * 100) if session_duration > 0 else 0,
            'laptop_percentage': (self.laptop_time / session_duration * 100) if session_duration > 0 else 0,
        }
    
    def format_time(self, seconds: float) -> str:
        """
        Format seconds into human-readable time.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string (HH:MM:SS)
        """
        return str(timedelta(seconds=int(seconds)))
    
    def save_current_session(self) -> None:
        """Save current session to file."""
        stats = self.get_usage_stats()
        stats['timestamp'] = datetime.now().isoformat()
        
        session_file = Path(self.config['storage']['current_session_file'])
        session_file.parent.mkdir(exist_ok=True)
        
        with open(session_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def save_and_archive_session(self) -> None:
        """Save current session and archive to sessions history."""
        stats = self.get_usage_stats()
        stats['timestamp'] = datetime.now().isoformat()
        
        # Load existing sessions
        sessions_file = Path(self.config['storage']['session_file'])
        sessions_file.parent.mkdir(exist_ok=True)
        
        sessions = []
        if sessions_file.exists():
            with open(sessions_file, 'r') as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    sessions = []
        
        # Add current session
        sessions.append(stats)
        
        # Save updated sessions
        with open(sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        print(f"Session saved: {self.session_id}")
    
    def _load_current_session(self) -> None:
        """Load current session if it exists (for crash recovery)."""
        session_file = Path(self.config['storage']['current_session_file'])
        
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    
                # Check if session is recent (within last hour)
                session_time = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - session_time < timedelta(hours=1):
                    self.phone_time = data.get('phone_time', 0.0)
                    self.laptop_time = data.get('laptop_time', 0.0)
                    print("Resumed previous session")
            except (json.JSONDecodeError, KeyError, ValueError):
                pass
    
    def reset(self) -> None:
        """Reset tracking counters."""
        self.phone_time = 0.0
        self.laptop_time = 0.0
        self.phone_last_seen = None
        self.laptop_last_seen = None
        self.session_start = time.time()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print("Timers reset")
