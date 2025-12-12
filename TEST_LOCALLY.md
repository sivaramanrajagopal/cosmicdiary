# 🧪 Testing Cosmic Diary Locally

**Quick Start Guide for Local Testing**

---

## 📋 Prerequisites

✅ Ensure you have:
- Python 3.9+ installed
- Node.js 18+ installed
- All dependencies installed (`pip install -r requirements.txt` and `npm install`)
- `.env.local` file configured with Supabase credentials

---

## 🚀 Starting the Application

### Step 1: Start Flask API Server

Open **Terminal 1** and run:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
python3 api_server.py
```

**Expected Output:**
```
🚀 Starting Cosmic Diary API Server on port 8000
📊 Swiss Ephemeris version: 2.10.03
🔮 Using Ayanamsa: Lahiri (SIDM_LAHIRI)
 * Serving Flask app 'api_server'
 * Running on http://127.0.0.1:8000
```

✅ **Keep this terminal open!**

---

### Step 2: Start Next.js Frontend

Open **Terminal 2** and run:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
npm run dev
```

**Expected Output:**
```
▲ Next.js 15.5.7
- Local:        http://localhost:3002
- Environments: .env.local, .env
✓ Ready in 2.6s
```

✅ **Keep this terminal open!**

---

## 🧪 Testing Steps

### Test 1: API Health Check

Open a browser or use curl:

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "cosmic-diary-api",
  "swiss_ephemeris_version": "2.10.03"
}
```

✅ **API is running!**

---

### Test 2: Planetary Data Calculation

```bash
curl "http://localhost:8000/api/planets/daily?date=2025-12-10"
```

**Expected:** JSON with all 9 planets including Rahu and Ketu

---

### Test 3: Verify Rahu/Ketu Fix

Run this Python test:

```bash
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')
from api_server import calculate_planet_position
import swisseph as swe
from datetime import date

jd = swe.julday(2025, 12, 10, 12.0/24.0, swe.GREG_CAL)

rahu = calculate_planet_position('Rahu', jd)
ketu = calculate_planet_position('Ketu', jd)

diff = abs(ketu['longitude'] - rahu['longitude'])
if diff > 180:
    diff = 360 - diff

print(f"Rahu: {rahu['longitude']:.2f}° ({rahu['rasi']['name']})")
print(f"Ketu: {ketu['longitude']:.2f}° ({ketu['rasi']['name']})")
print(f"Difference: {diff:.2f}°")

if abs(diff - 180.0) < 0.1:
    print("\n✅ SUCCESS: Rahu and Ketu are exactly 180° apart!")
else:
    print(f"\n❌ FAILED: Difference is {abs(diff - 180.0):.2f}° off")
PYEOF
```

**Expected Output:**
```
Rahu: 317.98° (Aquarius)
Ketu: 137.98° (Leo)
Difference: 180.00°

✅ SUCCESS: Rahu and Ketu are exactly 180° apart!
```

---

### Test 4: Frontend - Planets Page

1. Open browser: `http://localhost:3002/planets`
2. You should see:
   - Date picker
   - Table with all 9 planets
   - Rahu and Ketu should be 180° apart

**Check:**
- ✅ All 9 planets displayed
- ✅ Rahu longitude
- ✅ Ketu longitude
- ✅ Verify: `|Rahu - Ketu| = 180°`

---

### Test 5: Chart Calculation Endpoint (New)

```bash
curl -X POST http://localhost:8000/api/chart/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-10",
    "time": "14:30:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  }'
```

**Expected:** Complete chart data with ascendant, house cusps, and planetary positions

---

### Test 6: Timezone Detection

```bash
curl "http://localhost:8000/api/timezone/detect?lat=13.0827&lng=80.2707"
```

**Expected:**
```json
{
  "success": true,
  "latitude": 13.0827,
  "longitude": 80.2707,
  "timezone": "Asia/Kolkata"
}
```

---

### Test 7: Chart Validation

```bash
curl http://localhost:8000/api/chart/validate
```

**Expected:** JSON with Swiss Ephemeris version, available planets, supported features

---

## 🌐 Frontend Pages to Test

### 1. Home Page
**URL:** `http://localhost:3002/`
- Should show recent events
- Navigation links working

### 2. Planets Page
**URL:** `http://localhost:3002/planets`
- Date picker functional
- All planets displayed
- **CRITICAL:** Verify Rahu/Ketu are 180° apart

### 3. Events Page
**URL:** `http://localhost:3002/events`
- List of all events
- Links to event details

### 4. Analysis Page
**URL:** `http://localhost:3002/analysis`
- Event analysis
- Planetary correlations

### 5. House Analysis Page
**URL:** `http://localhost:3002/house-analysis`
- House mappings
- Planetary aspects

---

## 🐛 Troubleshooting

### Flask API not starting?

**Check:**
```bash
# Verify port 8000 is free
lsof -i :8000

# Check Python dependencies
pip list | grep -E "flask|swisseph|supabase"
```

### Next.js not starting?

**Check:**
```bash
# Verify port 3002 is free (or 3000)
lsof -i :3002

# Check Node dependencies
npm list --depth=0
```

### Rahu/Ketu still wrong?

**Verify the fix is applied:**
```bash
grep -A 5 "Special handling for Ketu" api_server.py
```

Should show:
```python
rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
```

Not:
```python
rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SWIEPH)  # WRONG!
```

---

## ✅ Success Criteria

- ✅ Flask API responds to `/health`
- ✅ Planetary data calculated correctly
- ✅ Rahu and Ketu exactly 180° apart
- ✅ Frontend displays all planets
- ✅ All pages load without errors
- ✅ Date picker works
- ✅ Chart calculation endpoint works

---

## 🎯 Quick Test Script

Save this as `quick_test.sh`:

```bash
#!/bin/bash

echo "🧪 Quick Test Suite"
echo "==================="

# Test 1: API Health
echo -n "Test 1: API Health... "
curl -s http://localhost:8000/health | grep -q "healthy" && echo "✅" || echo "❌"

# Test 2: Planetary Data
echo -n "Test 2: Planetary Data... "
curl -s "http://localhost:8000/api/planets/daily?date=2025-12-10" | grep -q "planets" && echo "✅" || echo "❌"

# Test 3: Rahu/Ketu (180° apart)
echo -n "Test 3: Rahu/Ketu Fix... "
python3 -c "
import sys; sys.path.insert(0, '.')
from api_server import calculate_planet_position
import swisseph as swe
jd = swe.julday(2025, 12, 10, 12.0/24.0, swe.GREG_CAL)
rahu = calculate_planet_position('Rahu', jd)
ketu = calculate_planet_position('Ketu', jd)
diff = abs(ketu['longitude'] - rahu['longitude'])
if diff > 180: diff = 360 - diff
exit(0 if abs(diff - 180.0) < 0.1 else 1)
" && echo "✅" || echo "❌"

echo ""
echo "Tests complete!"
```

Make it executable and run:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

---

**Happy Testing!** 🌙✨

