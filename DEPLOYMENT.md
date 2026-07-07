# Deployment Guide

Complete guide to deploying Screen Time Monitor in various environments.

## Deployment Options

Choose based on your needs:

1. **Local Deployment** - Run on your own machine
2. **Cloud Web App** - Deploy to Heroku/AWS/Azure (headless)
3. **Docker Container** - Containerized deployment
4. **Raspberry Pi** - Edge device deployment
5. **Network Deployment** - Multi-user setup with central server

---

## 1. LOCAL DEPLOYMENT (Windows/Linux/macOS)

### Standalone Executable (Windows)

#### Option A: PyInstaller (Recommended)

**Step 1: Install PyInstaller**
```bash
pip install pyinstaller
```

**Step 2: Create executable**
```bash
pyinstaller --onefile --windowed --icon=icon.ico src/main.py
```

**Step 3: Distribute**
- Executable located in `dist/main.exe`
- Users just run the .exe file
- No Python installation needed

**Create installer with NSIS:**
```bash
pip install pyinstaller-nsis
# Create NSIS installer script
```

#### Option B: Executable with Dependencies

Create a batch script that includes everything:

```bash
@echo off
REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Installing Python...
    REM Download and install Python
    exit /b 1
)

REM Install dependencies if first run
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
)

REM Run application
call venv\Scripts\activate
python src/main.py
```

### Linux/macOS Deployment

**Create shell script launcher:**

```bash
#!/bin/bash
set -e

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Create venv if needed
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run monitor
python src/main.py
```

Make it executable:
```bash
chmod +x monitor.sh
./monitor.sh
```

---

## 2. CLOUD WEB APP DEPLOYMENT

### Headless Mode (No Camera on Server)

For web dashboard showing stats:

**`src/web_server.py`** (Flask backend)

```python
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

DATA_DIR = Path("data")

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current statistics."""
    session_file = DATA_DIR / "current_session.json"
    
    if session_file.exists():
        with open(session_file) as f:
            return jsonify(json.load(f))
    return jsonify({"error": "No session data"}), 404

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get session history."""
    sessions_file = DATA_DIR / "sessions.json"
    
    if sessions_file.exists():
        with open(sessions_file) as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/download', methods=['GET'])
def download_data():
    """Download all data as JSON."""
    sessions_file = DATA_DIR / "sessions.json"
    if sessions_file.exists():
        return send_file(sessions_file, as_attachment=True)
    return jsonify({"error": "No data"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Deploy to Heroku

**Step 1: Create `Procfile`**
```
web: python src/web_server.py
```

**Step 2: Create `runtime.txt`**
```
python-3.9.16
```

**Step 3: Update `requirements.txt`**
```
flask==2.3.0
flask-cors==4.0.0
```

**Step 4: Deploy**
```bash
# Install Heroku CLI
# heroku login
# heroku create your-app-name
# git push heroku main
```

### Deploy to AWS

**Using EC2:**

```bash
# 1. Launch EC2 instance (Ubuntu)
# 2. SSH into instance
ssh -i key.pem ubuntu@your-instance

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# 4. Clone project
git clone https://github.com/yourusername/screen-time-monitor.git
cd screen-time-monitor

# 5. Setup venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run with Gunicorn (production)
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 src.web_server:app
```

**Using Elastic Beanstalk (easier):**

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 screen-time-monitor

# Create environment
eb create production-env

# Deploy
eb deploy
```

### Deploy to Azure

**Create `app.py` at root:**
```python
from src.web_server import app

if __name__ == '__main__':
    app.run()
```

**Deploy:**
```bash
# Install Azure CLI
# az login
az group create --name mygroup --location eastus
az appservice plan create --name myplan --resource-group mygroup --sku B1
az webapp create --name screen-time-monitor --resource-group mygroup --plan myplan --runtime "PYTHON|3.9"
```

---

## 3. DOCKER DEPLOYMENT

### Create `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p data

# Expose port for web server
EXPOSE 5000

# Run command (choose based on use case)
# For monitoring (requires camera):
# CMD ["python", "src/main.py"]

