# 🔧 Railway Build Failed - FIX

## ❌ Issue: Build Failed

**Error:** "Failed to build an image"

**Cause:** Most likely one of these:
1. Missing `src/web_server.py` file
2. Issue with `Procfile` format
3. Missing `gunicorn` in requirements.txt
4. Python syntax error in code

---

## ✅ Solution: Fix and Redeploy

### Step 1: Check Your Files Locally

Run these commands in your project directory:

```bash
# Check if web_server.py exists
dir src\web_server.py

# Check Procfile content
type Procfile

# Check if gunicorn is in requirements.txt
findstr gunicorn requirements.txt
```

### Step 2: Verify Procfile

**File:** `Procfile` (no extension)

**Should contain EXACTLY:**
```
web: gunicorn src.web_server:app
```

**If missing or wrong:**
```bash
# Windows:
echo web: gunicorn src.web_server:app > Procfile

# Linux/Mac:
echo "web: gunicorn src.web_server:app" > Procfile
```

### Step 3: Verify requirements.txt

**Must include:**
```
flask==2.3.0
flask-cors==4.0.0
gunicorn>=20.1.0
```

**If missing, add them:**
```bash
echo flask==2.3.0 >> requirements.txt
echo flask-cors==4.0.0 >> requirements.txt
echo gunicorn>=20.1.0 >> requirements.txt
```

### Step 4: Verify src/web_server.py

**Must exist and have:**
```python
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run()
```

**Check it exists:**
```bash
# Windows
type src\web_server.py | head -20

# Linux/Mac
head -20 src/web_server.py
```

### Step 5: Commit and Push

```bash
git add .
git commit -m "Fix Railway deployment - ensure all files correct"
git push origin main
```

### Step 6: Retry Deployment

In Railway:
1. Go to Deployments
2. Click "Retry Diagnosis" button
3. Wait for new build
4. Monitor logs

---

## 🔍 Common Issues & Fixes

### Issue 1: Procfile Missing or Wrong

**Error:** Can't find how to start app

**Fix:**
```bash
# Create correct Procfile
echo web: gunicorn src.web_server:app > Procfile
git add Procfile
git commit -m "Fix Procfile"
git push origin main
```

### Issue 2: Gunicorn Not Installed

**Error:** Command 'gunicorn' not found

**Fix:**
```bash
# Add to requirements.txt
echo gunicorn>=20.1.0 >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn"
git push origin main
```

### Issue 3: web_server.py Missing

**Error:** No module named 'web_server'

**Fix:**
- Verify `src/web_server.py` exists
- Check it's not in wrong folder
- Ensure filename is exactly `web_server.py` (lowercase, underscore)

### Issue 4: Port Configuration

**Error:** Address already in use

**Fix in web_server.py:**
```python
import os
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Issue 5: Dependencies Issue

**Error:** Pip install failed

**Fix:**
```bash
# Test locally first
python -m pip install -r requirements.txt

# If error, check for typos in requirements.txt
type requirements.txt
```

---

## 📋 Complete Fix Checklist

Before redeploying:

- [ ] Procfile exists with correct content
- [ ] Procfile has NO .txt extension
- [ ] `web: gunicorn src.web_server:app` in Procfile
- [ ] requirements.txt includes flask
- [ ] requirements.txt includes gunicorn
- [ ] src/web_server.py exists
- [ ] src/web_server.py is not empty
- [ ] All files committed to git
- [ ] Pushed to GitHub main branch

---

## 🚀 Step-by-Step Fix

### For Windows Users:

```batch
@echo off
REM Step 1: Fix Procfile
echo web: gunicorn src.web_server:app > Procfile

REM Step 2: Add to requirements.txt
echo gunicorn>=20.1.0 >> requirements.txt
echo flask==2.3.0 >> requirements.txt
echo flask-cors==4.0.0 >> requirements.txt

REM Step 3: Check files
echo.
echo Checking Procfile:
type Procfile
echo.
echo Checking web_server.py exists:
if exist src\web_server.py (
    echo OK - web_server.py found
) else (
    echo ERROR - web_server.py NOT found!
)

