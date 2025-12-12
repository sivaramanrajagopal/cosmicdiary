# ✅ Vercel Configuration - Quick Reference

## Your Railway Backend URL

**Public URL**: `https://cosmicdiary-production.up.railway.app`

---

## 🔧 Vercel Environment Variables

Go to: **Vercel Dashboard** → **Your Project** → **Settings** → **Environment Variables**

### Required Variables:

| Variable | Value | Environments |
|----------|-------|--------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL | ✅ Production<br>✅ Preview<br>✅ Development |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Your Supabase anon key | ✅ Production<br>✅ Preview<br>✅ Development |
| `FLASK_API_URL` | `https://cosmicdiary-production.up.railway.app` | ✅ Production<br>✅ Preview<br>✅ Development |

### Optional Variables:

| Variable | Value | Purpose |
|----------|-------|---------|
| `SUPABASE_SERVICE_ROLE_KEY` | Your service role key | For server-side operations (if needed) |

---

## 📋 Configuration Checklist

- [x] Railway backend URL: `https://cosmicdiary-production.up.railway.app`
- [ ] `FLASK_API_URL` set in Vercel to: `https://cosmicdiary-production.up.railway.app`
- [ ] All environment variables added to Vercel
- [ ] Vercel redeployed after adding variables
- [ ] Railway backend is running and accessible
- [ ] CORS configured to allow Vercel domain

---

## 🧪 Testing the Connection

### 1. Test Railway Backend:
```bash
curl https://cosmicdiary-production.up.railway.app/health
```
Should return:
```json
{
  "status": "healthy",
  "service": "cosmic-diary-api",
  "swiss_ephemeris_version": "2.10.03"
}
```

### 2. Test from Vercel:
1. Open `https://cosmicdiary.vercel.app/`
2. Open browser DevTools (F12) → Console tab
3. Go to Planets page
4. Check for:
   - ✅ No CORS errors
   - ✅ Successful API calls
   - ✅ Planetary data loading

---

## 🔐 CORS Configuration

The Railway backend is configured to allow:
- ✅ `https://cosmicdiary.vercel.app` (your production domain)
- ✅ `https://*.vercel.app` (all Vercel preview deployments)
- ✅ `http://localhost:3000` (local development)

**Note**: If you need to add more domains, set the `ALLOWED_ORIGINS` environment variable in Railway:
```
ALLOWED_ORIGINS=https://cosmicdiary.vercel.app,https://your-other-domain.com
```

---

## 🚨 Common Issues

### Issue: CORS Error
**Error**: `Access to fetch at '...' has been blocked by CORS policy`

**Fix**:
1. Verify Railway is running
2. Check Railway logs
3. Ensure `FLASK_API_URL` is set correctly in Vercel
4. Redeploy Railway after CORS changes

### Issue: 404 or Connection Failed
**Fix**:
1. Verify Railway URL is correct: `https://cosmicdiary-production.up.railway.app`
2. Test Railway URL directly in browser
3. Check Railway service status
4. Ensure Railway service is not sleeping

### Issue: Environment Variable Not Working
**Fix**:
1. Variable must start with `NEXT_PUBLIC_` for client-side access
2. Redeploy Vercel after adding/changing variables
3. Check Vercel deployment logs for variable errors

---

**Last Updated**: 2025-12-12

