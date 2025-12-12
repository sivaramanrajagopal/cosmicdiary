# 🚂 Railway Deployment Guide (Flask API Backend)

Complete guide to deploy the Cosmic Diary Flask API to Railway.

---

## Prerequisites

1. **Railway account** (sign up at [railway.app](https://railway.app))
2. **GitHub account** with repository pushed
3. **Supabase project** already set up
4. **OpenAI API key**

---

## Step 1: Prepare for Deployment

### 1.1 Create `Procfile`

Railway uses a `Procfile` to know how to start your application.

Create `Procfile` in the root of `CosmicDiary/`:

```bash
cd /path/to/CosmicDiary/CosmicDiary
nano Procfile
```

Add:
```
web: python api_server.py
```

### 1.2 Create `runtime.txt` (Optional but Recommended)

Specify Python version:

```bash
nano runtime.txt
```

Add:
```
python-3.10.12
```

### 1.3 Update `api_server.py` for Production

Ensure the Flask server binds to Railway's host and port:

Check your `api_server.py` has:
```python
if __name__ == '__main__':
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 8000)))  # Railway sets PORT
    host = os.getenv('HOST', '0.0.0.0')  # Bind to all interfaces
    
    app.run(host=host, port=port, debug=False)  # Always False in production
```

### 1.4 Create `.railwayignore` (Optional)

Similar to `.gitignore`, exclude unnecessary files:

```bash
nano .railwayignore
```

Add:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.env.local
*.log
logs/
node_modules/
.git/
```

---

## Step 2: Push to GitHub

```bash
cd /path/to/CosmicDiary/CosmicDiary
git add Procfile runtime.txt .railwayignore
git commit -m "Add Railway deployment files"
git push origin main
```

---

## Step 3: Deploy to Railway

### 3.1 Create New Project

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your repository: `cosmicdiary`
5. Select branch: `main`

### 3.2 Configure Service

Railway will auto-detect Python and install dependencies.

**Important**: Railway will look for `requirements.txt` in the root of the repo.

Since your project structure is:
```
cosmicdiary/
  └── CosmicDiary/
      ├── api_server.py
      ├── requirements.txt
      └── ...
```

You need to configure the root directory:

1. In Railway dashboard, click on your service
2. Go to **Settings** → **Deploy**
3. Set **Root Directory** to: `CosmicDiary`
4. Set **Start Command** to: `python api_server.py`

### 3.3 Set Environment Variables

Go to **Variables** tab and add:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# Flask Configuration
FLASK_PORT=8000
FLASK_DEBUG=false
FLASK_API_URL=${{RAILWAY_PUBLIC_DOMAIN}}  # Railway will provide this

# Railway automatically sets:
# PORT (use this in code)
# RAILWAY_ENVIRONMENT
```

**Note**: Railway sets `PORT` automatically. Use it in your code:
```python
port = int(os.getenv('PORT', 8000))
```

### 3.4 Configure Domain

1. Go to **Settings** → **Networking**
2. Railway will generate a public domain (e.g., `your-app.up.railway.app`)
3. Copy this URL - you'll need it for frontend configuration
4. Optionally, add a custom domain

---

## Step 4: Verify Deployment

### 4.1 Check Logs

In Railway dashboard:
1. Go to **Deployments** tab
2. Click on the latest deployment
3. View logs to ensure app started successfully

You should see:
```
🚀 Starting Cosmic Diary API Server on port XXXXX
📊 Swiss Ephemeris version: 2.10.03
🔮 Using Ayanamsa: Lahiri (SIDM_LAHIRI)
```

### 4.2 Test Health Endpoint

```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "cosmic-diary-api",
  "swiss_ephemeris_version": "2.10.03"
}
```

### 4.3 Test Planetary Endpoint

```bash
curl "https://your-app.up.railway.app/api/planets/daily?date=2025-12-12"
```

---

## Step 5: Update Frontend Configuration

Update your `.env.local` for Next.js:

```env
NEXT_PUBLIC_FLASK_API_URL=https://your-app.up.railway.app
```

Or if deploying to Vercel, add this as an environment variable in Vercel dashboard.

---

## Step 6: Troubleshooting

### Issue: Build Fails

**Error**: `ModuleNotFoundError: No module named 'pyswisseph'`

**Solution**:
- Ensure `requirements.txt` includes `pyswisseph==2.10.3.2`
- Check Railway logs for installation errors

### Issue: App Crashes on Startup

**Error**: `Port already in use` or `Address already in use`

**Solution**:
- Use `PORT` environment variable (Railway sets this automatically)
- Update `api_server.py` to use `os.getenv('PORT')`

### Issue: CORS Errors

**Error**: Frontend can't call backend API

**Solution**:
- Ensure `flask-cors` is installed
- Check CORS is configured in `api_server.py`:
  ```python
  from flask_cors import CORS
  CORS(app)  # Allow all origins (or configure specific origins)
  ```

### Issue: Environment Variables Not Working

**Solution**:
- Verify variables are set in Railway dashboard → Variables
- Check variable names match exactly (case-sensitive)
- Redeploy after changing environment variables

### Issue: Swiss Ephemeris Not Working

**Solution**:
- `pyswisseph` includes ephemeris files, but may need system libraries
- Railway uses Debian/Ubuntu base image
- If issues persist, check Railway logs for specific errors

---

## Step 7: Monitor and Maintain

### 7.1 View Logs

Railway provides real-time logs:
- Go to **Deployments** → Latest deployment → View logs

### 7.2 Set Up Monitoring (Optional)

Railway provides:
- Metrics dashboard (CPU, Memory, Network)
- Log aggregation
- Error tracking

### 7.3 Auto-Deployments

Railway automatically deploys when you push to GitHub:
- Push to `main` branch → Auto-deploy
- Create pull request → Preview deployment (optional)

---

## Step 8: Scale and Optimize

### 8.1 Scale Resources

In Railway dashboard:
- Go to **Settings** → **Resource**
- Adjust CPU and RAM as needed
- Start with free tier, scale up if needed

### 8.2 Enable HTTP/2

Railway supports HTTP/2 automatically via Cloudflare.

### 8.3 Add Health Check

Railway can monitor your health endpoint:
- Go to **Settings** → **Health Check**
- Set path: `/health`
- Set interval: 30 seconds

---

## Configuration Summary

### Railway Settings

- **Root Directory**: `CosmicDiary`
- **Start Command**: `python api_server.py`
- **Build Command**: (auto-detected from `requirements.txt`)

### Required Environment Variables

```env
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
PORT (set automatically by Railway)
```

### Optional Environment Variables

```env
FLASK_DEBUG=false
FLASK_API_URL=${{RAILWAY_PUBLIC_DOMAIN}}
```

---

## Next Steps

1. ✅ Verify backend is working at Railway URL
2. ✅ Deploy frontend to Vercel (see `VERCEL_DEPLOYMENT_GUIDE.md`)
3. ✅ Update frontend to use Railway backend URL
4. ✅ Test end-to-end functionality

---

## Useful Commands

```bash
# View Railway logs (CLI)
railway logs

# Connect to Railway CLI (if installed)
railway link

# View environment variables
railway variables

# Open Railway dashboard
railway open
```

---

**Last Updated**: 2025-12-12

