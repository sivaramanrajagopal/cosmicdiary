# 🔍 On-Demand Job Explanation

## ❓ What the On-Demand Job Does

### ✅ **Updates: `planetary_data` Table ONLY**

The `run_planetary_job_with_notification.py` script:
1. ✅ Calculates planetary positions for a specific date
2. ✅ Stores/updates data in the `planetary_data` table
3. ✅ Sends email notification

### ❌ **Does NOT Update: Events**

The job does **NOT**:
- ❌ Create new events
- ❌ Update existing events
- ❌ Modify the `events` table in any way

---

## 📊 What Was Actually Stored

When you ran the on-demand job, it updated:

### `planetary_data` Table
- **Table**: `planetary_data`
- **What**: Planetary positions (Sun, Moon, planets, etc.) for the date
- **Structure**: JSONB containing all 9 planets with their positions, Rasi, Nakshatra

**Example Record:**
```json
{
  "date": "2025-12-11",
  "planetary_data": {
    "planets": [
      {"name": "Sun", "longitude": 233.11, "rasi": {...}, ...},
      {"name": "Moon", "longitude": 121.4, "rasi": {...}, ...},
      ... 9 planets total
    ]
  }
}
```

---

## 🆚 Planetary Data vs Events

### Planetary Data (`planetary_data` table)
- **What**: Astronomical positions of planets
- **When**: Calculated for every date
- **Purpose**: Used for astrological analysis
- **Updated by**: `daily_planetary_job.py`

### Events (`events` table)
- **What**: Real-world events (disasters, news, etc.)
- **When**: Created manually or via automation
- **Purpose**: Event records to correlate with planetary data
- **Created by**: 
  - Manual entry through UI (`/events/new`)
  - Automated collection (`import_automated_events.py`)

---

## 🔄 Complete Data Flow

```
1. Planetary Data Calculation
   └─ daily_planetary_job.py
      └─ Stores in: planetary_data table
      
2. Event Creation
   └─ Manual: /events/new page
   └─ Automated: import_automated_events.py
      └─ Stores in: events table
      
3. Analysis (Automatic)
   └─ When event is created:
      ├─ Maps event to house (event_house_mappings)
      ├─ Calculates aspects (event_planetary_aspects)
      └─ Correlates with planets (event_planetary_correlations)
```

---

## 💡 What You Need

### To Create/Update Events:

**Option 1: Manual Entry**
```bash
# Visit the web UI
http://localhost:3002/events/new
```

**Option 2: Automated Collection**
```bash
# Run the automated event collection script
python3 import_automated_events.py
```

**Option 3: API Endpoint**
```bash
# Create event via API
curl -X POST http://localhost:3002/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-11",
    "title": "Test Event",
    "category": "Natural Disaster",
    "impact_level": "high",
    "event_type": "world"
  }'
```

---

## ✅ Summary

| Aspect | On-Demand Job | Events |
|--------|---------------|--------|
| **Table Updated** | `planetary_data` | `events` |
| **What It Stores** | Planet positions | Event records |
| **When to Use** | Calculate planetary data for a date | Record world/personal events |
| **Automatic Analysis** | No | Yes (house mapping, aspects, correlations) |

---

## 🎯 Next Steps

If you want to:

1. **Check what was stored**: Run `python3 check_db_status.py`
2. **Create an event**: Visit `/events/new` or use API
3. **Run automated event collection**: `python3 import_automated_events.py`
4. **Create on-demand event job**: I can create a script for this if needed

---

**The on-demand job successfully updated planetary data, but events must be created separately!** 📊✨

