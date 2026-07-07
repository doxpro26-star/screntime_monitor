# 🚀 START HERE - Deployment Guide

**Welcome!** Your Screen Time Monitor is ready to deploy. This guide will help you get started in the next 5-10 minutes.

---

## 🎯 Choose Your Deployment Path

### Path 1: Quick Local Test (5 minutes) ⭐ FASTEST
**Best for:** Testing, development, personal use

```bash
# Windows
deploy-docker.bat

# Linux/macOS  
./deploy-docker.sh
```

Then open: **http://localhost:5000**

### Path 2: Cloud Deployment (10-30 minutes)
**Best for:** Web access from anywhere, 24/7 monitoring

Choose your platform:
- **Heroku** (easiest, free) → [Go to Heroku Guide](#heroku)
- **AWS** (most powerful) → [Go to AWS Guide](#aws)
- **Raspberry Pi** (always-on) → [Go to Raspberry Pi Guide](#raspberry-pi)

### Path 3: Custom Server (30+ minutes)
**Best for:** Full control, custom domain, enterprise

→ [Go to Server Guide](#server)

---

## 🐳 Quick Deploy: Docker

### Prerequisites
- Windows/Linux/macOS
- Docker installed ([download](https://docker.com))

### Installation

**Windows Users:**
```batch
deploy-docker.bat
```

**Linux/macOS Users:**
```bash
chmod +x deploy-docker.sh
./deploy-docker.sh
```

### ✅ Verify Deployment
```bash
# Check health
curl http://localhost:5000/api/health

# View dashboard
open http://localhost:5000  # macOS
start http://localhost:5000 # Windows
xdg-open http://localhost:5000 # Linux
```

### 🎨 What You'll See
- Dashboard at http://localhost:5000
- Statistics cards with usage data
- Interactive charts
- API endpoints for programmatic access

### 🛑 Stop Deployment
```bash
docker-compose down
```

---

## ☁️ Cloud Deployments

<a name="heroku"></a>
### Heroku (Free Tier Available)

**Setup (10 minutes):**

1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Run these commands:

```bash
# Login
heroku login

# Create app
heroku create my-screen-time-monitor

# Deploy
git push heroku main

# View live
heroku open
```

**Result:** Your app at `https://my-screen-time-monitor.herokuapp.com`

---

<a name="aws"></a>
### AWS EC2 (Free Tier Eligible)

**Setup (20 minutes):**

1. Create AWS account
2. Launch t2.micro EC2 instance (free tier)
3. SSH into instance:

```bash
ssh -i key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv

# Clone project
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Run (in background)
nohup gunicorn --bind 0.0.0.0:5000 src.web_server:app &

# Access at http://your-instance-ip:5000
```

---

<a name="raspberry-pi"></a>
### Raspberry Pi (Always-On)

**Setup (30 minutes):**

1. Get Raspberry Pi with OS installed
2. SSH into Pi:

```bash
ssh pi@your-pi-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv

# Clone project
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create service (copy-paste the service file from DEPLOYMENT.md)
sudo nano /etc/systemd/system/screen-time-monitor.service
# [Add service content here]

# Enable & start
sudo systemctl enable screen-time-monitor
sudo systemctl start screen-time-monitor

# Access at http://your-pi-ip:5000
```

---

<a name="server"></a>
### Your Own Server

**Setup (30+ minutes):**

1. Get VPS from DigitalOcean, Linode, etc.
2. SSH into server
3. Install dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot

# Clone project & setup (same as above)

# Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/default
# [Add Nginx config]

# Setup SSL (free)
sudo certbot --nginx -d yourdomain.com

# Run with Gunicorn
gunicorn --bind 127.0.0.1:5000 src.web_server:app
```

---

## 📊 API Endpoints

All deployments include these API endpoints:

```
GET /                    # Web Dashboard
GET /api/health         # Health check
GET /api/summary        # Overall statistics
GET /api/daily          # Daily breakdown
GET /api/weekly         # Weekly statistics
GET /api/sessions       # All sessions
GET /api/download       # Download data (JSON)
```

**Example:**
```bash
curl http://localhost:5000/api/summary
```

Response:
```json
{
  "total_sessions": 5,
  "total_phone_time": 7200,
  "total_laptop_time": 14400,
  "phone_percentage": 33.3,
  "laptop_percentage": 66.7
}
```

---

## 🎨 Dashboard Features

- 📱 **Phone Usage** - Time & percentage
- 💻 **Laptop Usage** - Time & percentage
- 📊 **Charts** - Usage trends
- 📥 **Export** - Download data
- 🔄 **Refresh** - Real-time updates
- 📱 **Mobile Friendly** - Works on any device

---

## ✅ Deployment Verification

After deployment, verify everything works:

### 1. Check API Health
```bash
curl http://your-deployment-url/api/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "...",
  "version": "1.0.0"
}
```

### 2. Get Statistics
```bash
curl http://your-deployment-url/api/summary
```

### 3. Access Dashboard
Open in browser:
```
http://your-deployment-url
```

You should see the dashboard with statistics cards and charts.

---

## 🚨 Troubleshooting

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :5000

# Linux/macOS
lsof -i :5000
```

### "Docker not found"
```bash
# Install Docker from https://docker.com
# Verify installation
docker --version
```

### "Can't connect to deployment"
1. Check firewall settings
2. Ensure port 5000 is open
3. Check if service is running
4. View logs for errors

### "Out of memory"
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
```

### "Need more help?"
Check these files:
- **DEPLOY_QUICK_START.md** - Quick reference
- **DEPLOYMENT.md** - Detailed guides
- **DEPLOYMENT_SUMMARY.md** - Overview

---

## 🎯 Next Steps

### Immediate (Right Now)
1. ✅ Choose deployment method above
2. ✅ Install required tools (Docker, Heroku CLI, etc.)
3. ✅ Run deployment script
4. ✅ Verify dashboard loads

### Today
5. ✅ Configure settings if needed
6. ✅ Test API endpoints
7. ✅ Download sample data

### This Week
8. ✅ Set up monitoring
9. ✅ Plan backups
10. ✅ Share with team/family

---

## 📚 Full Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview |
| **DEPLOY_QUICK_START.md** | Quick reference |
| **DEPLOYMENT.md** | Detailed deployment guide |
| **DEPLOYMENT_SUMMARY.md** | Deployment overview |
| **ARCHITECTURE.md** | Technical design |
| **USAGE.md** | Application usage |
| **PROJECT_STRUCTURE.md** | File organization |

---

## 🎊 You're All Set!

Your Screen Time Monitor is ready to deploy! 

### Quick Summary
✅ Application built  
✅ Web dashboard included  
✅ Docker configured  
✅ Cloud deployment options  
✅ Comprehensive documentation  
✅ Testing tools included  

### Ready to deploy?

**Choose your path:**
- 🐳 **Docker** - 5 minutes
- ☁️ **Heroku** - 10 minutes
- 🚀 **AWS** - 20 minutes
- 🏠 **Raspberry Pi** - 30 minutes
- 🖥️ **Your Server** - 30+ minutes

---

## 💡 Tips

1. **Test locally first** with Docker
2. **Keep data backed up** regularly
3. **Monitor performance** after deployment
4. **Use HTTPS in production** (use Let's Encrypt)
5. **Set up monitoring alerts** for issues
6. **Document your setup** for future reference

---

## 🆘 Quick Help

| Issue | Solution |
|-------|----------|
| Port in use | Change port in docker-compose.yml |
| Docker not installed | Download from docker.com |
| Can't SSH to server | Check key permissions & IP |
| App won't start | Check logs: `docker logs` or `journalctl` |
| Out of memory | Reduce model size in config.yaml |

---

## 🚀 Let's Deploy!

### Ready? Pick one:

**Option 1: Docker (Easiest)**
```bash
# Windows
deploy-docker.bat

# Linux/macOS
./deploy-docker.sh
```

**Option 2: Heroku (Cloud)**
```bash
git push heroku main
```

**Option 3: AWS (Powerful)**
Follow setup guide above ↑

---

## 🎉 Congratulations!

You have a production-ready Screen Time Monitor deployment!

### Features Available:
✅ Real-time monitoring  
✅ Web dashboard  
✅ REST API  
✅ Data download  
✅ Statistics  
✅ 24/7 operation  

### Get started now! 🚀

Questions? Check the comprehensive guides included in this project.

---

**Happy monitoring! 📊✨**

Next step: Run your deployment script and access the dashboard!
