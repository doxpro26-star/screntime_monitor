# 🚀 Railway Deployment - Step by Step

Complete guide to deploy your Screen Time Monitor to Railway (FREE with $5/month credit).

---

## ✅ Prerequisites

- GitHub account (you have this!)
- GitHub repo with your code (you have this!)
- Railway account (will create)
- 10 minutes

---

## 📋 Step 1: Prepare Your GitHub Repository

You've already done the initial setup! Let's verify and add all project files.

### Check current status:
```bash
git status
```

### Add all project files:
```bash
git add .
git commit -m "Add Screen Time Monitor project with deployment files"
git push origin main
```

Your repo should now contain all files including:
- ✅ `src/` folder with all modules
- ✅ `requirements.txt`
- ✅ `Procfile` (important for Railway!)
- ✅ `runtime.txt`
- ✅ `config.yaml`
- ✅ `src/web_server.py`
- ✅ All other project files

### Verify on GitHub:
Go to: https://github.com/doxpro26-star/screntime_monitor

You should see all files listed.

---

## 🚂 Step 2: Create Railway Account

### 2.1 Go to Railway
https://railway.app

### 2.2 Sign Up
- Click "Sign Up" (top right)
- Select "GitHub" (easiest)
- Authorize Railway to access your GitHub
- You'll be logged in!

### 2.3 Complete Setup
- Railway might ask for email confirmation
- Verify email if needed
- Done!

---

## 🚀 Step 3: Create Railway Project

### 3.1 Start New Project
- You'll see Railway dashboard
- Click "Create New Project" (large button)
- Or click "+" button

### 3.2 Select Deployment Method
You'll see options:
- "Provision a database"
- "Deploy from GitHub repo" ← **SELECT THIS ONE**
- "Create an empty project"
- Other options

**Click: "Deploy from GitHub repo"**

---

## 🔗 Step 4: Connect GitHub Repository

### 4.1 Configure GitHub Access
- Railway will ask for permission to access GitHub
- Click "Install and Authorize"
- Choose your GitHub account

### 4.2 Select Repository
- Search for: `screntime_monitor`
- Click on your repo from the list
- Or if you have it bookmarked, select it

### 4.3 Deploy Configuration
- Railway will auto-detect Python project
- It will read your `requirements.txt`
- Should auto-detect `Procfile`

If not auto-detected, configure:
- **Start Command:** `gunicorn src.web_server:app`
- **Python Version:** 3.9 or 3.10

---

## ⚙️ Step 5: Configure Environment Variables (Optional)

### 5.1 Click "Variables" Tab
In your project dashboard, look for "Variables" section

### 5.2 Add Variables (Optional but Recommended)
```
FLASK_ENV = production
DATA_DIR = /app/data
FLASK_PORT = 5000
```

### 5.3 Save
Click "Save" or equivalent

**Note:** These are optional - app works with defaults

---

## 📦 Step 6: Deploy!

### 6.1 Click Deploy
- You should see a green "Deploy" button
- Click it!
- Or it might auto-deploy

### 6.2 Watch Deployment
- You'll see logs appearing
- Shows installation progress
- Shows app startup

### 6.3 Wait for Success
Look for messages like:
```
✓ Build completed
✓ App started successfully
Running on http://...
```

**Deployment takes 2-5 minutes**

---

## 🎉 Step 7: Access Your App!

### 7.1 Get Your URL
After deployment succeeds:
- Railway shows your app URL
- Usually: `https://app-name-xyz.railway.app`
- Copy this URL

### 7.2 Test Your App
- Open URL in browser
- You should see your dashboard!
- Check if charts and stats load

### 7.3 Test API
```bash
# Test health endpoint
curl https://your-railway-url/api/health

# Should return:
# {"status": "ok", "timestamp": "...", "version": "1.0.0"}
```

---

## ✅ Verify Deployment

### Test Dashboard
- Access: https://your-railway-url/
- Should see:
  - Statistics cards (phone, laptop, sessions)
  - Charts
  - Refresh button

### Test API Endpoints
```bash
# Get summary
curl https://your-railway-url/api/summary

# Should return JSON with stats
```

### Check Logs
In Railway dashboard:
- Go to "Deployments" tab
- Click latest deployment
- View logs
- Should see no errors

---

## 🔧 Troubleshooting

