# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Webcam
- Windows/Linux/macOS

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
cd screen-time-monitor
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- OpenCV for camera handling
- Ultralytics YOLOv8 for object detection
- PyTorch for deep learning
- NumPy for numerical operations
- PyYAML for configuration
- Matplotlib for statistics visualization

### 4. Verify Installation

Check if your camera works:

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

### 5. First Run

The first time you run the monitor, it will automatically download the YOLOv8 model (about 6MB).

```bash
python src/main.py
```

## GPU Acceleration (Optional)

For faster performance, enable GPU support:

### NVIDIA GPU (CUDA)

1. Install CUDA Toolkit from [NVIDIA](https://developer.nvidia.com/cuda-downloads)

2. Install PyTorch with CUDA:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

3. Update `config.yaml`:
```yaml
detection:
  device: "cuda"  # Change from "cpu" to "cuda"
```

### Verify GPU

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

## Troubleshooting

### Camera Not Found

- Check if camera is connected and not used by another application
- Try different camera IDs in `config.yaml` (0, 1, 2, etc.)
- On Linux, you may need camera permissions

### Import Errors

Make sure you're in the virtual environment and all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### Performance Issues

- Reduce frame resolution in `config.yaml`
- Increase `process_every_n_frames` value
- Use lighter model: `yolov8n.pt` instead of `yolov8s.pt`

### Model Download Issues

If automatic download fails, manually download from:
https://github.com/ultralytics/assets/releases

Place the `.pt` file in the project root.

## Quick Start Commands

### Windows:
```bash
run_monitor.bat  # Start monitoring
run_stats.bat    # View statistics
```

### Linux/macOS:
```bash
python src/main.py   # Start monitoring
python src/stats.py  # View statistics
```

## Configuration

Edit `config.yaml` to customize:
- Camera settings (resolution, FPS)
- Detection parameters (confidence, model)
- Performance optimization (frame skipping)
- Display options

## Next Steps

1. Run the monitor for a few sessions
2. View your statistics with `python src/stats.py`
3. Adjust `config.yaml` based on your needs
4. Set up scheduled monitoring (optional)

For more information, see README.md