# For web server only:
CMD ["python", "src/web_server.py"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  screen-time-monitor:
    build: .
    image: screen-time-monitor:latest
    container_name: screen-time-monitor
    
    # For camera access
    devices:
      - /dev/video0:/dev/video0
    
    # For persistent data
    volumes:
      - ./data:/app/data
      - ./config.yaml:/app/config.yaml
    
    # Web server
    ports:
      - "5000:5000"
    
    # Environment
    environment:
      - PYTHONUNBUFFERED=1
    
    # Auto-restart
    restart: unless-stopped
```

### Docker Build & Run

```bash
# Build image
docker build -t screen-time-monitor .

# Run container
docker run -d \
  --name monitor \
  -v $(pwd)/data:/app/data \
  -p 5000:5000 \
  -v /dev/video0:/dev/video0 \
  screen-time-monitor

# View logs
docker logs -f monitor

# Stop container
docker stop monitor
```

### Docker Hub Deployment

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag screen-time-monitor yourusername/screen-time-monitor:latest

# Push to Docker Hub
docker push yourusername/screen-time-monitor:latest

# Others can now run:
docker run -d yourusername/screen-time-monitor:latest
```

---

## 4. RASPBERRY PI DEPLOYMENT

### Setup

**Step 1: Install OS**
```bash
# Download Raspberry Pi OS Lite
# Flash to SD card using Balena Etcher
```

**Step 2: Initial Setup**
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv

# Install camera support
sudo apt install python3-opencv libatlas-base-dev libjasper-dev
```

**Step 3: Enable Camera**
```bash
sudo raspi-config
# Interface Options → Camera → Enable
```

**Step 4: Install Project**
```bash
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 5: Create Systemd Service**

Create `/etc/systemd/system/screen-time-monitor.service`:

```ini
[Unit]
Description=Screen Time Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/screen-time-monitor
Environment="PATH=/home/pi/screen-time-monitor/venv/bin"
ExecStart=/home/pi/screen-time-monitor/venv/bin/python src/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable screen-time-monitor
sudo systemctl start screen-time-monitor
sudo systemctl status screen-time-monitor
```

### Optimize for Raspberry Pi

Edit `config.yaml`:

```yaml
detection:
  model: "yolov8n.pt"        # Nano model only
  process_every_n_frames: 5  # More skipping
  device: "cpu"              # No GPU

camera:
  width: 320
  height: 240                # Lower resolution
  fps: 15                    # Lower FPS

display:
  show_feed: false           # Headless mode
```

---

## 5. NETWORK DEPLOYMENT (Multi-User)

### Central Server + Multiple Clients

**Architecture:**
```
Client 1 (Monitor) → Server (Stats & Dashboard)
Client 2 (Monitor) → Server
Client 3 (Monitor) → Server
                  ↓
            Web Dashboard
```

### Server (`src/server.py`)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = Path("data/clients")
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/api/report', methods=['POST'])
def report_data():
    """Client reports usage data."""
    data = request.json
    client_id = data.get('client_id')
    
    if not client_id:
        return jsonify({"error": "No client_id"}), 400
    
    # Save client data
    client_file = DATA_DIR / f"{client_id}.json"
    
    sessions = []
    if client_file.exists():
        with open(client_file) as f:
            sessions = json.load(f)
    
    # Add new session
    sessions.append({
        **data,
        'timestamp': datetime.now().isoformat(),
        'reported_at': datetime.now().isoformat()
    })
    
    with open(client_file, 'w') as f:
        json.dump(sessions, f, indent=2)
    
    return jsonify({"status": "ok"})

@app.route('/api/stats/<client_id>', methods=['GET'])
def get_client_stats(client_id):
    """Get stats for specific client."""
    client_file = DATA_DIR / f"{client_id}.json"
    
    if client_file.exists():
        with open(client_file) as f:
            sessions = json.load(f)
        
        total_phone = sum(s['phone_time'] for s in sessions)
        total_laptop = sum(s['laptop_time'] for s in sessions)
        
        return jsonify({
            'client_id': client_id,
            'sessions': len(sessions),
            'total_phone_time': total_phone,
            'total_laptop_time': total_laptop,
            'data': sessions
        })
    
    return jsonify({"error": "No data"}), 404

@app.route('/api/all-clients', methods=['GET'])
def get_all_clients():
    """Get summary of all clients."""
    clients = {}
    
    for client_file in DATA_DIR.glob("*.json"):
        client_id = client_file.stem
        with open(client_file) as f:
            sessions = json.load(f)
        
        clients[client_id] = {
            'sessions': len(sessions),
            'phone_time': sum(s['phone_time'] for s in sessions),
            'laptop_time': sum(s['laptop_time'] for s in sessions)
        }
    
    return jsonify(clients)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Client Report Module (`src/client_reporter.py`)

```python
import requests
import json
from pathlib import Path
import time

class ClientReporter:
    def __init__(self, server_url, client_id):
        self.server_url = server_url
        self.client_id = client_id
        self.report_interval = 300  # 5 minutes
    
    def send_report(self, stats):
        """Send stats to server."""
        try:
            data = {
                'client_id': self.client_id,
                **stats
            }
            
            response = requests.post(
                f"{self.server_url}/api/report",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✓ Report sent successfully")
                return True
            else:
                print(f"✗ Server error: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ Network error: {e}")
            return False
    
    def start_auto_report(self, tracker):
        """Start background reporting."""
        while True:
            time.sleep(self.report_interval)
            stats = tracker.get_usage_stats()
            self.send_report(stats)
```

### Integration in `main.py`

```python
# Add this to main.py if using network mode
if config.get('network', {}).get('enabled'):
    from src.client_reporter import ClientReporter
    
    reporter = ClientReporter(
        server_url=config['network']['server_url'],
        client_id=config['network']['client_id']
    )
    
    # Start reporting in background thread
    import threading
    report_thread = threading.Thread(
        target=reporter.start_auto_report,
        args=(tracker,),
        daemon=True
    )
    report_thread.start()
```

### Client Configuration

Add to `config.yaml`:

```yaml
network:
  enabled: true
  server_url: "http://192.168.1.100:5000"
  client_id: "office-client-1"
  report_interval: 300  # 5 minutes
```

---

## 6. GITHUB RELEASES DEPLOYMENT

### Create Release Package

**Step 1: Create release workflow** (`.github/workflows/release.yml`):

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build executable
        run: |
          pyinstaller --onefile --windowed src/main.py
      
      - name: Upload Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/main.exe
```

**Step 2: Create release**

```bash
git tag v1.0.0
git push origin v1.0.0
```

**Step 3: Users download from GitHub Releases**

---

## 7. MSI INSTALLER (Windows)

### Create MSI Installer

**Install tools:**
```bash
pip install pyinstaller
# Install WiX Toolset from: https://wixtoolset.org/
```

**Create `setup.wxs`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="Screen Time Monitor" Language="1033" Version="1.0.0.0">
    <Package InstallerVersion="200" Compressed="yes" />
    <Media Id="1" Cabinet="cab1.cab" EmbedCab="yes" />
    
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="Screen Time Monitor" />
      </Directory>
    </Directory>
    
    <Feature Id="ProductFeature" Title="Screen Time Monitor" Level="1">
      <ComponentRef Id="MainExecutable" />
    </Feature>
  </Product>
</Wix>
```

**Build:**
```bash
candle setup.wxs
light setup.wixobj -out Setup.msi
```

---

## Deployment Checklist

- [ ] Choose deployment method
- [ ] Install all dependencies
- [ ] Test locally first
- [ ] Configure for target environment
- [ ] Set up monitoring/logging
- [ ] Create backup strategy
- [ ] Document deployment steps
- [ ] Test disaster recovery
- [ ] Set up auto-updates
- [ ] Monitor performance

---

## Comparison Table

| Method | Setup Time | Ease | Performance | Cost |
|--------|-----------|------|------------|------|
| Local Standalone | 10 min | Easy | Excellent | Free |
| Web Dashboard | 30 min | Medium | Good | Free-$10/mo |
| Docker | 20 min | Medium | Good | Free-variable |
| Raspberry Pi | 45 min | Medium | Fair | $35 |
| Cloud VM | 1 hour | Hard | Excellent | $5-20/mo |
| Network | 2 hours | Hard | Good | Variable |

---

## Recommended Deployments

### For Personal Use
→ **Local Standalone** (easiest, fastest)

### For Small Team
→ **Docker on local machine**

### For Web Access
→ **Heroku or AWS** with stats dashboard

### For 24/7 Monitoring
→ **Raspberry Pi** or **Docker**

### For Multi-User Organization
→ **Network deployment** with central server

---

## Troubleshooting Deployment

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Or change port in config
export FLASK_PORT=8000
```

### Camera Not Accessible in Docker
```bash
# Run with camera device
docker run --device /dev/video0:/dev/video0 screen-time-monitor
```

### Out of Memory
```yaml
# Reduce model size
detection:
  model: "yolov8n.pt"  # Nano only
  process_every_n_frames: 5
```

### Slow Performance
- Increase frame skipping
- Use smaller model
- Reduce resolution
- Enable GPU if available

---

## Next Steps

1. Choose deployment method based on your needs
2. Follow step-by-step guide for chosen method
3. Test thoroughly before full deployment
4. Monitor logs and performance
5. Set up backups and recovery plan

For questions on a specific deployment, ask!