### Issue: "Deployment failed"
**Solution:**
1. Check logs in Railway dashboard
2. Common issue: Missing `Procfile`
   - Verify `Procfile` is in your GitHub repo
   - Content should be: `web: gunicorn src.web_server:app`
3. Check `requirements.txt` is valid

### Issue: "Build error"
**Solution:**
1. Check all dependencies are in `requirements.txt`
2. Ensure `src/web_server.py` exists
3. Check for syntax errors in Python files

### Issue: "App won't start"
**Solution:**
1. Check logs for error messages
2. Verify `FLASK_PORT` is set to 5000
3. Check `src/web_server.py` starts correctly

### Issue: "Can't access dashboard"
**Solution:**
1. Wait 1-2 minutes for app to fully start
2. Refresh page
3. Check Railway logs for errors

---

## 📊 Monitor Your App

### In Railway Dashboard

**Deployments Tab:**
- View deployment history
- See logs
- Check for errors
- Redeploy if needed

**Metrics Tab:**
- CPU usage
- Memory usage
- Network traffic

**Settings Tab:**
- Environment variables
- Domains
- App configuration

**Logs:**
- Real-time logs
- Shows requests
- Error messages

---

## 🔄 Update Your App

### If you make changes:

```bash
# Make changes locally
# Then:
git add .
git commit -m "Update description"
git push origin main

# Railway auto-redeploys!
# Watch deployment in dashboard
```

Railway automatically redeploys when you push to GitHub!

---

## 💡 Free Credit & Billing

### Your Free $5/Month
- Railway gives $5 free credit monthly
- This app uses ~$0-2/month
- You have plenty of free usage!

### Monitor Usage
- Go to Railway dashboard
- Check "Account" section
- View usage metrics
- See remaining credit

### Cost Estimation
- Your app: ~$0-2/month
- Well within $5 free credit
- **No charge!** ✅

---

## 🎯 What's Next?

### Right Now
1. ✅ Verify deployment works
2. ✅ Test dashboard access
3. ✅ Check API endpoints

### This Week
1. ✅ Monitor app performance
2. ✅ Check logs for issues
3. ✅ Test all features

### Long Term
1. ✅ Set up monitoring alerts
2. ✅ Plan scaling
3. ✅ Regular backups

---

## 📚 Useful Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Your Project:** https://github.com/doxpro26-star/screntime_monitor
- **Railway Docs:** https://docs.railway.app/
- **Python Support:** https://docs.railway.app/guides/python

---

## ✨ Key Files for Railway

Make sure these are in your GitHub repo:

```
your-repo/
├── Procfile ........................ Web process definition
├── runtime.txt ..................... Python version
├── requirements.txt ................ Dependencies
├── config.yaml ..................... Configuration
├── src/
│   ├── web_server.py ............... Main Flask app
│   ├── main.py ..................... Monitor app
│   ├── detector.py ................. Detection
│   ├── tracker.py .................. Tracking
│   ├── stats.py .................... Statistics
│   └── utils.py .................... Utilities
└── README.md ....................... Documentation
```

**Important:** All these files must be in your GitHub repo for Railway to work!

---

## 🚀 Quick Checklist

- [ ] GitHub repo created with all files
- [ ] GitHub repo pushed with all project files
- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] Project deployed from GitHub
- [ ] Deployment completed successfully
- [ ] Dashboard accessible
- [ ] API endpoints working
- [ ] App showing statistics

---

## 🎉 Success!

When you see:
- ✅ Green "deployed" status in Railway
- ✅ Dashboard loads in browser
- ✅ API responds to requests
- ✅ No errors in logs

**You're done!** 🎊

Your app is now live on Railway, completely FREE!

Access it at: `https://your-app-name.railway.app`

---

## 📞 Need Help?

### Common Issues
→ See "Troubleshooting" section above

### Railway Support
→ https://railway.app/support

### Documentation
→ https://docs.railway.app/

### My Project Docs
→ DEPLOYMENT.md, START_HERE.md

---

## 💰 Cost Summary

| Item | Cost/Month |
|------|-----------|
| Your App | ~$0-2 |
| Free Credit | +$5 |
| **Total** | **$0** ✅ |

**Completely FREE!**

---

**You're all set! Deploy your Screen Time Monitor to Railway now!** 🚀

Any questions? Check the troubleshooting section or refer to other documentation files!
