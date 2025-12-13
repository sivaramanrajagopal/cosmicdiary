# How the Event Collection System Works - Simple Explanation

## 🎯 Overview

Every 2 hours, the system automatically:
1. **Snapshots the current cosmic state** (planetary positions)
2. **Detects significant world events** using AI
3. **Calculates astrological charts** for each event
4. **Correlates events with cosmic state** to find patterns
5. **Stores everything** in the database

---

## ⏰ Scheduler: When It Runs

### GitHub Actions (Automated)
- **Schedule**: Runs every 2 hours automatically
- **Location**: `.github/workflows/event-collection.yml`
- **What it does**: Triggers the collection script on GitHub's servers

### On-Demand (Manual)
- **Where**: `/jobs` page in the web app
- **Button**: "Run Event Collection Job"
- **Use case**: Test or trigger manually when needed

---

## 📸 Step 1: Capture Cosmic Snapshot

**What happens:**
- System takes a "photo" of current planetary positions
- Uses Delhi, India as the reference location (28.6139°N, 77.2090°E)
- Calculates:
  - **Lagna** (Ascendant) - Which sign is rising
  - **Planetary positions** - Where all 9 planets are (Sun, Moon, Mars, etc.)
  - **Active aspects** - Which planets are influencing each other
  - **Retrograde planets** - Which planets appear to be moving backward
  - **Dominant planets** - Which planets are strongest right now

**Stored in**: `cosmic_snapshots` table

**Example:**
```
Snapshot Time: 2025-12-13 02:47:11 UTC
Lagna: Scorpio (226.16°)
Retrograde Planets: Rahu, Ketu
Active Aspects: 19 aspects detected
```

---

## 🔍 Step 2: Detect Events Using AI (OpenAI)

**What happens:**
- AI scans news from the **past 8 hours**
- Filters for events that are:
  - **Significant** (not minor/local news)
  - **Astrologically relevant** (matches planetary/house significations)
  - **Research-worthy** (important enough to study)
  - **Geographically relevant** (India, G20 countries, global events)

**Prompt System** (`prompts/event_detection_prompt.py`):
- Uses detailed astrological knowledge
- Checks event categories against house/planet significations
- Validates quality (description length, impact level, etc.)
- Scores events (1-100) based on research value

**Event Categories Accepted:**
- Natural Disasters (earthquakes, floods, cyclones)
- Economic Events (market crashes, inflation, trade deals)
- Political Events (elections, policy changes, government shifts)
- Health & Medical (outbreaks, medical breakthroughs)
- Wars & Conflicts
- Technology & Innovation
- Business & Commerce
- Employment & Labor
- And more...

**Conditions for Selection:**
1. ✅ Event has clear time and location
2. ✅ Event matches astrological categories
3. ✅ Event has sufficient impact (medium/high/critical)
4. ✅ Event description is detailed enough (50-800 characters)
5. ✅ Event score is above threshold

**Stored in**: `events` table (temporarily, before processing)

---

## 🧮 Step 3: Calculate Event Charts

**What happens for EACH event:**
1. **Get coordinates** (if missing, geocode the location name)
   - Example: "Himachal Pradesh, India" → (31.1048°N, 77.1734°E)

2. **Calculate astrological chart** at event time + location:
   - **Ascendant (Lagna)** - Which sign was rising when/where event happened
   - **House cusps** - 12 houses based on location
   - **Planetary positions** - Where each planet was
   - **Planetary strengths** - Exaltation, debilitation, own sign, etc.
   - **Nakshatras** - Lunar mansions for each planet

3. **Store chart data** in `event_chart_data` table

**Conditions for Chart Calculation:**
- ✅ Event has a **time** (HH:MM:SS)
- ✅ Event has **coordinates** (latitude + longitude)
- ✅ Chart calculation succeeds (no errors)

---

## 🔗 Step 4: Correlate Events with Cosmic Snapshot

