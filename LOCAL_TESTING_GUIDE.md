# 🧪 Local Testing Guide

Complete guide to test Cosmic Diary locally before deployment.

---

## Prerequisites

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **Supabase account** with project created
4. **OpenAI API key**
5. **Git** installed

---

## Step 1: Clone and Setup

```bash
cd /path/to/workspace
git clone https://github.com/sivaramanrajagopal/cosmicdiary.git
cd cosmicdiary/CosmicDiary
```

---

## Step 2: Database Setup

### 2.1 Apply Database Migrations

1. Go to your Supabase project dashboard
2. Open SQL Editor
3. Run migrations in order:
   - `database_migrations/001_add_time_to_events.sql`
   - `database_migrations/002_create_event_chart_data_table.sql`
   - `database_migrations/003_update_house_mappings.sql`
   - `database_migrations/007_add_astrological_metadata.sql`
   - `database_migrations/008_create_cosmic_snapshots.sql`
   - `database_migrations/009_create_event_cosmic_correlations.sql`

### 2.2 Get Supabase Credentials

From Supabase Dashboard → Settings → API:
- **Project URL** (e.g., `https://xxxxx.supabase.co`)
- **anon key** (Public anon key)
- **service_role key** (Secret service role key - keep safe!)

---

## Step 3: Environment Variables

### 3.1 Create `.env.local` for Backend

```bash
cd /path/to/CosmicDiary
nano .env.local  # or use your preferred editor
```

Add the following:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# Flask API Configuration (for local development)
FLASK_PORT=8000
FLASK_DEBUG=true
FLASK_API_URL=http://localhost:8000

# Optional: Email Configuration (if using email reports)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### 3.2 Create `.env.local` for Frontend

```bash
cd /path/to/CosmicDiary
nano .env.local  # Same file, add frontend vars
```

Add/verify frontend variables:

```env
# Next.js Public Variables (prefixed with NEXT_PUBLIC_)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Backend API URL (for frontend to call Flask API)
NEXT_PUBLIC_FLASK_API_URL=http://localhost:8000
```

---

## Step 4: Backend Setup (Flask API)

### 4.1 Install Python Dependencies

```bash
cd /path/to/CosmicDiary
python3 -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Linux/Mac)
# OR
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 4.2 Test Backend

```bash
# Start Flask API server
python3 api_server.py

# In another terminal, test the health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "cosmic-diary-api",
  "swiss_ephemeris_version": "2.10.03"
}
```

### 4.3 Test Planetary Calculations

```bash
# Test daily planetary data
curl "http://localhost:8000/api/planets/daily?date=2025-12-12"

# Test chart calculation endpoint
curl -X POST http://localhost:8000/api/chart/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-12",
    "time": "10:30:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

---

## Step 5: Frontend Setup (Next.js)

### 5.1 Install Node Dependencies

```bash
cd /path/to/CosmicDiary
npm install
```

### 5.2 Start Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## Step 6: Test Complete System

### 6.1 Test Event Creation

1. Open browser: `http://localhost:3000`
2. Navigate to "Events" → "New Event"
3. Create a test event with:
   - Title: "Test Event"
   - Date: Today
   - Category: "Technology"
   - Location with coordinates
   - Time (optional)

4. Verify event appears in events list

### 6.2 Test Planetary Data

1. Navigate to "Planets" page
2. Select a date
3. Verify planetary positions display correctly
4. Check retrograde status (Rahu/Ketu should always be retrograde)

### 6.3 Test Chart Display

1. Navigate to an event detail page
2. Verify chart displays (North Indian / South Indian)
3. Check planetary positions in chart
4. Verify house mapping shows correct houses

### 6.4 Test Analysis Page

1. Navigate to "Analysis" page
2. Verify event correlations are calculated
3. Check planetary patterns display

---

## Step 7: Test Event Collection Script

### 7.1 Test Enhanced Event Collection

```bash
# Make sure Flask API is running first
python3 api_server.py  # In one terminal

# In another terminal, run event collection
python3 collect_events_with_cosmic_state.py
```

Expected output:
```
================================================================================
COSMIC DIARY - ENHANCED EVENT COLLECTION WITH COSMIC STATE CORRELATION
Run Time: 2025-12-12 10:30:00 UTC
================================================================================

STEP 1: CAPTURING COSMIC STATE
--------------------------------------------------------------------------------
📅 Snapshot Time: 2025-12-12T10:30:00.000Z
📍 Reference Location: Delhi, India
...
✓ Snapshot stored with ID: 1

STEP 2: DETECTING EVENTS VIA OPENAI
--------------------------------------------------------------------------------
...
```

### 7.2 Test Import Script (Alternative)

```bash
# Test the import script with enhanced prompts
python3 import_automated_events.py

# Or test with specific date
python3 import_automated_events.py 2025-12-12
```

---

## Step 8: Verify Database

### 8.1 Check Events Table

```bash
# Connect to Supabase SQL Editor and run:
SELECT COUNT(*) as total_events FROM events;
SELECT * FROM events ORDER BY created_at DESC LIMIT 5;
```

### 8.2 Check Cosmic Snapshots

```sql
SELECT COUNT(*) as total_snapshots FROM cosmic_snapshots;
SELECT snapshot_time, lagna_rasi, lagna_rasi_number 
FROM cosmic_snapshots 
ORDER BY snapshot_time DESC 
LIMIT 5;
```

### 8.3 Check Correlations

```sql
SELECT 
  e.title,
  cs.snapshot_time,
  ecc.correlation_score,
  ecc.total_matches
FROM event_cosmic_correlations ecc
JOIN events e ON ecc.event_id = e.id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
ORDER BY ecc.correlation_score DESC
LIMIT 10;
```

---

## Troubleshooting

### Flask API Not Starting

**Error**: `ModuleNotFoundError: No module named 'swisseph'`

**Solution**:
```bash
pip install pyswisseph==2.10.3.2
```

**Error**: Port 8000 already in use

**Solution**:
```bash
# Change port in .env.local
FLASK_PORT=8001

# Or kill process using port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
```

### Next.js Build Errors

**Error**: Environment variables not found

**Solution**:
- Ensure `.env.local` exists in `CosmicDiary/` directory
- Variables must be prefixed with `NEXT_PUBLIC_` for client-side access
- Restart Next.js dev server after changing `.env.local`

### Database Connection Issues

**Error**: `Invalid API key` or `Connection refused`

**Solution**:
- Verify Supabase URL and keys in `.env.local`
- Check if Supabase project is active
- Ensure service role key is used (not anon key) for backend scripts

### Swiss Ephemeris Errors

**Error**: Swiss Ephemeris calculation fails

**Solution**:
- Verify `pyswisseph==2.10.3.2` is installed
- Check if ephemeris files are downloaded (should be automatic)
- For Linux, may need: `sudo apt-get install libsweph1 libsweph-dev`

---

## Quick Test Checklist

- [ ] Flask API responds to `/health`
- [ ] Planetary data endpoint returns data
- [ ] Chart calculation endpoint works
- [ ] Next.js frontend loads at localhost:3000
- [ ] Can create new events
- [ ] Planetary positions display correctly
- [ ] Chart visualization works
- [ ] Event collection script runs successfully
- [ ] Database tables are populated
- [ ] Correlations are stored

---

## Next Steps

Once local testing passes:
1. ✅ Deploy backend to Railway (see `RAILWAY_DEPLOYMENT_GUIDE.md`)
2. ✅ Deploy frontend to Vercel (see `VERCEL_DEPLOYMENT_GUIDE.md`)
3. ✅ Set up GitHub Actions for automated event collection

---

**Last Updated**: 2025-12-12

