"""
Statistics viewer for screen time monitoring data.
Analyzes and displays usage patterns from saved sessions.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from utils import load_config


class StatsViewer:
    """Analyze and display usage statistics."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize stats viewer.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.sessions_file = Path(self.config['storage']['session_file'])
    
    def load_sessions(self) -> List[Dict]:
        """
        Load all saved sessions.
        
        Returns:
            List of session dictionaries
        """
        if not self.sessions_file.exists():
            print("No session data found.")
            return []
        
        with open(self.sessions_file, 'r') as f:
            return json.load(f)
    
    def format_time(self, seconds: float) -> str:
        """Format seconds to HH:MM:SS."""
        return str(timedelta(seconds=int(seconds)))
    
    def print_summary(self) -> None:
        """Print summary statistics."""
        sessions = self.load_sessions()
        
        if not sessions:
            return
        
        print("\n" + "="*60)
        print("SCREEN TIME STATISTICS")
        print("="*60)
        
        # Overall stats
        total_phone = sum(s['phone_time'] for s in sessions)
        total_laptop = sum(s['laptop_time'] for s in sessions)
        total_session_time = sum(s['session_duration'] for s in sessions)
        
        print(f"\nTotal Sessions: {len(sessions)}")
        print(f"Total Monitoring Time: {self.format_time(total_session_time)}")
        print(f"\nTotal Phone Time:  {self.format_time(total_phone)}")
        print(f"Total Laptop Time: {self.format_time(total_laptop)}")
        
        if total_session_time > 0:
            print(f"\nPhone Usage:  {(total_phone/total_session_time*100):.1f}%")
            print(f"Laptop Usage: {(total_laptop/total_session_time*100):.1f}%")
        
        # Recent sessions
        print("\n" + "-"*60)
        print("RECENT SESSIONS (Last 5)")
        print("-"*60)
        
        for session in sessions[-5:]:
            timestamp = datetime.fromisoformat(session['timestamp'])
            print(f"\nSession: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Duration: {self.format_time(session['session_duration'])}")
            print(f"  Phone:    {self.format_time(session['phone_time'])} ({session['phone_percentage']:.1f}%)")
            print(f"  Laptop:   {self.format_time(session['laptop_time'])} ({session['laptop_percentage']:.1f}%)")
        
        print("\n" + "="*60)
    
    def plot_usage_over_time(self) -> None:
        """Plot usage over time."""
        sessions = self.load_sessions()
        
        if not sessions:
            print("No data to plot.")
            return
        
        timestamps = [datetime.fromisoformat(s['timestamp']) for s in sessions]
        phone_times = [s['phone_time'] / 60 for s in sessions]  # Convert to minutes
        laptop_times = [s['laptop_time'] / 60 for s in sessions]
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(timestamps, phone_times, 'g-o', label='Phone', linewidth=2)
        plt.plot(timestamps, laptop_times, 'b-o', label='Laptop', linewidth=2)
        plt.xlabel('Session Time')
        plt.ylabel('Usage Time (minutes)')
        plt.title('Device Usage Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Bar chart comparison
        plt.subplot(1, 2, 2)
        total_phone = sum(phone_times)
        total_laptop = sum(laptop_times)
        
        plt.bar(['Phone', 'Laptop'], [total_phone, total_laptop], color=['green', 'blue'])
        plt.ylabel('Total Usage Time (minutes)')
        plt.title('Total Device Usage')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def daily_summary(self) -> None:
        """Print daily usage summary."""
        sessions = self.load_sessions()
        
        if not sessions:
            return
        
        # Group by date
        daily_data = defaultdict(lambda: {'phone': 0, 'laptop': 0, 'duration': 0})
        
        for session in sessions:
            date = datetime.fromisoformat(session['timestamp']).date()
            daily_data[date]['phone'] += session['phone_time']
            daily_data[date]['laptop'] += session['laptop_time']
            daily_data[date]['duration'] += session['session_duration']
        
        print("\n" + "="*60)
        print("DAILY USAGE SUMMARY")
        print("="*60)
        
        for date in sorted(daily_data.keys()):
            data = daily_data[date]
            print(f"\n{date.strftime('%Y-%m-%d')}:")
            print(f"  Monitoring: {self.format_time(data['duration'])}")
            print(f"  Phone:      {self.format_time(data['phone'])}")
            print(f"  Laptop:     {self.format_time(data['laptop'])}")
        
        print("\n" + "="*60)


def main():
    """Entry point for stats viewer."""
    viewer = StatsViewer()
    
    print("\nScreen Time Monitor - Statistics Viewer")
    print("="*60)
    print("\n1. View Summary")
    print("2. View Daily Summary")
    print("3. Plot Usage Graphs")
    print("4. All of the above")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        viewer.print_summary()
    elif choice == '2':
        viewer.daily_summary()
    elif choice == '3':
        viewer.plot_usage_over_time()
    elif choice == '4':
        viewer.print_summary()
        viewer.daily_summary()
        viewer.plot_usage_over_time()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
