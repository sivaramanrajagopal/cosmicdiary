# 🔐 Environment Variables Configuration Guide

Complete guide for configuring environment variables in Railway (Backend) and Vercel (Frontend).

---

## 📋 Quick Reference

### Railway (Backend) - Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | ✅ Yes | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ Yes | Supabase service role key (secret) |
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for event detection |
| `PORT` | ⚠️ Auto-set | Railway automatically sets this |
| `FLASK_DEBUG` | ❌ No | Set to `false` for production |

### Vercel (Frontend) - Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | ✅ Yes | Supabase project URL (public) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ Yes | Supabase anon key (public) |
| `FLASK_API_URL` | ✅ Yes | Railway backend URL |

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

---

## 🚂 Railway Configuration (Backend)

### Step 1: Get Railway Deployment URL

1. Deploy your Flask API to Railway (see `RAILWAY_DEPLOYMENT_GUIDE.md`)
2. Railway will provide a URL like: `https://your-app.up.railway.app`
3. **Copy this URL** - you'll need it for Vercel configuration

### Step 2: Add Environment Variables in Railway

Go to **Railway Dashboard** → Your Project → Your Service → **Variables** tab:

#### Required Variables:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional Variables:

```env
FLASK_DEBUG=false
HOST=0.0.0.0
```

**Note**: `PORT` is automatically set by Railway - **DO NOT** set it manually.

### Step 3: Configure CORS (Already Done)

✅ **CORS is already configured** in `api_server.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins
```

This allows your Vercel frontend to call the Railway backend.

**If you need to restrict CORS to specific domains**, update `api_server.py`:

```python
CORS(app, origins=[
    "https://your-vercel-app.vercel.app",
    "https://your-custom-domain.com"
])
```

---

## ▲ Vercel Configuration (Frontend)

### Step 1: Add Environment Variables

Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**:

#### Required Variables:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
FLASK_API_URL=https://web-production-946b5.up.railway.app
```

**Important**: 
- Variables starting with `NEXT_PUBLIC_` are exposed to the browser
- Use `FLASK_API_URL` (without `NEXT_PUBLIC_`) for server-side API routes

### Step 2: Configure for All Environments

When adding variables in Vercel, select all three environments:
- ✅ **Production**
- ✅ **Preview** 
- ✅ **Development**

This ensures variables work in all deployments.

### Step 3: Redeploy After Adding Variables

After adding/updating environment variables:
1. Go to **Deployments** tab
2. Click **"..."** on the latest deployment
3. Click **"Redeploy"**
4. Or push a new commit to trigger auto-deployment

---

## 🔍 How Environment Variables Are Used

### Backend (Railway) - Server-Side Only

#### `api_server.py` Uses:

```python
# From environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 8000))  # Railway sets PORT automatically
```

**These are NEVER exposed to the browser** - they're server-side only.

### Frontend (Vercel) - Mixed Usage

#### Server-Side API Routes (`src/app/api/**/*.ts`)

**Use**: `FLASK_API_URL` (without `NEXT_PUBLIC_` prefix)

```typescript
// src/app/api/planetary-data/route.ts
const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';
// Used in server-side API routes only
```

**Why**: Server-side routes run on Vercel's server, not in the browser.

#### Client-Side Components

**Use**: `NEXT_PUBLIC_*` prefixed variables

```typescript
// src/lib/supabase.ts
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// Used in browser
```

**Why**: These run in the browser, so they must be public.

---

## 📝 Complete Configuration Checklist

### ✅ Railway (Backend)

- [ ] `SUPABASE_URL` - Supabase project URL
- [ ] `SUPABASE_SERVICE_ROLE_KEY` - Service role key (secret)
- [ ] `OPENAI_API_KEY` - OpenAI API key
- [ ] `FLASK_DEBUG=false` - Production mode (optional)
- [ ] CORS enabled (already configured in code)
- [ ] Railway URL copied for Vercel configuration

### ✅ Vercel (Frontend)

- [ ] `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anon key
- [ ] `FLASK_API_URL` - Railway backend URL
- [ ] Variables added for Production, Preview, and Development
- [ ] Redeployed after adding variables

---

## 🔐 Security Best Practices

### ✅ Do's

1. **Use Service Role Key in Railway** (backend only)
   - ✅ Never expose service role key to browser
   - ✅ Use it only in server-side code

2. **Use Anon Key in Vercel** (frontend)
   - ✅ Anon key is safe for browser
   - ✅ RLS policies protect your data

3. **Use `NEXT_PUBLIC_` Prefix Carefully**
   - ✅ Only for variables needed in browser
   - ✅ Never put secrets in `NEXT_PUBLIC_` variables

### ❌ Don'ts

1. ❌ **Never** put `SUPABASE_SERVICE_ROLE_KEY` in Vercel
2. ❌ **Never** put `OPENAI_API_KEY` in `NEXT_PUBLIC_` prefix
3. ❌ **Never** commit `.env.local` to Git
4. ❌ **Never** use `SUPABASE_SERVICE_ROLE_KEY` in frontend code

---

## 🔧 CORS Configuration

### Current Setup

**CORS is already configured** in `api_server.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Allows all origins
```

This means **no additional CORS configuration needed** in Vercel.

### How It Works

1. **Frontend (Vercel)** makes request to **Backend (Railway)**
2. **Backend** responds with CORS headers
3. **Browser** allows the request (CORS check passes)

**Example Request Flow:**

```
Browser (Vercel) → Request → Railway Backend
                                      ↓
                    CORS Headers Added ← Flask CORS Middleware
                                      ↓
Browser ← Response (with CORS headers) ← Railway Backend
```

