# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Camera    │  │  Detection  │  │   Usage     │         │
│  │    Feed     │  │   Overlay   │  │   Timers    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  Keyboard: Q=Quit, S=Save, R=Reset                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     MAIN APPLICATION                         │
│                      (src/main.py)                           │
│                                                               │
│  • Capture frames from camera                                │
│  • Coordinate detection and tracking                         │
│  • Handle user input                                         │
│  • Manage display                                            │
└────────────────┬─────────────────┬──────────────────────────┘
                 │                 │
        ┌────────▼────────┐   ┌────▼────────┐
        │    DETECTOR     │   │   TRACKER   │
        │ (detector.py)   │   │ (tracker.py)│
        └────────┬────────┘   └────┬────────┘
                 │                 │
        ┌────────▼────────┐   ┌────▼────────┐
        │  YOLOv8 Model   │   │ Time Logic  │
        │  (Pretrained)   │   │ JSON Store  │
        └─────────────────┘   └─────────────┘
                 │                 │
        ┌────────▼────────┐   ┌────▼────────┐
        │  Phone: Class   │   │  data/      │
        │  Laptop: Class  │   │  *.json     │
        └─────────────────┘   └─────────────┘
```

## Component Breakdown

### 1. Main Application Layer (main.py)

```python
┌─────────────────────────────────────────┐
│     ScreenTimeMonitor Class             │
├─────────────────────────────────────────┤
│ Responsibilities:                        │
│ • Initialize camera (OpenCV)             │
│ • Create detector and tracker            │
│ • Main event loop                        │
│ • Frame processing optimization          │
│ • Display management                     │
│ • Keyboard handling                      │
│ • Cleanup and saving                     │
└─────────────────────────────────────────┘
```

**Key Optimization:**
```python
# Frame skipping for efficiency
if frame_counter % frame_skip == 0:
    detections = detector.detect(frame)
    tracker.update(detections)
```

### 2. Detection Layer (detector.py)

```python
┌─────────────────────────────────────────┐
│      DeviceDetector Class               │
├─────────────────────────────────────────┤
│ • Load YOLOv8 model                      │
│ • Warm up model (eliminates cold start) │
│ • Detect objects in frame                │
│ • Filter for phones (class 67)          │
│ • Filter for laptops (class 63)         │
│ • Draw bounding boxes                    │
│ • GPU/CPU optimization                   │
└─────────────────────────────────────────┘
```

**Detection Pipeline:**
```
Frame → YOLOv8 → All Objects → Filter Classes → Phone/Laptop → Confidence Filter → Output
```

### 3. Tracking Layer (tracker.py)

```python
┌─────────────────────────────────────────┐
│       UsageTracker Class                │
├─────────────────────────────────────────┤
│ • Track time per device                  │
│ • Apply minimum detection time filter   │
│ • Calculate statistics                   │
│ • Periodic auto-save                     │
│ • Session management                     │
│ • Crash recovery                         │
│ • Format time output                     │
└─────────────────────────────────────────┘
```

**Tracking Logic:**
```python
if device_detected:
    if continuously_detected_for > min_time:
        add_to_usage_time(elapsed)
```

### 4. Statistics Layer (stats.py)

```python
┌─────────────────────────────────────────┐
│        StatsViewer Class                │
├─────────────────────────────────────────┤
│ • Load session history                   │
│ • Calculate aggregates                   │
│ • Generate summaries                     │
│ • Create visualizations                  │
│ • Daily/weekly breakdowns                │
└─────────────────────────────────────────┘
```

## Data Flow

### Real-Time Monitoring Flow

```
1. Camera Capture
   │
   ├─> OpenCV VideoCapture
   └─> 640x480 @ 30fps
       │
       ↓
2. Frame Optimization
   │
   ├─> Skip N frames (default: 3)
   └─> Process every 3rd frame
       │
       ↓
3. Object Detection
   │
   ├─> YOLOv8 inference
   ├─> Get bounding boxes
   └─> Filter by confidence (>0.5)
       │
       ↓
4. Class Filtering
   │
   ├─> Keep only class 67 (phone)
   └─> Keep only class 63 (laptop)
       │
       ↓
