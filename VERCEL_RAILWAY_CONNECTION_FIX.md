# 🔧 Vercel-Railway Connection Fix Guide

## Problem

Vercel frontend (`https://cosmicdiary.vercel.app/`) is not connecting to Railway backend.

## Root Causes

1. **Wrong Railway URL**: Using `cosmicdiary.railway.internal` (internal URL) instead of public Railway URL
2. **CORS Configuration**: Backend needs to allow Vercel domain
3. **Environment Variable**: `FLASK_API_URL` in Vercel must be set to public Railway URL

---

## ✅ Solution Steps

### Step 1: Get Railway Public URL

1. Go to **Railway Dashboard** → Your Project → Your Service
2. Go to **Settings** → **Networking**
3. Find **Public Domain** (e.g., `cosmicdiary-production.up.railway.app`)
4. **Copy this URL** - this is your public Railway URL

**Important**: 
- ❌ **DO NOT** use `cosmicdiary.railway.internal` (internal only)
- ✅ **USE** the public domain like `https://cosmicdiary-production.up.railway.app`

### Step 2: Update CORS in Railway Backend

The code has been updated to allow Vercel domain. If you need to add more domains:

**Option A: Use Environment Variable (Recommended)**

In Railway Dashboard → Variables, add:

```
ALLOWED_ORIGINS=https://cosmicdiary.vercel.app,https://*.vercel.app,http://localhost:3000
```

**Option B: Update Code Directly**

The code now includes Vercel domain by default. Redeploy to Railway after code update.

### Step 3: Configure Vercel Environment Variable

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**

2. **Add or Update:**
   ```
   FLASK_API_URL=https://cosmicdiary-production.up.railway.app
   ```
   (Replace with your actual Railway public URL)

3. **Select Environments:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

4. **Save** and **Redeploy**

### Step 4: Verify Railway Backend is Accessible

Test the Railway URL directly:

```bash
# Test health endpoint
curl https://cosmicdiary-production.up.railway.app/health

# Should return:
# {"status":"healthy","service":"cosmic-diary-api","swiss_ephemeris_version":"2.10.03"}
```

### Step 5: Test Connection from Vercel

1. Open browser console on `https://cosmicdiary.vercel.app/`
2. Go to Network tab
3. Navigate to Planets page or create an event
4. Check for API calls:
   - ✅ Should see calls to `/api/planetary-data`
   - ✅ Should NOT see CORS errors
   - ✅ Should see successful responses

---

## 🔍 Troubleshooting

### Issue: Still Getting CORS Errors

**Error**: `Access to fetch at '...' has been blocked by CORS policy`

**Solution**:
1. Verify Railway backend is running
2. Check Railway logs for CORS errors
3. Verify `ALLOWED_ORIGINS` includes Vercel URL
4. Redeploy Railway after CORS changes

### Issue: 404 Not Found

**Error**: `Failed to fetch` or `404 Not Found`

**Solution**:
1. Verify Railway URL is correct (public domain, not internal)
2. Test Railway URL directly in browser
3. Check Railway service is running
4. Verify `FLASK_API_URL` in Vercel matches Railway URL exactly

### Issue: Connection Timeout

**Error**: `Network request failed` or timeout

**Solution**:
1. Check Railway service is running (not sleeping)
2. Verify Railway URL is accessible
3. Check Railway logs for errors
4. Increase timeout in API routes if needed

---

## 📋 Quick Checklist

- [ ] Railway public URL obtained (not `.internal`)
- [ ] CORS updated in `api_server.py` (includes Vercel domain)
- [ ] Railway redeployed with CORS changes
- [ ] `FLASK_API_URL` set in Vercel to Railway public URL
- [ ] Vercel redeployed after environment variable change
- [ ] Railway backend accessible via public URL
- [ ] No CORS errors in browser console
- [ ] API calls succeed from Vercel

---

## 🔐 Current CORS Configuration

The backend now allows:
- ✅ `https://cosmicdiary.vercel.app` (production)
- ✅ `https://*.vercel.app` (all Vercel preview deployments)
- ✅ `http://localhost:3000` (local development)
- ✅ `http://localhost:3001` (alternative local port)
- ✅ `http://127.0.0.1:3000` (local IP)

---

## 📝 Environment Variables Summary

### Railway (Backend):
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
OPENAI_API_KEY=sk-your-openai-key
ALLOWED_ORIGINS=https://cosmicdiary.vercel.app,https://*.vercel.app (optional)
```

### Vercel (Frontend):
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
FLASK_API_URL=https://cosmicdiary-production.up.railway.app
```

**Important**: Use Railway **public URL**, not `.railway.internal`!

---

**Last Updated**: 2025-12-12