**What happens:**
For each event, compare its chart with the cosmic snapshot:

### Correlation Checks:

1. **Lagna Match** (20 points)
   - Does event's ascendant match snapshot's ascendant?
   - Example: Both are Scorpio → Strong correlation

2. **Retrograde Match** (15 points each)
   - Do the same planets appear retrograde in both?
   - Example: Rahu retrograde in both → Correlation

3. **House Position Match** (10 points each)
   - Are planets in similar houses?
   - Example: Jupiter in 2nd house in both → Correlation

4. **Aspect Match** (10 points each)
   - Do planets aspect the same houses?
   - Example: Saturn aspects 7th house in both → Correlation

5. **Rasi Match** (5 points each)
   - Are planets in the same zodiac signs?
   - Example: Moon in Cancer in both → Correlation

**Correlation Score:**
- Sum of all matching factors
- Categorized as: Strong (>40), Moderate (20-40), Weak (<20)

**Stored in**: `event_cosmic_correlations` table

---

## 💾 Step 5: Store Everything

**Database Tables Used:**
1. **`cosmic_snapshots`** - Cosmic state at time of collection
2. **`events`** - Event details (title, description, category, location, etc.)
3. **`event_chart_data`** - Complete astrological chart for each event
4. **`event_cosmic_correlations`** - Correlation scores and matching factors

---

## 📊 Example Flow

```
Time: 2025-12-13 02:47 UTC

1. CAPTURE SNAPSHOT
   → Lagna: Scorpio, Retrograde: Rahu/Ketu, 19 aspects active

2. DETECT EVENTS (OpenAI)
   → Found 5 events:
      - Earthquake in Himachal Pradesh (Natural Disaster)
      - Stock market crash (Economic)
      - Government change in Maharashtra (Political)
      - Climate summit in Delhi (Political)
      - COVID outbreak (Health)

3. CALCULATE CHARTS
   → Geocode locations
   → Calculate ascendant for each event
   → Get planetary positions for each event
   → Store charts

4. CORRELATE
   → Compare each event chart with snapshot
   → Find matches (Lagna, retrograde, aspects, etc.)
   → Calculate scores (e.g., 35/100 = Moderate)
   → Store correlations

5. SUMMARY
   → Events Detected: 5
   → Events Stored: 5
   → Correlations Created: 5
   → Average Correlation Score: 28.5
```

---

## 🔧 Configuration

### Reference Location (for snapshot)
```python
Delhi, India
Latitude: 28.6139°N
Longitude: 77.2090°E
Timezone: Asia/Kolkata
```

### Time Window (for event detection)
- **Lookback**: Past 8 hours from current time
- **Timezone**: UTC

### Selection Criteria
- **Maximum events**: Top 15 (sorted by research score)
- **Minimum impact**: Medium or higher
- **Geographic priority**: India, then G20 countries, then global

---

## 🎯 Why This Works

1. **Captures Current State**: Snapshot shows "what the cosmos looks like right now"
2. **Finds Relevant Events**: AI filters for events that matter astrologically
3. **Calculates Event Charts**: Shows "what the cosmos looked like when event happened"
4. **Finds Patterns**: Correlation reveals if cosmic state influenced events
5. **Stores for Analysis**: All data saved for research and pattern discovery

---

## 🔍 What to Look For

High correlation events suggest:
- **Cosmic influence** on world events
- **Patterns** in planetary positions and significant happenings
- **Astrological timing** of important events
- **Research insights** for Vedic astrology studies

---

## ⚙️ Technical Details

- **Language**: Python 3.10+
- **Astrological Library**: Swiss Ephemeris (pyswisseph)
- **AI**: OpenAI GPT-4o-mini
- **Geocoding**: Geopy (Nominatim)
- **Database**: Supabase (PostgreSQL)
- **Scheduler**: GitHub Actions (cron: `0 */2 * * *` - every 2 hours)

