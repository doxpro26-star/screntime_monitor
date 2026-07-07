@echo off
REM Deploy Screen Time Monitor using Docker

echo.
echo ==========================================
echo Screen Time Monitor - Docker Deployment
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed
    echo Please install Docker from https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

echo OK: Docker is installed
echo.

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed
    echo Please install Docker Compose
    pause
    exit /b 1
)

echo.
echo Building Docker image...
docker-compose build

if errorlevel 1 (
    echo ERROR: Failed to build image
    pause
    exit /b 1
)

echo.
echo Starting container...
docker-compose up -d

if errorlevel 1 (
    echo ERROR: Failed to start container
    pause
    exit /b 1
)

timeout /t 3 /nobreak

echo.
echo ==========================================
echo Deployment Complete!
echo ==========================================
echo Dashboard: http://localhost:5000
echo API: http://localhost:5000/api/
echo.
echo View logs:
echo   docker-compose logs -f
echo.
echo Stop container:
echo   docker-compose down
echo ==========================================
echo.
pause
