# Quick Deployment Guide

Choose your deployment method below and follow the steps.

---

## 🚀 Option 1: Docker (Easiest & Recommended)

### Prerequisites
- Docker installed ([download](https://docs.docker.com/get-docker/))
- Docker Compose (usually comes with Docker Desktop)

### Windows
```batch
deploy-docker.bat
```

### Linux/macOS
```bash
chmod +x deploy-docker.sh
./deploy-docker.sh
```

### Result
- 📊 Dashboard at http://localhost:5000
- 🔌 API at http://localhost:5000/api/
- 💾 Data persisted in `data/` directory

**Verify it's working:**
```bash
curl http://localhost:5000/api/health
```

---

## 📱 Option 2: Heroku (Free Tier Available)

### Prerequisites
- Heroku account (sign up at heroku.com)
- Heroku CLI installed

### Steps

**1. Login to Heroku**
```bash
heroku login
```

**2. Create app**
```bash
heroku create your-app-name
```

**3. Deploy**
```bash
git push heroku main
```

**4. View logs**
```bash
heroku logs --tail
```

**5. Access dashboard**
```
https://your-app-name.herokuapp.com
```

**Stop or delete app**
```bash
heroku destroy your-app-name
```

---

## ☁️ Option 3: AWS (Most Reliable)

### Prerequisites
- AWS account
- AWS CLI installed

### Using EC2

**1. Launch Instance**
```bash
# In AWS Console:
# - Choose Ubuntu 20.04 LTS
# - t2.micro (free tier eligible)
# - Configure security group to allow port 5000
```

**2. Connect & Deploy**
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Clone repo
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

# Install & run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn (production)
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 src.web_server:app
```

**3. Access**
```
http://your-instance-ip:5000
```

---

## 🐧 Option 4: Raspberry Pi (Always-On Monitoring)

### Prerequisites
- Raspberry Pi (3B+ or newer)
- Raspberry Pi OS installed
- Camera module enabled

### Steps

**1. SSH into Pi**
```bash
ssh pi@your-pi-ip
```

**2. Install dependencies**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv

# Camera support (if needed)
sudo apt install -y python3-opencv
```

**3. Clone & setup**
```bash
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Create service**

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
ExecStart=/home/pi/screen-time-monitor/venv/bin/python src/web_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl enable screen-time-monitor
sudo systemctl start screen-time-monitor
sudo systemctl status screen-time-monitor
```

**5. Access**
```
http://your-pi-ip:5000
```

---

## 🏢 Option 5: Traditional Server (Virtual Machine)

### Prerequisites
- VPS/VM with Python 3.8+
- SSH access

### Steps

**1. SSH into server**
```bash
ssh user@your-server-ip
```

**2. Install dependencies**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx

# For SSL certificates
sudo apt install -y certbot python3-certbot-nginx
```

**3. Deploy application**
```bash
git clone https://github.com/yourusername/screen-time-monitor
cd screen-time-monitor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**4. Create Nginx config** (`/etc/nginx/sites-available/default`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**5. Enable SSL (optional but recommended)**
```bash
sudo certbot --nginx -d your-domain.com
```

**6. Create systemd service** and enable (see Raspberry Pi example above)

**7. Access**
```
https://your-domain.com
```

---

## 🔄 Comparison

| Option | Setup Time | Cost | Best For |
|--------|-----------|------|----------|
| Docker | 5 min | Free | Local/testing |
| Heroku | 10 min | Free-$7/mo | Small projects |
| AWS | 20 min | Free-$10/mo | Production |
| Raspberry Pi | 30 min | $35 one-time | 24/7 monitoring |
| Server | 30 min | $5-20/mo | Full control |

---

## ✅ Verify Deployment

### Check health
```bash
curl http://your-deployment-url/api/health
```

### Get statistics
```bash
curl http://your-deployment-url/api/summary
```

### View dashboard
Open in browser:
```
http://your-deployment-url
```

---

## 🚨 Troubleshooting

### Port already in use
```bash
# Change port in docker-compose.yml or environment
export FLASK_PORT=8080
```

### Container won't start
```bash
# Check logs
docker-compose logs
```

### Out of memory
```yaml
# Edit docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M
```

### Permission denied
```bash
# On Linux, run as sudo
sudo docker-compose up -d
```

---

## 🔐 Security Considerations

### For Production Deployment

1. **Use environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

2. **Enable SSL/HTTPS**
   - Use Let's Encrypt (free)
   - Configure Nginx/Apache

3. **Add authentication** (optional)
   - Protect with password
   - Use API keys

4. **Monitor logs**
   - Check error logs regularly
   - Set up log rotation

5. **Backup data**
   ```bash
   # Backup data directory
   cp -r data/ data-backup-$(date +%Y%m%d)
   ```

---

## 🎯 Next Steps After Deployment

1. **Access dashboard**
   - Open http://your-url
   - View statistics

2. **Configure auto-upload**
   - Set up cron job to send data
   - Or use API to pull data

3. **Monitor performance**
   - Check CPU/memory usage
   - Review logs

4. **Set up backups**
   - Backup data regularly
   - Test recovery process

5. **Scale if needed**
   - Add more capacity
   - Set up load balancing

---

## 📞 Need Help?

1. Check DEPLOYMENT.md for detailed options
2. Review Docker logs: `docker logs screen-time-monitor`
3. Check web server logs in container
4. Verify network connectivity
5. Ensure firewall allows port access

---

## 🎉 Congrats!

Your Screen Time Monitor is now deployed and accessible!

**Features available:**
- 📊 Real-time statistics dashboard
- 🔌 REST API for programmatic access
- 📥 Data download functionality
- 📈 Daily/weekly analytics
- ✅ Health monitoring

Enjoy tracking your screen time! 🚀
