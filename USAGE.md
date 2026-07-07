# Usage Guide

Complete guide to using the Screen Time Monitor.

## Quick Start

### 1. First Time Setup

Run the quick start script to verify everything is working:

```bash
python quick_start.py
```

This will:
- Check all dependencies
- Verify camera access
- Download the detection model
- Test GPU availability

### 2. Start Monitoring

**Windows:**
```bash
run_monitor.bat
```

**Linux/macOS:**
```bash
python src/main.py
```

### 3. Using the Monitor

Once started, you'll see a window with:
- Live camera feed
- Bounding boxes around detected devices
- Real-time usage timers
- Keyboard shortcuts help

**Keyboard Controls:**
- **Q** - Quit and save session
- **S** - Save current session (without quitting)
- **R** - Reset timers to zero

### 4. View Statistics

After running a few sessions, view your statistics:

```bash
python src/stats.py
```

Choose from:
1. View summary statistics
2. View daily breakdown
3. Plot usage graphs
4. All of the above

## Configuration

Edit `config.yaml` to customize behavior.

### Camera Settings

```yaml
camera:
  device_id: 0      # Change if you have multiple cameras (0, 1, 2...)
  width: 640        # Resolution width
  height: 480       # Resolution height
  fps: 30          # Frames per second
```

### Detection Settings

```yaml
detection:
  model: "yolov8n.pt"              # Model size (n=nano, s=small, m=medium)
  confidence_threshold: 0.5         # Detection confidence (0.3-0.7)
  process_every_n_frames: 3         # Process every Nth frame (optimization)
  device: "cpu"                     # Use "cuda" for GPU acceleration
```

**Model Options:**
- `yolov8n.pt` - Fastest, lowest accuracy (recommended for CPU)
- `yolov8s.pt` - Balanced (recommended for GPU)
- `yolov8m.pt` - High accuracy, slower

### Tracking Settings

```yaml
tracking:
  min_detection_time: 1.0    # Minimum seconds to count (reduces false positives)
  save_interval: 30          # Auto-save every N seconds
```

### Display Settings

```yaml
display:
  show_feed: true         # Show camera window
  show_boxes: true        # Show detection boxes
  show_labels: true       # Show device labels
  show_confidence: true   # Show confidence scores
  show_timer: true        # Show usage timers
```

**Headless Mode** (no window, background monitoring):
```yaml
display:
  show_feed: false
```

## Advanced Usage

### Running in Background (Headless)

1. Disable display in config:
```yaml
display:
  show_feed: false
```

2. Run in background:
```bash
python src/main.py > monitor.log 2>&1 &
```

3. Stop with:
```bash
pkill -f "python src/main.py"
```

### Multiple Cameras

To monitor multiple locations, run separate instances:

```bash
# Terminal 1 - Camera 0
python src/main.py --camera 0

# Terminal 2 - Camera 1
python src/main.py --camera 1
```

### Scheduled Monitoring

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Start program
5. Program: `python`
6. Arguments: `path\to\src\main.py`

**Linux/macOS Cron:**
```bash
# Edit crontab
crontab -e

# Add entry (run daily at 9 AM)
0 9 * * * cd /path/to/project && python src/main.py
```

### Export Statistics

Statistics are saved in JSON format at `data/sessions.json`.

You can process this data with any tool:

**Python:**
```python
import json
with open('data/sessions.json') as f:
    sessions = json.load(f)
    
# Analyze as needed
total_phone_time = sum(s['phone_time'] for s in sessions)
```

**Excel/Google Sheets:**
1. Open `data/sessions.json`
2. Import as JSON
3. Create charts and reports

### Custom Analysis

Create custom analysis scripts:

```python
from src.utils import load_config
from src.stats import StatsViewer

viewer = StatsViewer()
sessions = viewer.load_sessions()

# Your custom analysis here
for session in sessions:
    if session['phone_time'] > 3600:  # More than 1 hour
        print(f"High phone usage: {session['timestamp']}")
```

## Tips and Best Practices

### Optimal Camera Placement

- **Position camera to capture your typical working area**
- Ensure devices are visible when in use
- Avoid backlighting (don't face window)
- Stable mount reduces false detections

### Reducing False Positives

1. Increase confidence threshold:
```yaml
detection:
  confidence_threshold: 0.6  # Higher = fewer false positives
```

2. Increase minimum detection time:
```yaml
tracking:
  min_detection_time: 2.0  # Only count if seen for 2+ seconds
```

### Improving Accuracy

1. Use better model:
```yaml
detection:
  model: "yolov8s.pt"  # More accurate than nano
```

2. Reduce frame skipping:
```yaml
detection:
  process_every_n_frames: 2  # Process more frames
```

3. Increase resolution:
```yaml
camera:
  width: 1280
  height: 720
```

### Performance Tuning

**For slow computers:**
```yaml
detection:
  model: "yolov8n.pt"
  process_every_n_frames: 5
camera:
  width: 320
  height: 240
```

**For powerful computers:**
```yaml
detection:
  model: "yolov8s.pt"
  process_every_n_frames: 2
  device: "cuda"
camera:
  width: 1280
  height: 720
```

## Troubleshooting

### "Camera not available"
- Close other applications using camera (Zoom, Skype, etc.)
- Try different device_id in config (0, 1, 2...)
- Check camera permissions in OS settings

### "Model download failed"
- Check internet connection
- Download manually from https://github.com/ultralytics/assets/releases
- Place `yolov8n.pt` in project root

### "Low FPS / Laggy"
- Increase `process_every_n_frames`
- Use smaller model (`yolov8n.pt`)
- Reduce resolution
- Enable GPU if available

### "Not detecting devices"
- Lower `confidence_threshold` to 0.3
- Improve lighting
- Ensure device is clearly visible
- Try different camera angle

### "Too many false detections"
- Increase `confidence_threshold` to 0.6-0.7
- Increase `min_detection_time`
- Use better model (`yolov8s.pt`)

## Data Privacy

- All processing is **local** - no data is sent to cloud
- Camera feed is not recorded
- Only time statistics are saved
- Delete `data/` folder to remove all history

## Integration Ideas

### Productivity Apps

Export data to:
- RescueTime
- Toggl
- Custom dashboards

### Parental Controls

Monitor children's device usage:
- Set time limits
- Generate reports
- Alert on excessive usage

### Research

Academic studies on:
- Screen time patterns
- Device usage behavior
- Productivity correlation

### Wellness Apps

Track digital wellbeing:
- Compare with health metrics
- Set healthy limits
- Monitor progress

## Support

For issues, questions, or feature requests:
- Check INSTALL.md for setup issues
- Check OPTIMIZATION.md for performance tuning
- Review config.yaml comments
- Create GitHub issue with logs

## Next Steps

1. Run `quick_start.py` to verify setup
2. Start monitoring with default settings
3. Run for a few days to collect data
4. Review statistics and adjust config
5. Optimize for your specific needs

Happy monitoring! 📊