REM Step 4: Commit
git add .
git commit -m "Fix Railway deployment issues"
git push origin main

echo.
echo Fixed and pushed! Retry deployment in Railway.
```

Save as `fix_railway.bat` and run:
```bash
fix_railway.bat
```

### For Linux/Mac Users:

```bash
#!/bin/bash

# Step 1: Fix Procfile
echo "web: gunicorn src.web_server:app" > Procfile

# Step 2: Add to requirements.txt
echo "gunicorn>=20.1.0" >> requirements.txt
echo "flask==2.3.0" >> requirements.txt
echo "flask-cors==4.0.0" >> requirements.txt

# Step 3: Check files
echo "Checking Procfile:"
cat Procfile
echo ""
echo "Checking web_server.py:"
if [ -f "src/web_server.py" ]; then
    echo "OK - web_server.py found"
else
    echo "ERROR - web_server.py NOT found!"
fi

# Step 4: Commit
git add .
git commit -m "Fix Railway deployment issues"
git push origin main

echo ""
echo "Fixed and pushed! Retry deployment in Railway."
```

Save as `fix_railway.sh` and run:
```bash
chmod +x fix_railway.sh
./fix_railway.sh
```

---

## 🔄 Redeploy After Fix

1. **Go to Railway Dashboard**
   → https://railway.app/dashboard

2. **Click Your Project**
   → screntime_monitor

3. **Click Deployments Tab**
   → See failed deployment

4. **Click "Retry Diagnosis"**
   → Railway re-checks (optional)

5. **OR Click Deploy Again**
   → New deployment from latest GitHub code

6. **Watch Logs**
   → Should see successful build this time

---

## 🎯 Expected Success Signs

When build succeeds, you'll see:
- ✅ Initialization: COMPLETE
- ✅ Build > Build image: COMPLETE (green)
- ✅ Deploy: RUNNING
- ✅ Post-deploy: (if applicable)

---

## 📞 If Still Failing

### Click "View Logs" and Check For:

**Error: No module named 'gunicorn'**
→ Add `gunicorn>=20.1.0` to requirements.txt

**Error: No module named 'flask'**
→ Add `flask==2.3.0` to requirements.txt

**Error: No such file or directory: 'Procfile'**
→ Create Procfile with: `web: gunicorn src.web_server:app`

**Error: Failed to find application object**
→ Check Procfile says: `src.web_server:app`

**Error: Address already in use**
→ Use PORT env variable in web_server.py

---

## 💡 Pro Tips

### Tip 1: Test Build Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Test if Flask starts
python src/web_server.py

# Should see: Running on http://127.0.0.1:5000
```

### Tip 2: Check Procfile Format

```bash
# CORRECT:
web: gunicorn src.web_server:app

# WRONG (don't do these):
web: python src/web_server.py    ❌
web: flask run                     ❌
web: gunicorn src.main:app        ❌ (wrong module)
```

### Tip 3: Use Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy from command line
railway link          # Link to project
railway up            # Deploy
```

---

## ✅ Quick Fix Summary

| Issue | Fix |
|-------|-----|
| **Procfile missing** | `echo web: gunicorn src.web_server:app > Procfile` |
| **Gunicorn missing** | `echo gunicorn>=20.1.0 >> requirements.txt` |
| **Flask missing** | `echo flask==2.3.0 >> requirements.txt` |
| **web_server.py missing** | Copy from project files |
| **Wrong Procfile format** | Use: `web: gunicorn src.web_server:app` |
| **Port issues** | Add: `os.getenv('PORT', 5000)` in code |

---

## 🚀 Ready to Fix?

1. **Run fix script** (Windows: fix_railway.bat, Linux: fix_railway.sh)
2. **Verify files** (check Procfile, requirements.txt)
3. **Push to GitHub** (git push origin main)
4. **Retry in Railway** (click Retry or Deploy button)
5. **Monitor logs** (click View logs)
6. **Wait 3-5 minutes** for new build
7. **Success!** ✅

---

**Your deployment will succeed this time!** 🚀

Let me know if you need more help!
