# 🚀 Force Railway Deployment Guide

## Problem
Railway is not picking up the latest commit and auto-deploying.

## ✅ Solution: Force Deployment

### Method 1: Manual Redeploy via Railway Dashboard (Easiest)

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Select your backend service (Cosmic Diary API)

2. **Trigger Manual Deployment**
   - Click on the service
   - Go to **"Deployments"** tab
   - Click **"Redeploy"** button (top right)
   - Or click **"New Deployment"** → **"Deploy Latest"**

3. **Verify Deployment**
   - Watch the deployment logs
   - Wait for "Deployed successfully" status
   - Should take 1-3 minutes

### Method 2: Push Empty Commit (Triggers Auto-Deploy)

If Railway is connected to GitHub, push an empty commit to trigger deployment:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
git commit --allow-empty -m "Trigger Railway deployment"
git push origin main
```

This forces GitHub to trigger Railway's webhook.

### Method 3: Disconnect and Reconnect GitHub

If auto-deploy is broken:

1. Railway Dashboard → Your Service → **Settings**
2. Under **"Source"**, click **"Disconnect"**
3. Click **"Connect GitHub"** again
4. Select repository: `sivaramanrajagopal/cosmicdiary`
5. Select branch: `main`
6. Railway will deploy automatically

### Method 4: Use Railway CLI (If Installed)

```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up
```

### Method 5: Check Railway Settings

1. Go to Railway Dashboard → Your Service → **Settings**
2. Check **"Source"**:
   - ✅ Repository: `sivaramanrajagopal/cosmicdiary`
   - ✅ Branch: `main`
   - ✅ Auto-deploy: Enabled

3. Check **"Build & Deploy"**:
   - Root Directory: Should be `/` (or leave empty)
   - Build Command: Usually auto-detected (may need `pip install -r requirements.txt`)
   - Start Command: Should be `python api_server.py` or auto-detected

## 🔍 Verify Latest Commit is Deployed

After deployment, check:

1. **Railway Logs:**
   - Go to your service → **Logs** tab
   - Look for startup message: `🚀 Starting Cosmic Diary API Server`
   - Check commit hash if logged

2. **Test Endpoint:**
   ```bash
   curl -X POST https://cosmicdiary-production.up.railway.app/api/jobs/run-event-collection \
     -H "Content-Type: application/json" \
     -v
   ```

3. **Check Deployment Details:**
   - Railway Dashboard → Deployments
   - Latest deployment should show:
     - ✅ Green checkmark
     - Latest commit hash
     - "Deployed successfully"

## 🐛 Common Issues

### Issue: Deployment keeps failing

**Check:**
- Build logs in Railway
- Look for import errors
- Check if all dependencies are in `requirements.txt`

**Common errors:**
- `ModuleNotFoundError` → Missing dependency in requirements.txt
- `FileNotFoundError` → Wrong root directory
- Import errors → Check Python version compatibility

### Issue: Auto-deploy not working

**Causes:**
- GitHub webhook not configured
- Branch mismatch (deploying wrong branch)
- Railway-GitHub connection broken

**Fix:**
- Reconnect GitHub (Method 3 above)
- Verify branch is `main`
- Check Railway webhook in GitHub repo settings

### Issue: Old code still running

**Causes:**
- Deployment succeeded but using cached files
- Wrong branch deployed
- Build caching old code

**Fix:**
1. Clear Railway cache (Settings → Clear Cache)
2. Force redeploy
3. Verify correct branch

## 📋 Quick Checklist

- [ ] Latest code pushed to GitHub main branch
- [ ] Railway service connected to GitHub
- [ ] Branch set to `main` in Railway settings
- [ ] Auto-deploy enabled in Railway
- [ ] Manual redeploy triggered
- [ ] Deployment shows "Deployed successfully"
- [ ] Test endpoint returns 200 (not 404)
- [ ] Railway logs show latest startup message

## 🎯 Recommended Steps (Do This Now)

1. **Push empty commit to trigger:**
   ```bash
   cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
   git commit --allow-empty -m "Trigger Railway deployment"
   git push origin main
   ```

2. **If that doesn't work, manually redeploy:**
   - Railway Dashboard → Service → Deployments → Redeploy

3. **Verify deployment:**
   ```bash
   curl -X POST https://cosmicdiary-production.up.railway.app/api/jobs/run-event-collection \
     -H "Content-Type: application/json"
   ```

4. **Check Railway logs** for any startup errors

---

**Most reliable method:** Manual redeploy via Railway Dashboard (Method 1)

