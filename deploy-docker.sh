#!/bin/bash
# Deploy Screen Time Monitor using Docker

set -e

echo "=========================================="
echo "Screen Time Monitor - Docker Deployment"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"

# Build the image
echo ""
echo "📦 Building Docker image..."
docker-compose build

# Start the container
echo ""
echo "🚀 Starting container..."
docker-compose up -d

# Wait for container to start
sleep 2

# Check if container is running
if [ "$(docker-compose ps -q)" != "" ]; then
    echo "✓ Container started successfully"
    echo ""
    echo "=========================================="
    echo "Deployment Complete!"
    echo "=========================================="
    echo "📊 Dashboard: http://localhost:5000"
    echo "🔌 API: http://localhost:5000/api/"
    echo ""
    echo "View logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "Stop container:"
    echo "  docker-compose down"
    echo "=========================================="
else
    echo "❌ Failed to start container"
    docker-compose logs
    exit 1
fi