### Restricting CORS (Optional)

If you want to restrict CORS to specific domains only, update `api_server.py`:

```python
CORS(app, origins=[
    "https://your-app.vercel.app",
    "https://your-custom-domain.com",
    "http://localhost:3000"  # For local development
])
```

Then redeploy to Railway.

---

## 🌐 Backend Endpoint Configuration

### Option 1: Server-Side API Routes (Recommended)

**How it works**: Next.js API routes act as a proxy to Railway backend.

**File**: `src/app/api/planetary-data/route.ts`

```typescript
const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  // Server-side: calls Railway backend
  const response = await fetch(`${FLASK_API_URL}/api/planets/daily?date=${date}`);
  return response.json();
}
```

**Benefits**:
- ✅ Hides Railway URL from browser
- ✅ Can add authentication/rate limiting
- ✅ Better error handling

**Vercel Environment Variable:**
```
FLASK_API_URL=https://web-production-946b5.up.railway.app
```

### Option 2: Direct Browser Calls (Alternative)

If you want to call Railway directly from browser:

1. **Add to Vercel:**
   ```
   NEXT_PUBLIC_FLASK_API_URL=https://web-production-946b5.up.railway.app
   ```

2. **Update CORS in Railway:**
   ```python
   CORS(app, origins=["https://your-app.vercel.app"])
   ```

**Note**: Option 1 (Server-Side Proxy) is recommended and already implemented.

---

## 🧪 Testing Configuration

### Test Railway Backend

```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Test planetary data
curl "https://your-app.up.railway.app/api/planets/daily?date=2025-12-12"
```

### Test Vercel Frontend

1. Open deployed site: `https://your-app.vercel.app`
2. Open browser console (F12)
3. Check for errors:
   - ✅ No CORS errors
   - ✅ No "API URL not found" errors
   - ✅ Supabase connection works

### Test Environment Variables

**In Vercel:**

```typescript
// Add temporarily to test (remove after)
console.log('Backend URL:', process.env.FLASK_API_URL);  // Server-side only
console.log('Supabase URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);  // Client-side
```

**In Railway:**

Check logs for environment variable usage:
- Railway Dashboard → Deployments → View Logs
- Look for startup messages showing configuration

---

## 🐛 Troubleshooting

### Issue: CORS Error in Browser

**Error**: `Access to fetch at '...' has been blocked by CORS policy`

**Solution**:
1. ✅ Verify CORS is enabled in `api_server.py`: `CORS(app)`
2. ✅ Check Railway backend is accessible
3. ✅ Verify Railway URL is correct in Vercel
4. ✅ If needed, restrict CORS origins explicitly

### Issue: Environment Variable Undefined

**Error**: `process.env.FLASK_API_URL is undefined`

**Solution**:
1. ✅ Check variable name matches exactly (case-sensitive)
2. ✅ Verify variable is added in Vercel (Settings → Environment Variables)
3. ✅ Redeploy after adding variables
4. ✅ Check if variable needs `NEXT_PUBLIC_` prefix

### Issue: Supabase Connection Fails

**Error**: `Invalid API key` or `Supabase client error`

**Solution**:
1. ✅ Verify `NEXT_PUBLIC_SUPABASE_URL` is correct
2. ✅ Verify `NEXT_PUBLIC_SUPABASE_ANON_KEY` is correct
3. ✅ Check Supabase project is active
4. ✅ Ensure RLS policies allow access

### Issue: Backend API Not Found

**Error**: `Failed to fetch from Railway backend`

**Solution**:
1. ✅ Verify Railway backend is running
2. ✅ Check `FLASK_API_URL` in Vercel matches Railway URL
3. ✅ Test Railway URL directly in browser
4. ✅ Check Railway logs for errors

---

## 📋 Complete Environment Variables List

### Railway (Backend) - All Variables

```env
# Required
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci... (service role key)
OPENAI_API_KEY=sk-... (OpenAI API key)

# Auto-set by Railway
PORT=XXXXX (automatically set, don't set manually)

# Optional
FLASK_DEBUG=false
HOST=0.0.0.0
```

### Vercel (Frontend) - All Variables

```env
# Required - Public (browser accessible)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci... (anon key)

# Required - Server-side only
FLASK_API_URL=https://web-production-946b5.up.railway.app

# Optional - For email notifications (if enabled)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
ENABLE_EMAIL_NOTIFICATIONS=true
```

---

## 🔄 Quick Setup Commands

### Railway Setup

```bash
# 1. Get Supabase credentials
# From Supabase Dashboard → Settings → API

# 2. Get OpenAI API key
# From OpenAI Dashboard → API Keys

# 3. Add to Railway Dashboard → Variables
SUPABASE_URL=<your-url>
SUPABASE_SERVICE_ROLE_KEY=<your-key>
OPENAI_API_KEY=<your-key>
```

### Vercel Setup

```bash
# 1. Get Railway deployment URL
# From Railway Dashboard → Your Service → Settings → Networking

# 2. Add to Vercel Dashboard → Settings → Environment Variables
NEXT_PUBLIC_SUPABASE_URL=<your-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-key>
FLASK_API_URL=<railway-url>
```

---

## ✅ Verification Checklist

After configuration:

- [ ] Railway backend responds to `/health` endpoint
- [ ] Railway backend has all required environment variables
- [ ] Vercel frontend has all required environment variables
- [ ] Vercel site loads without errors
- [ ] No CORS errors in browser console
- [ ] Events can be created/listed
- [ ] Planetary data displays correctly
- [ ] Charts render correctly

---

**Last Updated**: 2025-12-12

