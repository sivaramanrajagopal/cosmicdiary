# 🚂 Railway Deployment Check

## Issue: 404 Error on `/api/jobs/run-event-collection`

The endpoint exists in the code but returns 404, meaning Railway hasn't deployed the new code yet.

## ✅ Verify Code is in Repository

The endpoint was added at line 529 in `api_server.py`:

```python
@app.route('/api/jobs/run-event-collection', methods=['POST'])
def run_event_collection_job():
```

Check if this exists in your repository on GitHub:
- Go to: https://github.com/sivaramanrajagopal/cosmicdiary/blob/main/api_server.py
- Search for: `run-event-collection`
- If found: ✅ Code is in repository
- If not found: Need to push the code

## 🔄 Redeploy Railway

### Option 1: Auto-Deploy (if connected to GitHub)

Railway should auto-deploy when you push to main branch. Check:

1. Go to Railway Dashboard
2. Select your backend service
3. Go to "Deployments" tab
4. Look for latest deployment
   - ✅ Green checkmark = Deployed successfully
   - ⏳ In progress = Deploying
   - ❌ Red X = Deployment failed

**If deployment failed:**
- Check deployment logs
- Look for errors in build/deploy process

### Option 2: Manual Redeploy

1. Go to Railway Dashboard
2. Select your backend service
3. Click "Deploy" button (or three dots menu → "Redeploy")
4. Select "Latest Commit" or "Redeploy"
5. Wait for deployment to complete

### Option 3: Trigger via GitHub

If Railway isn't auto-deploying:

1. Make a small change to trigger deployment
2. Or disconnect/reconnect GitHub in Railway settings

## 🧪 Test After Deployment

### 1. Test Health Endpoint (should work):
```bash
curl https://cosmicdiary-production.up.railway.app/health
```

### 2. Test Job Endpoint (should work after redeploy):
```bash
curl -X POST https://cosmicdiary-production.up.railway.app/api/jobs/run-event-collection \
  -H "Content-Type: application/json" \
  -v
```

**Expected after redeploy:**
- ✅ Status 200 or 202
- ✅ JSON response with job status
- ❌ If still 404: Deployment didn't include the new code

## 🔍 Verify Deployment

After redeploying, check:

1. **Railway Logs:**
   - Go to Railway → Your Service → Logs
   - Look for: `🚀 Starting Cosmic Diary API Server`
   - Check for any import errors or startup issues

2. **List All Routes (if possible):**
   - The Flask app should register the route on startup
   - Check logs for route registration

3. **Test from Local:**
   ```bash
   # If you have Railway CLI
   railway logs
   ```

## 📋 Quick Checklist

- [ ] Code pushed to GitHub (main branch)
- [ ] Railway service connected to GitHub repo
- [ ] Latest deployment shows latest commit
- [ ] Deployment completed successfully (green checkmark)
- [ ] `/health` endpoint works
- [ ] `/api/jobs/run-event-collection` returns 200 (not 404)
- [ ] `FLASK_API_URL` set in Vercel
- [ ] Vercel redeployed

## 🚨 Common Issues

### Issue: Code pushed but Railway not deploying

**Solution:**
1. Check Railway → Settings → Source
2. Verify GitHub connection
3. Verify branch is `main`
4. Try manual redeploy

### Issue: Deployment succeeds but endpoint still 404

**Possible causes:**
1. Wrong file deployed (check Railway build settings)
2. Route not being registered (check Flask app initialization)
3. Path mismatch (verify route path exactly matches)

**Debug:**
```python
# Add to api_server.py temporarily to list all routes
@app.route('/api/debug/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'path': rule.rule,
            'methods': list(rule.methods)
        })
    return jsonify({'routes': routes})
```

### Issue: Import errors preventing route registration

**Check Railway logs for:**
- `ModuleNotFoundError`
- `ImportError`
- Any Python errors during startup

## 🎯 Current Status

- ✅ Code committed and pushed to GitHub
- ✅ Endpoint added to `api_server.py` (line 529)
- ❌ Railway not deployed yet (returns 404)
- ✅ Enhanced error handling in frontend

**Action Required:** Redeploy Railway backend

---

**After redeploying, test again from the `/jobs` page. The enhanced error messages will now show exactly what's happening.**