5. Time Tracking
   │
   ├─> Update last_seen timestamp
   ├─> Calculate elapsed time
   └─> Add to cumulative time
       │
       ↓
6. Display Update
   │
   ├─> Draw bounding boxes
   ├─> Overlay statistics
   └─> Show frame
       │
       ↓
7. Periodic Save (every 30s)
   │
   └─> Write to JSON
```

### Statistics Flow

```
User runs stats.py
       │
       ↓
Load data/sessions.json
       │
       ↓
Parse all sessions
       │
       ├─> Calculate totals
       ├─> Group by date
       ├─> Compute percentages
       └─> Generate graphs
       │
       ↓
Display to user
```

## File System Structure

```
screen-time-monitor/
│
├── Configuration
│   └── config.yaml              ← All settings
│
├── Source Code
│   └── src/
│       ├── main.py             ← Entry point
│       ├── detector.py         ← YOLOv8 wrapper
│       ├── tracker.py          ← Time tracking
│       ├── stats.py            ← Analytics
│       └── utils.py            ← Helpers
│
├── Data (created at runtime)
│   └── data/
│       ├── sessions.json       ← History
│       └── current_session.json ← Backup
│
├── Models (downloaded automatically)
│   └── yolov8n.pt              ← Weights (~6MB)
│
└── Documentation
    ├── README.md
    ├── GETTING_STARTED.md
    ├── INSTALL.md
    ├── USAGE.md
    ├── OPTIMIZATION.md
    └── PROJECT_OVERVIEW.md
```

## Threading Model

```
┌─────────────────────────────────────────┐
│           Main Thread                    │
│  (Single-threaded for simplicity)        │
├─────────────────────────────────────────┤
│                                           │
│  Loop:                                    │
│    1. Capture frame                       │
│    2. Detect (if frame_counter % skip)   │
│    3. Track time                          │
│    4. Display                             │
│    5. Handle input                        │
│    6. Auto-save check                     │
│                                           │
└─────────────────────────────────────────┘
```

**Why single-threaded?**
- Simpler code, easier to debug
- No race conditions
- Adequate performance with optimizations
- Can be multi-threaded later if needed

## Memory Management

```
┌─────────────────────────────────────────┐
│            Memory Layout                 │
├─────────────────────────────────────────┤
│                                           │
│  YOLOv8 Model:        ~100-200 MB        │
│  PyTorch Runtime:     ~200-300 MB        │
│  Frame Buffers:       ~10 MB             │
│  Application Logic:   ~5 MB              │
│                                           │
│  Total:               ~500 MB            │
│                                           │
└─────────────────────────────────────────┘
```

**Optimization strategies:**
- Frames not kept in memory
- Results moved to CPU immediately (GPU mode)
- NumPy arrays for efficiency
- No video buffering
- Periodic garbage collection

## Processing Pipeline Detail

### Detection Phase

```
Input Frame (640x480x3)
       │
       ├─> Resize for model
       ├─> Normalize [0,1]
       └─> Convert RGB→BGR
       │
       ↓
YOLOv8 Neural Network
       │
       ├─> Backbone (CSPDarknet)
       ├─> Neck (PANet)
       └─> Head (Detection)
       │
       ↓
Raw Detections
       │
       ├─> [x1,y1,x2,y2] boxes
       ├─> class_id
       └─> confidence
       │
       ↓
Post-Processing
       │
       ├─> NMS (remove duplicates)
       ├─> Confidence filter (>0.5)
       └─> Class filter (67, 63)
       │
       ↓
Final Detections
```

### Tracking Phase

```
Detection: Phone Found
       │
       ↓
Is this first detection? ──YES─→ Record timestamp
       │                         Exit (wait for continuity)
       NO
       ↓
Calculate time since last seen
       │
       ↓
Is elapsed > min_time (1s)? ──NO──→ Exit (too brief)
       │
       YES
       ↓
Add elapsed time to total
       │
       ↓
Update last_seen timestamp
```

## Configuration Flow

```yaml
config.yaml
    │
    ├─> camera: {...}        → OpenCV settings
    ├─> detection: {...}     → YOLOv8 settings
    ├─> tracking: {...}      → Time tracking logic
    ├─> storage: {...}       → File paths
    └─> display: {...}       → UI options
          │
          ↓
    load_config() in utils.py
          │
          ↓
    Dictionary passed to all modules
