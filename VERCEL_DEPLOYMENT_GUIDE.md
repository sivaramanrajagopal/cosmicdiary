# ▲ Vercel Deployment Guide (Next.js Frontend)

Complete guide to deploy the Cosmic Diary Next.js frontend to Vercel.

---

## Prerequisites

1. **Vercel account** (sign up at [vercel.com](https://vercel.com))
2. **GitHub account** with repository pushed
3. **Railway backend URL** (or local Flask API URL for testing)
4. **Supabase project** credentials

---

## Step 1: Verify Project Configuration

### 1.1 Check `vercel.json`

Ensure `vercel.json` exists in `CosmicDiary/`:

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

### 1.2 Check `next.config.js`

Verify your `next.config.js` is configured correctly:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Add any necessary configuration
}

module.exports = nextConfig
```

---

## Step 2: Prepare Environment Variables

You'll need these environment variables in Vercel:

### Required Variables

```env
# Supabase (Public - prefixed with NEXT_PUBLIC_)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Backend API URL (Public - for frontend to call)
NEXT_PUBLIC_FLASK_API_URL=https://your-app.up.railway.app
```

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

---

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)**
   - Sign in with GitHub

2. **Create New Project**
   - Click **"Add New"** → **"Project"**
   - Import your GitHub repository: `cosmicdiary`

3. **Configure Project**
   - **Root Directory**: Select `CosmicDiary` (if not auto-detected)
   - **Framework Preset**: Next.js (should auto-detect)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

4. **Add Environment Variables**
   - Go to **"Environment Variables"** section
   - Add each variable:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
     - `NEXT_PUBLIC_FLASK_API_URL`
   - Select **"Production"**, **"Preview"**, and **"Development"** for each

5. **Deploy**
   - Click **"Deploy"**
   - Wait for build to complete (2-5 minutes)

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Navigate to project directory
cd /path/to/CosmicDiary/CosmicDiary

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No (for first deploy)
# - Project name? cosmic-diary (or your preferred name)
# - Directory? ./
# - Override settings? No

# Add environment variables
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add NEXT_PUBLIC_FLASK_API_URL

# Deploy to production
vercel --prod
```

---

## Step 4: Verify Deployment

### 4.1 Check Build Logs

In Vercel dashboard:
1. Go to **Deployments**
2. Click on the latest deployment
3. View build logs

You should see:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages
```

### 4.2 Test the Deployed Site

1. Click the deployment URL (e.g., `cosmic-diary.vercel.app`)
2. Verify:
   - Home page loads
   - Navigation works
   - Events page loads
   - Can create new events
   - Planetary data displays
   - Charts render correctly

### 4.3 Test API Integration

Open browser console and verify:
- No CORS errors
- API calls to Railway backend succeed
- Supabase connection works

---

## Step 5: Configure Custom Domain (Optional)

1. **In Vercel Dashboard**
   - Go to **Settings** → **Domains**
   - Click **"Add Domain"**
   - Enter your domain (e.g., `cosmicdiary.com`)

2. **Configure DNS**
   - Add DNS records as instructed by Vercel:
     - **A Record**: `@` → Vercel IP
     - **CNAME**: `www` → `cname.vercel-dns.com`

3. **Wait for SSL**
   - Vercel automatically provisions SSL certificates
   - Wait 1-24 hours for DNS propagation

---

## Step 6: Update Backend CORS (If Needed)

If you get CORS errors, update `api_server.py`:

```python
from flask_cors import CORS

# Allow specific origins (more secure)
CORS(app, origins=[
    "https://cosmic-diary.vercel.app",
    "https://your-custom-domain.com",
    "http://localhost:3000"  # For local development
])
```

Then redeploy to Railway.

---

## Step 7: Environment Variables Management

### 7.1 Production vs Preview

Vercel supports three environments:
- **Production**: Live site (main branch)
- **Preview**: Pull request previews
- **Development**: Local development (`vercel dev`)

Set environment variables for each environment as needed.

### 7.2 Update Variables

1. Go to **Settings** → **Environment Variables**
2. Edit or add variables
3. Redeploy (or wait for next deployment)

### 7.3 Secrets Management

For sensitive values:
- Never commit `.env.local` to git
- Use Vercel's environment variables
- Use Vercel's **Secrets** feature for sensitive data

---

## Step 8: Monitoring and Analytics

### 8.1 Vercel Analytics (Optional)

Enable in dashboard:
- Go to **Settings** → **Analytics**
- Enable **Vercel Analytics** (free tier available)

### 8.2 Error Tracking

Vercel provides:
- Error logs in dashboard
- Function logs
- Performance metrics

### 8.3 Web Vitals

Monitor Core Web Vitals:
- Go to **Analytics** tab
- View performance metrics

---

## Step 9: Continuous Deployment

### 9.1 Automatic Deployments

Vercel automatically:
- Deploys on push to `main` branch → Production
- Creates preview deployments for pull requests

### 9.2 Build Settings

Configure in **Settings** → **General**:
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 9.3 Ignore Build Step

Add `vercel.json` ignore pattern if needed:
```json
{
  "ignoreCommand": "git diff HEAD^ HEAD --quiet ./"
}
```

---

## Troubleshooting

### Issue: Build Fails

**Error**: `Module not found` or `Build error`

**Solution**:
- Check build logs for specific error
- Ensure `package.json` has all dependencies
- Try `npm install` locally to verify
- Clear Vercel build cache (Settings → General → Clear)

### Issue: Environment Variables Not Working

**Error**: Variables undefined in browser

**Solution**:
- Variables must be prefixed with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding/updating variables
- Check variable names match exactly

### Issue: API Calls Fail

**Error**: CORS or connection refused

**Solution**:
- Verify `NEXT_PUBLIC_FLASK_API_URL` is correct
- Check Railway backend is running
- Verify CORS is configured in Flask backend
- Check network tab in browser DevTools

### Issue: Supabase Connection Fails

**Error**: Supabase client initialization fails

**Solution**:
- Verify `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Check Supabase project is active
- Verify RLS policies allow access

### Issue: Images/Assets Not Loading

**Solution**:
- Ensure images are in `public/` directory
- Use Next.js `Image` component for optimized images
- Check file paths are correct

---

## Configuration Summary

### Vercel Settings

- **Framework**: Next.js
- **Root Directory**: `CosmicDiary`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Required Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_FLASK_API_URL
```

---

## Post-Deployment Checklist

- [ ] Site loads at Vercel URL
- [ ] All pages accessible
- [ ] Can create events
- [ ] Planetary data displays
- [ ] Charts render correctly
- [ ] API calls to Railway succeed
- [ ] Supabase connection works
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Custom domain configured (if applicable)

---

## Next Steps

1. ✅ Frontend deployed to Vercel
2. ✅ Backend deployed to Railway
3. ✅ Update GitHub Actions to use production URLs
4. ✅ Test end-to-end functionality
5. ✅ Set up monitoring and alerts

---

## Useful Commands

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View deployments
vercel list

# View logs
vercel logs

# Pull environment variables
vercel env pull .env.local

# Run locally with Vercel
vercel dev
```

---

**Last Updated**: 2025-12-12

