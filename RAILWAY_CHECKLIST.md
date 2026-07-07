# ✅ Railway Deployment Checklist

Quick checklist before deploying to Railway.

---

## 📦 Step 1: Verify GitHub Repository Files

Run this in your project directory to verify all files are present:

```bash
# Check key files exist
dir Procfile
dir runtime.txt
dir requirements.txt
dir config.yaml
dir src\web_server.py
dir src\main.py
```

**Required files:**
- ✅ `Procfile` - Web process
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies
- ✅ `src/web_server.py` - Flask app
- ✅ `config.yaml` - Configuration
- ✅ `src/` folder - All modules

---

## 📝 Step 2: Verify Procfile Content

**File: `Procfile`**

Should contain exactly:
```
web: gunicorn src.web_server:app
```

**Check it:**
```bash
type Procfile
```

**If it's wrong, create it:**
```bash
echo web: gunicorn src.web_server:app > Procfile
```

---

## 🐍 Step 3: Verify Python Version

**File: `runtime.txt`**

Should contain exactly:
```
python-3.9.16
```

**Check it:**
```bash
type runtime.txt
```

**If it's wrong, create it:**
```bash
echo python-3.9.16 > runtime.txt
```

---

## 📋 Step 4: Verify requirements.txt

**File: `requirements.txt`**

Should have all dependencies:
```
opencv-python>=4.8.0
ultralytics>=8.0.0
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
PyYAML>=6.0
pillow>=10.0.0
matplotlib>=3.7.0
flask==2.3.0
flask-cors==4.0.0
gunicorn>=20.1.0
```

**Check it:**
```bash
type requirements.txt
```

**If missing Flask/Gunicorn, add them:**
```bash
echo flask==2.3.0 >> requirements.txt
echo flask-cors==4.0.0 >> requirements.txt
echo gunicorn>=20.1.0 >> requirements.txt
```

---

## 🔧 Step 5: Verify config.yaml

**File: `config.yaml`**

Should exist and contain configuration.

**Check it:**
```bash
type config.yaml
```

---

## 🐙 Step 6: Git Repository Setup

### Check Git Status
```bash
git status
```

Expected output: "On branch main" with no uncommitted changes

### If changes exist, commit them:
```bash
git add .
git commit -m "Add/update project files for Railway deployment"
git push origin main
```

### Verify on GitHub
- Go to: https://github.com/doxpro26-star/screntime_monitor
- You should see all files
- Should show "main" branch

---

## ✅ Final Checklist

Before deploying to Railway:

### Repository Files
- [ ] `Procfile` exists with correct content
- [ ] `runtime.txt` exists with Python version
- [ ] `requirements.txt` includes Flask & Gunicorn
- [ ] `config.yaml` exists
- [ ] `src/web_server.py` exists
- [ ] `src/main.py` exists
- [ ] All other project files present

### Git Repository
- [ ] All files committed to git
- [ ] Pushed to GitHub main branch
- [ ] GitHub repo is public (for Railway)
- [ ] Repository at: https://github.com/doxpro26-star/screntime_monitor

### Local Testing (Optional)
- [ ] App runs locally: `python src/web_server.py`
- [ ] Dashboard works: http://localhost:5000
- [ ] API responds: curl http://localhost:5000/api/health

---

## 🚀 Ready to Deploy!

If all checkboxes are checked, you're ready!

### Next Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project
4. Select "Deploy from GitHub repo"
5. Choose `screntime_monitor`
6. Click deploy!

---

## 🆘 Troubleshooting Before Deploy

### Issue: "Procfile not found"
```bash
# Create it
echo web: gunicorn src.web_server:app > Procfile
git add Procfile
git commit -m "Add Procfile"
git push origin main
```

### Issue: "requirements.txt incomplete"
```bash
# Add missing packages
pip freeze > requirements.txt
# Or manually add:
echo flask==2.3.0 >> requirements.txt
echo gunicorn>=20.1.0 >> requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt"
git push origin main
```

### Issue: "Python version not specified"
```bash
# Create runtime.txt
echo python-3.9.16 > runtime.txt
git add runtime.txt
git commit -m "Add Python version"
git push origin main
```

### Issue: "Files not in GitHub"
```bash
# Check what's committed
git status

# If files show as untracked:
git add .
git commit -m "Add all project files"
git push origin main

# Verify on GitHub website
```

---

## 📊 File Check Script

Run this Windows batch script to verify everything:

```batch
@echo off
echo Checking Railway deployment files...
echo.

if exist "Procfile" (
    echo ✓ Procfile exists
) else (
    echo ✗ Procfile MISSING
)

if exist "runtime.txt" (
    echo ✓ runtime.txt exists
) else (
    echo ✗ runtime.txt MISSING
)

if exist "requirements.txt" (
    echo ✓ requirements.txt exists
    findstr /c:"flask" requirements.txt >nul && echo ✓ Flask included || echo ✗ Flask missing
    findstr /c:"gunicorn" requirements.txt >nul && echo ✓ Gunicorn included || echo ✗ Gunicorn missing
) else (
    echo ✗ requirements.txt MISSING
)

if exist "config.yaml" (
    echo ✓ config.yaml exists
) else (
    echo ✗ config.yaml MISSING
)

if exist "src\web_server.py" (
    echo ✓ src/web_server.py exists
) else (
    echo ✗ src/web_server.py MISSING
)

echo.
echo Check complete!
```

Save as `check_deployment.bat` and run:
```bash
check_deployment.bat
```

---

## 🎯 Summary

**To deploy to Railway:**

1. ✅ Verify all files present
2. ✅ Commit to GitHub
3. ✅ Go to railway.app
4. ✅ Deploy from GitHub repo
5. ✅ Done!

**Time to deploy:** 5 minutes
**Cost:** $0 (free credit)

---

## 🎉 You're Ready!

Use this checklist before deploying. If everything checks out, Railway deployment will work perfectly!

Questions? See RAILWAY_DEPLOYMENT.md for detailed steps.