```

## Error Handling Strategy

```
┌─────────────────────────────────────────┐
│         Error Handling Layers            │
├─────────────────────────────────────────┤
│                                           │
│  1. Validation                            │
│     • Check camera exists                 │
│     • Verify config file                  │
│     • Validate settings                   │
│                                           │
│  2. Graceful Degradation                  │
│     • GPU unavailable? Use CPU            │
│     • Model not found? Download           │
│     • Data corrupted? Start fresh         │
│                                           │
│  3. Recovery                              │
│     • Crash? Load last session            │
│     • Camera lost? Retry                  │
│     • Save failure? Try again             │
│                                           │
│  4. Cleanup                               │
│     • Release camera                      │
│     • Save data                           │
│     • Close windows                       │
│                                           │
└─────────────────────────────────────────┘
```

## Performance Bottlenecks & Solutions

### Bottleneck 1: Detection Speed
```
Problem: YOLOv8 inference takes 50-100ms per frame
Solution: Process every 3rd frame (saves 66% time)
Result: 15-20 FPS → acceptable for tracking
```

### Bottleneck 2: Model Loading
```
Problem: First inference slow due to model initialization
Solution: Warm-up with dummy frame during startup
Result: Consistent frame rates from start
```

### Bottleneck 3: Display Rendering
```
Problem: Drawing overlays adds latency
Solution: Optional headless mode for background use
Result: Can run without UI for max performance
```

### Bottleneck 4: File I/O
```
Problem: Saving every frame would slow down
Solution: Auto-save every 30 seconds only
Result: Negligible I/O impact
```

## Scalability Considerations

### Current Design (Single Camera)
```
1 Camera → 1 Process → 15-60 FPS ✓
```

### Multi-Camera (Future)
```
N Cameras → N Processes → Independent monitoring
           OR
N Cameras → 1 Process → Batch inference
```

### Cloud Deployment (If needed)
```
Edge Device → Local Detection → Send Stats Only → Cloud Dashboard
(Privacy preserved - only numbers sent, not video)
```

## Security Model

```
┌─────────────────────────────────────────┐
│          Security Boundaries             │
├─────────────────────────────────────────┤
│                                           │
│  Camera Access:                           │
│  ✓ Only when app running                  │
│  ✓ Explicit user start                    │
│  ✓ Visual indicator (window)              │
│                                           │
│  Data Storage:                            │
│  ✓ Local filesystem only                  │
│  ✓ User-accessible JSON                   │
│  ✓ No encryption needed (not sensitive)   │
│                                           │
│  Network:                                 │
│  ✓ No outbound connections                │
│  ✓ No cloud dependencies                  │
│  ✓ Works fully offline                    │
│                                           │
│  Privacy:                                 │
│  ✓ No face detection                      │
│  ✓ No identity tracking                   │
│  ✓ No video recording                     │
│  ✓ Only device presence tracked           │
│                                           │
└─────────────────────────────────────────┘
```

## Deployment Diagram

```
Development Machine
├── Edit code
├── Test with demo.py
└── Run monitor

        ↓

End User Machine
├── pip install requirements.txt
├── python quick_start.py (verify)
├── python src/main.py (monitor)
└── python src/stats.py (analyze)

        ↓

Data Generated
└── data/sessions.json (portable, can backup/share)
```

## Module Dependencies

```
main.py
├── imports detector.py
├── imports tracker.py
└── imports utils.py

detector.py
├── imports ultralytics (YOLOv8)
├── imports torch
├── imports cv2
└── imports numpy

tracker.py
├── imports json
└── imports datetime

stats.py
├── imports json
├── imports matplotlib
└── imports utils.py

utils.py
├── imports yaml
├── imports cv2
└── imports numpy
```

**Dependency Graph is Acyclic** ✓ (good design)

## Summary

This architecture emphasizes:

1. **Simplicity** - Single-threaded, straightforward flow
2. **Efficiency** - Optimizations at every layer
3. **Modularity** - Clear separation of concerns
4. **Privacy** - Local processing, no network
5. **Reliability** - Error handling and recovery
6. **Extensibility** - Easy to add new features

The design balances performance, maintainability, and user privacy while providing accurate screen time tracking.
