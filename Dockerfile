FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY config.yaml .
COPY src/ src/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p data

# Expose port for web server (if using)
EXPOSE 5000

# Default to web server (for headless deployment)
# For local monitoring with camera, run: docker run --device /dev/video0:/dev/video0 screen-time-monitor python src/main.py
CMD ["python", "src/web_server.py"]
