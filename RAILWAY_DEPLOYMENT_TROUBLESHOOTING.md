# Railway Deployment Troubleshooting

## Issue: Railway Not Picking Up Latest Commit

If Railway is not automatically deploying your latest commits, try these solutions:

## Solution 1: Manual Deploy Trigger

### Via Railway Dashboard:
1. Go to your Railway project: https://railway.app/project
2. Click on your service (Cosmic Diary API)
3. Go to **Settings** tab
4. Scroll down to **Deployments** section
5. Click **"Redeploy"** or **"Deploy"** button
6. Select **"Deploy latest commit"** or choose the specific commit

### Via Railway CLI:
```bash
# Install Railway CLI if not installed
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Trigger deployment
railway up
```

## Solution 2: Check GitHub Connection

1. Go to Railway Dashboard → Your Project → **Settings**
2. Check **"Source"** section
3. Verify:
   - ✅ Repository is connected (should show your GitHub repo)
   - ✅ Branch is set to `main` (or your default branch)
   - ✅ Auto-deploy is **enabled**
   - ✅ Service is **active**

## Solution 3: Check Webhook Status

1. Go to GitHub → Your Repository → **Settings** → **Webhooks**
2. Look for Railway webhook
3. Verify:
   - ✅ Status is "Active" (green)
   - ✅ Recent deliveries show successful requests
   - ✅ Events include: `push`, `repository`, `deployment`

## Solution 4: Force Redeploy via Empty Commit

Sometimes Railway needs a trigger. Create an empty commit:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
git commit --allow-empty -m "chore: Trigger Railway deployment"
git push origin main
```

## Solution 5: Check Railway Logs

1. Go to Railway Dashboard → Your Service
2. Click **"Deployments"** tab
3. Check the latest deployment:
   - Status (should be "Active")
   - Build logs (check for errors)
   - Runtime logs (check if service started)

## Solution 6: Verify Service Configuration

### Check railway.toml:
- Service name is correct
- Build command is correct
- Start command is correct

### Check Procfile:
- Start command matches Railway's expectations

## Solution 7: Disconnect and Reconnect GitHub

1. Railway Dashboard → Project → Settings → Source
2. Click **"Disconnect"** from GitHub
3. Click **"Connect GitHub"** again
4. Select your repository
5. Select branch `main`
6. Railway should trigger a new deployment

## Solution 8: Check Environment Variables

1. Railway Dashboard → Your Service → **Variables**
2. Verify all required env vars are set:
   - `PORT` (Railway sets this automatically)
   - `FLASK_PORT` (optional fallback)
   - `HOST` (optional, defaults to 0.0.0.0)
   - Other required variables

## Solution 9: Check Build/Start Commands

Verify in Railway Dashboard → Service → Settings:

### Build Command:
```bash
# Should be empty or minimal for Python/Flask
# Railway auto-detects Python projects
```

### Start Command:
```bash
python api_server.py
# OR
python3 api_server.py
```

## Solution 10: Check Service Status

1. Railway Dashboard → Your Service
2. Check:
   - ✅ Service is **Active** (not paused/stopped)
   - ✅ Health check is passing (if configured)
   - ✅ No deployment errors in logs

## Current Status Check

Your latest commits:
```
273afad docs: Add prompt system integration summary
6b710ff refactor: Integrate existing prompt system into cosmic collection script
1a98cf2 docs: Add OpenAI event detection improvements guide
```

If Railway shows an older commit, it means auto-deploy isn't working.

## Quick Fix: Manual Trigger

**Fastest solution:**
1. Railway Dashboard → Your Service → **Deployments**
2. Click **"..."** (three dots) on latest deployment
3. Click **"Redeploy"**
4. Or click **"Deploy Latest Commit"** button

## Verify Deployment

After triggering deployment:
1. Check Railway logs in real-time
2. Look for: `🚀 Starting Cosmic Diary API Server`
3. Verify build completed successfully
4. Check service is responding on health endpoint

---

**If none of these work:**
- Check Railway status page: https://status.railway.app/
- Contact Railway support: support@railway.app
- Check Railway Discord: https://discord.gg/railway

