# 🔧 Job Runner Troubleshooting Guide

## Issue: "Unknown error" when running job

### Problem
The job runner UI shows "Failed to run event collection job" with "Unknown error".

### Root Cause
The Railway backend endpoint `/api/jobs/run-event-collection` doesn't exist yet because Railway hasn't been redeployed with the new code.

## ✅ Solution Steps

### Step 1: Redeploy Railway Backend

The new endpoint has been added to `api_server.py` but Railway needs to be redeployed:

**Option A: Automatic Redeploy (if Railway is connected to GitHub)**
- Push the code to GitHub (already done ✅)
- Railway should auto-deploy
- Check Railway dashboard for deployment status

**Option B: Manual Redeploy**
1. Go to Railway Dashboard
2. Select your backend service
3. Click "Deploy" or "Redeploy"

### Step 2: Verify Endpoint Exists

After redeploy, test the endpoint:

```bash
curl -X POST https://cosmicdiary-production.up.railway.app/api/jobs/run-event-collection \
  -H "Content-Type: application/json"
```

**Expected Response:**
- ✅ If endpoint exists: JSON response with job status
- ❌ If 404: Endpoint not deployed yet, redeploy Railway

### Step 3: Verify Environment Variables

Make sure `FLASK_API_URL` is set in **Vercel**:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Verify `FLASK_API_URL` is set to:
   ```
   https://cosmicdiary-production.up.railway.app
   ```
3. If missing, add it and redeploy Vercel

### Step 4: Test Again

1. Go to `/jobs` page
2. Click "Run Event Collection Job"
3. Check the error message - it should now be more specific

## 🔍 Enhanced Error Messages

The updated code now provides detailed error messages:

### Error: "Backend URL not configured"
**Meaning:** `FLASK_API_URL` is not set in Vercel

**Fix:** Add `FLASK_API_URL` in Vercel environment variables

### Error: "Cannot connect to backend"
**Meaning:** Vercel can't reach Railway backend

**Possible causes:**
- Railway backend is down
- `FLASK_API_URL` is incorrect
- CORS not configured (though job endpoint doesn't need CORS from browser)

**Fix:**
1. Check Railway backend is running
2. Verify `FLASK_API_URL` is correct
3. Test Railway endpoint directly

### Error: "404 Not Found"
**Meaning:** Endpoint doesn't exist on Railway

**Fix:** Redeploy Railway backend

### Error: "Invalid response from backend"
**Meaning:** Railway returned non-JSON response

**Possible causes:**
- Railway returned HTML error page
- Backend crashed
- Wrong endpoint URL

**Fix:** Check Railway logs for errors

## 🧪 Testing Checklist

- [ ] Railway backend redeployed with new code
- [ ] Endpoint `/api/jobs/run-event-collection` returns 200 (not 404)
- [ ] `FLASK_API_URL` set in Vercel environment variables
- [ ] Vercel redeployed after setting environment variable
- [ ] Railway backend is running and healthy (check `/health` endpoint)
- [ ] Test from `/jobs` page

## 📋 Quick Test Commands

### Test Railway Health:
```bash
curl https://cosmicdiary-production.up.railway.app/health
```

### Test Job Endpoint:
```bash
curl -X POST https://cosmicdiary-production.up.railway.app/api/jobs/run-event-collection \
  -H "Content-Type: application/json"
```

### Test from Vercel API:
```bash
curl -X POST https://cosmicdiary.vercel.app/api/jobs/run-event-collection \
  -H "Content-Type: application/json"
```

## 🎯 Current Status

Based on the curl test:
- ❌ Railway endpoint returns 404 (not deployed yet)
- ✅ Code is committed and pushed
- ✅ Enhanced error handling added

**Next Step:** Redeploy Railway backend

