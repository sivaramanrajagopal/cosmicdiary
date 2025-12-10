# 🚀 Quick Implementation Guide

**For developers implementing Cosmic Diary from scratch**

---

## 📋 Pre-Implementation Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.9+ installed
- [ ] Supabase account created
- [ ] Git repository cloned
- [ ] Text editor/IDE ready

---

## ⚡ Quick Start (5 Steps)

### Step 1: Setup Environment

```bash
cd CosmicDiary
npm install
pip install -r requirements.txt
```

### Step 2: Configure Database

1. Go to Supabase Dashboard → SQL Editor
2. Copy entire `database_schema.sql`
3. Paste and execute
4. Verify tables created

### Step 3: Setup Environment Variables

Create `.env.local`:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
FLASK_API_URL=http://localhost:8000
```

### Step 4: Start Services

**Terminal 1 - Flask API:**
```bash
python3 api_server.py
```

**Terminal 2 - Next.js:**
```bash
npm run dev
```

### Step 5: Test

1. Visit http://localhost:3000 (or 3002)
2. Create a test event
3. Check `/house-analysis` page
4. Verify data in Supabase

---

## 📊 Data Flow Quick Reference

```
Event Created
    ↓
[Auto-triggers]
    ├─ House Mapping (mapEventToHouse)
    ├─ Aspect Calculation (calculatePlanetaryAspects)
    └─ Correlation Analysis (analyzeEventPlanetaryCorrelation)
    ↓
Stored in Database
    ├─ event_house_mappings
    ├─ event_planetary_aspects
    └─ event_planetary_correlations
```

---

## 🔧 Key Functions Reference

### House Mapping
```typescript
// Map event to house
import { mapEventToHouse } from '@/lib/houseMapping';
const mapping = mapEventToHouse(event, planetaryData);
// Returns: { house_number, rasi_name, house_significations, mapping_reason }
```

### Aspect Calculation
```typescript
// Calculate planetary aspects
import { calculatePlanetaryAspects } from '@/lib/houseMapping';
const aspects = calculatePlanetaryAspects(event, houseMapping, planetaryData);
// Returns: Array of aspect objects
```

### Store Everything
```typescript
// Complete calculation and storage
import { calculateAndStoreCorrelations } from '@/lib/storeCorrelations';
await calculateAndStoreCorrelations(event);
// Stores: mappings, aspects, correlations
```

---

## 📁 File Location Cheat Sheet

| What | Where |
|------|-------|
| Create Event | `/events/new` |
| View Events | `/events` |
| View Planets | `/planets` |
| Analysis | `/analysis` |
| House Analysis | `/house-analysis` |
| API - Events | `/api/events` |
| API - Planetary | `/api/planetary-data` |
| House Logic | `src/lib/houseMapping.ts` |
| Database | `src/lib/database.ts` |
| Types | `src/lib/types.ts` |

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Planetary data missing | Check Flask API running, verify date format |
| House mapping not created | Ensure event has category, run recalculation |
| Aspects not calculated | Verify planetary data exists, check house mapping |
| 405 Method Not Allowed | Endpoint accepts GET and POST |
| Database connection error | Check `.env.local` keys |

---

## ✅ Testing Checklist

- [ ] Create event → Check all tables populated
- [ ] View event detail → See house mapping and aspects
- [ ] Check `/house-analysis` → See table of all mappings
- [ ] Query Supabase → Verify data structure
- [ ] Recalculate correlations → All data updated

---

## 📚 Next Steps

1. Read `COMPLETE_SYSTEM_DOCUMENTATION.md` for full details
2. Review `CODE_STRUCTURE_GUIDE.md` for code organization
3. Check `QUERY_HOUSE_MAPPINGS.md` for SQL examples
4. Explore the codebase following the structure guide

---

**You're ready to go! 🎉**

