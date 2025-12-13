# 🔧 Railway Start Command Fix

## Problem
```
/bin/bash: line 1: /: Is a directory
```

Railway is trying to execute `/` as a command instead of starting the Flask app.

## ✅ Solution Applied

### 1. Fixed Procfile
- Removed extra blank lines
- Format: `web: python api_server.py`

### 2. Added railway.toml
Created `railway.toml` with explicit configuration:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python api_server.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## 🔍 Alternative: Set in Railway Dashboard

If the file-based config doesn't work, set it manually:

1. Go to Railway Dashboard → Your Service
2. Go to **Settings** → **Deploy**
3. Under **"Start Command"**, set:
   ```
   python api_server.py
   ```
4. Save and redeploy

## ✅ Verification

After deployment, check logs for:
```
🚀 Starting Cosmic Diary API Server on 0.0.0.0:XXXX
```

NOT:
```
/bin/bash: line 1: /: Is a directory
```

## 📋 Current Configuration

- **Procfile**: `web: python api_server.py`
- **railway.toml**: `startCommand = "python api_server.py"`
- **Both configured** for redundancy

The code is pushed. Railway should now use the correct start command.

