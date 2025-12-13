# 🐛 Railway Deployment Crash Debugging

## Issue
Deployment builds successfully but crashes on startup with "You reached the start of the range" (log truncation).

## 🔍 How to Debug

### Step 1: Check Railway Logs

1. Go to Railway Dashboard → Your Service
2. Click **"Logs"** tab
3. Look for error messages at the end of the logs
4. Common errors:
   - `ModuleNotFoundError` → Missing dependency
   - `ImportError` → Import path issue
   - `FileNotFoundError` → Missing file
   - `AttributeError` → Code issue

### Step 2: Check Startup Errors

The code now prints all registered routes on startup. Look for:
- `🚀 Starting Cosmic Diary API Server`
- `📋 Registered routes:`
- Any error messages after these

### Step 3: Common Crash Causes

#### 1. Missing Environment Variables
**Error:** `KeyError` or `None` values

**Check:**
- `SUPABASE_URL` set in Railway
- `SUPABASE_SERVICE_ROLE_KEY` set
- `OPENAI_API_KEY` set (optional but may cause issues)

#### 2. Import Errors
**Error:** `ModuleNotFoundError: No module named 'X'`

**Check:**
- All dependencies in `requirements.txt`
- Python version matches (3.10.12 per runtime.txt)

#### 3. File Not Found
**Error:** `FileNotFoundError`

**Check:**
- `collect_events_with_cosmic_state.py` exists
- `astro_calculations.py` exists
- All required files are in repository

#### 4. Port Binding Issues
**Error:** `Address already in use` or port errors

**Check:**
- Railway sets `PORT` automatically
- Procfile uses `web: python api_server.py`

## ✅ Fixes Applied

1. **Added `sys` import** - Needed for `sys.exit()` in error handler
2. **Added startup error handling** - Catches and logs fatal errors
3. **Route debugging** - Prints registered routes on startup
4. **Moved `timezone` import** - Now imported at top level

## 🧪 Test Locally First

Before deploying to Railway, test locally:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary

# Test imports
python3 -c "import api_server; print('✅ Imports OK')"

# Test startup
python3 api_server.py
# Should see: "🚀 Starting Cosmic Diary API Server"
# Press Ctrl+C to stop
```

## 📋 Railway Environment Variables Checklist

Make sure these are set in Railway:

- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_SERVICE_ROLE_KEY`
- [ ] `OPENAI_API_KEY` (optional)
- [ ] `FLASK_API_URL` (optional, for self-reference)
- [ ] `PORT` (auto-set by Railway, don't set manually)

## 🔧 Next Steps

1. **Check Railway Logs** for the actual error message
2. **Verify environment variables** are all set
3. **Test locally** to ensure code works
4. **Redeploy** after fixing any issues

## 📝 What to Look For in Logs

After redeploy, check logs for:

✅ **Success indicators:**
- `🚀 Starting Cosmic Diary API Server`
- `📊 Swiss Ephemeris version: 2.10.03`
- `📋 Registered routes:`
- No error messages

❌ **Failure indicators:**
- `ModuleNotFoundError`
- `ImportError`
- `FileNotFoundError`
- `AttributeError`
- Any Python traceback

---

**The code should now provide better error messages on startup. Check Railway logs to see the actual error.**

