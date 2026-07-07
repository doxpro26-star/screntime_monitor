# Getting Started with Screen Time Monitor

Welcome! This guide will get you up and running in under 10 minutes.

## What This Does

Screen Time Monitor uses your webcam and AI to automatically track how much time you spend using your phone and laptop. Everything runs locally on your computer - no cloud, no data collection, completely private.

## Prerequisites

- Windows/Linux/macOS computer
- Webcam (built-in or USB)
- Python 3.8 or newer
- 2-3 GB free disk space

## Installation Steps

### Step 1: Install Python Dependencies

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install OpenCV, PyTorch, YOLOv8, and other dependencies. It may take 5-10 minutes.

### Step 2: Verify Setup

Run the quick start script:

```bash
python quick_start.py
```

This will:
- ✓ Check all dependencies are installed
- ✓ Verify your camera works
- ✓ Download the AI model (~6MB, one-time)
- ✓ Test GPU availability

If all checks pass, you're ready!

### Step 3: Test Detection

Run a quick demo to test detection:

**Windows:**
```bash
run_demo.bat
```

**Linux/macOS:**
```bash
python demo.py
```

Point your camera at a phone or laptop. You should see green boxes appear around detected devices.

Press 'Q' to quit.

### Step 4: Start Monitoring

Now start the full monitor:

**Windows:**
```bash
run_monitor.bat
```

**Linux/macOS:**
```bash
python src/main.py
```

You'll see:
- Live camera feed
- Green boxes around phones
- Blue boxes around laptops  
- Timers showing usage time

### Step 5: Use It!

**Keyboard Controls:**
- **Q** - Quit and save
- **S** - Save current session
- **R** - Reset timers

Let it run for a while to collect data!

### Step 6: View Statistics

After running a few sessions, view your stats:

```bash
python src/stats.py
```

Choose an option to see:
- Summary statistics
- Daily breakdown
- Usage graphs

## Understanding the Results

The monitor tracks two metrics:

1. **Phone Time** - Total time your phone was visible in the camera
2. **Laptop Time** - Total time your laptop was visible

It also shows:
- Session duration (total monitoring time)
- Percentage of time spent on each device

## Common Questions

### Q: Does it record video?
**A:** No! Only statistics (time numbers) are saved. Video is never recorded.

### Q: Does it work offline?
**A:** Yes! 100% offline after initial model download.

### Q: How accurate is it?
**A:** Very accurate for detecting if devices are present. Not meant for precise second-by-second tracking, but great for understanding overall usage patterns.

### Q: Will it slow down my computer?
**A:** Minimal impact. Uses 20-30% CPU on most computers. Can be optimized further (see OPTIMIZATION.md).

### Q: What if I have multiple devices?
**A:** It tracks any phone and any laptop in view. Multiple phones count as "phone time", multiple laptops as "laptop time".

### Q: Can I monitor someone else?
**A:** Yes, but inform them! This tool is for consensual monitoring only (self-tracking, parental controls with child's knowledge, etc.).

## Next Steps

### Customize Settings

Edit `config.yaml` to change:
- Camera resolution
- Detection sensitivity
- Frame processing speed
- Display options

### Run in Background

To monitor without the window:

1. Edit `config.yaml`:
```yaml
display:
  show_feed: false
```

2. Run normally - it will work in background

### Scheduled Monitoring

Set up Windows Task Scheduler or cron job to run automatically at certain times.

See USAGE.md for details.

### Analyze Your Data

After a week of data, look for patterns:
- What time of day do you use devices most?
- Which device do you use more?
- Are weekends different from weekdays?
- How does usage correlate with productivity?

Use this awareness to make informed changes to your habits.

## Troubleshooting

### Camera not working
- Close other apps using camera (Zoom, Skype, etc.)
- Try `device_id: 1` or `2` in config.yaml if you have multiple cameras

### Not detecting devices
- Improve lighting
- Move camera closer
- Lower `confidence_threshold` in config.yaml to `0.3`

### Too slow
- Increase `process_every_n_frames` to `5` in config.yaml
- Lower resolution to `320x240`

### False detections
- Increase `confidence_threshold` to `0.6`
- Increase `min_detection_time` to `2.0`

For more help, see:
- **INSTALL.md** - Detailed installation
- **USAGE.md** - Complete usage guide
- **OPTIMIZATION.md** - Performance tuning

## Tips for Best Results

1. **Camera Placement**
   - Position where devices are visible when you use them
   - Stable mount (not handheld)
   - Avoid backlighting from windows

2. **Consistent Usage**
   - Run during your typical work/study time
   - Keep camera on for better data
   - Review stats weekly

3. **Privacy Settings**
   - Remember camera is active when running
   - Data stays on your computer
   - Can delete data/ folder anytime

4. **Realistic Expectations**
   - Meant for pattern awareness, not exact tracking
   - Some false positives/negatives are normal
   - Trends over days/weeks are most meaningful

## Project Files Quick Reference

- **src/main.py** - Main monitoring application
- **src/stats.py** - Statistics viewer
- **demo.py** - Quick detection test
- **config.yaml** - Settings
- **data/sessions.json** - Your usage data

## Getting Help

1. Check this guide first
2. Read USAGE.md for detailed instructions
3. Review config.yaml comments
4. Try demo.py to isolate issues
5. Check error messages carefully

## Success Checklist

✅ Python and dependencies installed  
✅ Camera working in demo.py  
✅ Model downloaded successfully  
✅ Devices detected in demo  
✅ Full monitor runs without errors  
✅ Stats viewer shows data  

If all checked, you're all set! 🎉

## What's Next?

1. **Customize** - Adjust config.yaml for your needs
2. **Automate** - Set up scheduled monitoring
3. **Analyze** - Review weekly statistics
4. **Optimize** - Tune performance if needed
5. **Act** - Use insights to improve habits

## Philosophy

This tool is about **awareness, not judgment**. Screen time isn't inherently bad - what matters is intentional use vs. mindless scrolling. Use this data to:

- Understand your patterns
- Make conscious choices
- Set boundaries
- Balance digital and physical life
- Improve focus and productivity

**Happy monitoring! 📊🎯**

---

*Need more details? Check out the other .md files in the project folder.*
