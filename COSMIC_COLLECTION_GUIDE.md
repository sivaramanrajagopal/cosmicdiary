# 📚 Cosmic Collection System - Complete Guide

**A Comprehensive Guide to Understanding and Implementing the Cosmic State Collection and Event Correlation System**

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Database Schema](#3-database-schema)
4. [Correlation Logic](#4-correlation-logic)
5. [Research Queries](#5-research-queries)
6. [Setup Instructions](#6-setup-instructions)
7. [Testing](#7-testing)
8. [Monitoring](#8-monitoring)
9. [Troubleshooting](#9-troubleshooting)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Overview

### What This System Does

The **Cosmic Collection System** is an automated astrological research system that:

1. **Captures Planetary State** - Every 2 hours, calculates and stores a complete snapshot of all planetary positions, aspects, and astrological configurations at a reference location (Delhi, India)

2. **Detects World Events** - Uses OpenAI to identify significant world events from the past 2-3 hours

3. **Calculates Event Charts** - For each detected event, calculates a complete astrological chart at the event's time and location

4. **Correlates Patterns** - Analyzes correlations between event charts and cosmic snapshots to identify matching planetary patterns

5. **Stores for Research** - All data is stored in a database for long-term pattern analysis and research

### Why Capture Cosmic State Every 2 Hours?

**Planetary positions change continuously**, but for research purposes, we need discrete snapshots:

- **Moon moves ~0.5° per hour** - Changes nakshatra every ~2 hours
- **Fast planets (Mercury, Venus) move 1-2° per day**
- **Lagna changes every ~2 hours** - Each 2-hour window has a different rising sign
- **Aspects change as planets move** - Planetary relationships evolve

**2-hour intervals provide:**
- ✅ Fine enough granularity to capture planetary movements
- ✅ Manageable data volume (12 snapshots per day)
- ✅ Enough overlap to catch events that span windows
- ✅ Research-grade temporal resolution

### How Correlation Works

**The core question**: "Do specific planetary configurations correlate with specific types of events?"

**Example Research Question:**
> "Do earthquakes occur more frequently when Mars is retrograde and in the 8th house (house of sudden events)?"

**The System Answers This By:**
1. Capturing the planetary state every 2 hours
2. Recording when earthquakes occur
3. Comparing the earthquake event charts with cosmic snapshots
4. Calculating correlation scores based on matching patterns
5. Storing results for statistical analysis

**Correlation = Matching Patterns**

When an event occurs, we compare:
- Event chart Lagna vs. Snapshot Lagna
- Retrograde planets in event vs. retrograde planets in snapshot
- Planetary house positions (e.g., Mars in 8th house)
- Active aspects (planetary relationships)
- Rasi (sign) positions

**Higher correlation = More matching patterns = Stronger astrological influence**

---

## 2. Architecture

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              GITHUB ACTIONS (Every 2 Hours)                     │
│                  Cron: '30 */2 * * *'                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   STEP 1: CAPTURE COSMIC STATE    │
        └────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ├─ Calculate Lagna (Delhi, India) │
        ├─ Get ALL 9 Planetary Positions  │
        ├─ Calculate Planetary Aspects    │
        ├─ Identify Active Houses         │
        ├─ Note Retrograde Planets        │
        └─ Store in cosmic_snapshots      │
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   STEP 2: DETECT EVENTS (OpenAI)  │
        └────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ├─ Scan News (Past 2-3 hours)    │
        ├─ Filter Astrological Relevance │
        ├─ Validate Event Quality        │
        ├─ Score Events (0-100)          │
        └─ Select Top 15 Events          │
                         │
                         ▼
        ┌────────────────────────────────────┐
        │  STEP 3: CALCULATE EVENT CHARTS   │
        └────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ├─ For Each Event:                │
        │  ├─ Calculate Lagna at          │
        │  │  Event Time/Location         │
        │  ├─ Get Planetary Positions     │
        │  ├─ Calculate Aspects           │
        │  └─ Store in event_chart_data   │
        └─────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   STEP 4: CORRELATION ANALYSIS    │
        └────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ├─ Compare Event Chart with       │
        │  Cosmic Snapshot                │
        ├─ Identify Matching Aspects      │
        ├─ Calculate Correlation Scores   │
        └─ Store in                      │
           event_cosmic_correlations      │
                         │
                         ▼
        ┌────────────────────────────────────┐
        │         DATABASE STORAGE           │
        └────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ├─ events (event details)         │
        ├─ cosmic_snapshots (every 2h)    │
        ├─ event_chart_data (per event)   │
        └─ event_cosmic_correlations      │
           (matching patterns)            │
```

### Component Files

| Component | File | Purpose |
|-----------|------|---------|
| Main Script | `collect_events_with_cosmic_state.py` | Orchestrates all 4 steps |
| Chart Calculations | `astro_calculations.py` | Calculates Lagna, planets, houses |
| Aspect Calculator | `aspect_calculator.py` | Calculates planetary aspects (Drishti) |
| Correlation Analyzer | `correlation_analyzer.py` | Compares charts and calculates scores |
| Workflow | `.github/workflows/event-collection.yml` | GitHub Actions automation |

---

## 3. Database Schema

### Table Relationships

```
events (1) ────────< (many) event_chart_data
   │
   │ (many)
   │
   ▼
event_cosmic_correlations (many) ────> (1) cosmic_snapshots
```

### Table: `cosmic_snapshots`

**Purpose**: Stores planetary state snapshots captured every 2 hours.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `snapshot_time` | TIMESTAMPTZ | Exact timestamp of snapshot |
| `reference_location` | TEXT | Location used (default: "Delhi, India") |
| `reference_latitude` | REAL | Latitude (default: 28.6139) |
| `reference_longitude` | REAL | Longitude (default: 77.2090) |
| `lagna_degree` | REAL | Ascendant degree (0-360°) |
| `lagna_rasi` | TEXT | Rising sign (e.g., "Scorpio") |
| `lagna_rasi_number` | INT | Rasi number (1-12) |
| `lagna_lord` | TEXT | Ruling planet of Lagna |
| `house_cusps` | JSONB | Array of 12 house cusp degrees |
| `planetary_positions` | JSONB | All 9 planets with positions, houses, rasis |
| `active_aspects` | JSONB | All planetary aspects at this moment |
| `retrograde_planets` | TEXT[] | Array of retrograde planet names |
| `moon_rasi` | TEXT | Moon's current sign |
| `moon_nakshatra` | TEXT | Moon's current nakshatra |
| `ayanamsa` | REAL | Ayanamsa value used (Lahiri) |

**Example `planetary_positions` JSONB:**

```json
{
  "Sun": {
    "longitude": 245.32,
    "latitude": 0.0,
    "speed": 0.9856,
    "is_retrograde": false,
    "rasi": {"name": "Sagittarius", "number": 9, "lord": "Jupiter"},
    "nakshatra": {"name": "Mula", "number": 19, "pada": 2},
    "house": 3
  },
  "Mars": {
    "longitude": 182.45,
    "is_retrograde": true,
    "house": 8,
    ...
  }
}
```

**Why This Table?**

- Provides temporal reference for planetary states
- Enables "What was happening in the cosmos when X event occurred?"
- Allows pattern analysis over time
- Research-grade data for statistical analysis

### Table: `event_cosmic_correlations`

**Purpose**: Links events with cosmic snapshots and stores correlation analysis.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `event_id` | BIGINT | Foreign key to `events` table |
| `snapshot_id` | BIGINT | Foreign key to `cosmic_snapshots` table |
| `correlation_score` | REAL | Overall score (0.0 - 1.0) |
| `matching_factors` | JSONB | Array of matching patterns found |
| `total_matches` | INT | Count of matching factors |

**Example `matching_factors` JSONB:**

```json
[
  {
    "type": "lagna_match",
    "description": "Both charts have Scorpio Lagna",
    "score": 0.3,
    "significance": "high"
  },
  {
    "type": "retrograde_match",
    "description": "Both charts have Mars and Jupiter retrograde",
    "score": 0.2,
    "significance": "medium"
  },
  {
    "type": "house_match",
    "description": "Mars in 8th house in both charts",
    "score": 0.05,
    "significance": "low"
  }
]
```

**Why This Table?**

- Stores correlation analysis results
- Enables querying: "Which events had high correlation scores?"
- Allows pattern matching: "Do disasters correlate with specific planetary positions?"
- Research foundation for statistical validation

### Table: `event_chart_data`

**Purpose**: Stores complete astrological chart for each event.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `event_id` | BIGINT | Foreign key to `events` (1:1 relationship) |
| `ascendant_degree` | REAL | Event's Lagna degree |
| `ascendant_rasi` | TEXT | Event's rising sign |
| `house_cusps` | JSONB | 12 house cusp degrees |
| `planetary_positions` | JSONB | All planets at event time/location |
| `planetary_strengths` | JSONB | Exaltation, debilitation, dig bala, etc. |

**Relationship:**

- **One event = One chart** (1:1 relationship)
- Chart is calculated based on event's time and location
- Used for correlation with cosmic snapshots

### Table: `events`

**Purpose**: Stores event details (existing table, enhanced for cosmic collection).

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `date` | DATE | Event date |
| `event_time` | TIME | Event time (HH:MM:SS) |
| `timezone` | TEXT | IANA timezone |
| `latitude` | REAL | Event location latitude |
| `longitude` | REAL | Event location longitude |
| `title` | TEXT | Event title |
| `category` | TEXT | Event category |
| `impact_level` | TEXT | low/medium/high/critical |

**Important**: Events must have `event_time`, `latitude`, and `longitude` for chart calculation.

---

## 4. Correlation Logic

### How Correlation Scores Are Calculated

The system compares an event chart with a cosmic snapshot and identifies matching patterns. Each pattern has a score, and scores are summed (capped at 1.0).

### Correlation Types and Scores

#### 1. Lagna Match (Score: 0.3)

**What**: Both charts have the same rising sign (Lagna).

**Example:**
- Event chart: Scorpio Lagna
- Snapshot: Scorpio Lagna
- **Match!** → +0.3 points

**Why Important**: Lagna is the most significant factor in Vedic astrology. Same Lagna = similar energy/time window.

**Code Logic:**
```python
if event_chart['ascendant_rasi'] == snapshot_chart['ascendant_rasi']:
    score += 0.3
```

#### 2. Retrograde Match (Score: 0.1 per planet)

**What**: Same planets are retrograde in both charts.

**Example:**
- Event chart: Mars, Jupiter retrograde
- Snapshot: Mars, Jupiter retrograde
- **2 matches!** → +0.2 points (0.1 × 2)

**Why Important**: Retrograde planets have intensified/reversed energy.

**Scoring:**
- Count retrograde planets in event chart
- Count how many match snapshot
- Score = 0.1 × number of matches
- Maximum possible: 0.9 (if all 9 planets match)

#### 3. House Position Match (Score: 0.05 per planet)

**What**: Same planets in same houses.

**Example:**
- Event: Mars in 8th house, Saturn in 12th house
- Snapshot: Mars in 8th house, Saturn in 12th house
- **2 matches!** → +0.1 points (0.05 × 2)

**Why Important**: House positions determine planetary influence areas.

**Scoring:**
- Compare house positions for each planet
- Score = 0.05 × number of matching house positions
- Maximum possible: 0.45 (if all 9 planets match)

#### 4. Aspect Match (Score: 0.15 per aspect)

**What**: Same planetary aspects active in both charts.

**Example:**
- Event: Jupiter aspects 7th house, Mars aspects 4th house
- Snapshot: Jupiter aspects 7th house, Mars aspects 4th house
- **2 matches!** → +0.3 points (0.15 × 2)

**Why Important**: Aspects show planetary relationships and influences.

**Scoring:**
- Compare active aspects in both charts
- Score = 0.15 × number of matching aspects
- Maximum possible: varies (depends on aspect count)

#### 5. Rasi Match (Score: 0.05 per planet)

**What**: Same planets in same zodiac signs.

**Example:**
- Event: Sun in Sagittarius, Moon in Cancer
- Snapshot: Sun in Sagittarius, Moon in Cancer
- **2 matches!** → +0.1 points (0.05 × 2)

**Why Important**: Sign placement determines planetary qualities.

**Scoring:**
- Compare rasi positions for each planet
- Score = 0.05 × number of matching rasi positions
- Maximum possible: 0.45 (if all 9 planets match)

### Total Score Calculation

**Formula:**
```
Total Score = Sum of all individual scores
Final Score = min(Total Score, 1.0)  // Capped at 1.0
```

**Example Calculation:**

```
Lagna Match:          0.30
Retrograde Match:     0.20 (2 planets)
House Position Match: 0.10 (2 planets)
Aspect Match:         0.30 (2 aspects)
Rasi Match:           0.10 (2 planets)
─────────────────────────────
Total:                1.00
Final Score:          1.00 (capped)
```

### Correlation Strength Categories

| Score Range | Category | Meaning |
|-------------|----------|---------|
| 0.7 - 1.0 | Very High | Strong correlation, significant match |
| 0.5 - 0.69 | High | Good correlation, notable match |
| 0.3 - 0.49 | Medium | Moderate correlation, some patterns match |
| 0.0 - 0.29 | Low | Weak correlation, few patterns match |

### Why These Scores?

**Score Distribution:**
- Lagna match (0.3) is weighted highest - most significant
- Aspects (0.15) are weighted high - show relationships
- Retrograde (0.1) shows intensity
- House/Rasi (0.05) show positions

**Design Rationale:**
- Ensures Lagna match alone provides "medium" correlation
- Multiple factors can reach "high" or "very high"
- Scores are additive but capped to prevent inflation
- Allows for statistical analysis and pattern recognition

---

## 5. Research Queries

### Basic Queries

#### Find All Events with High Correlation

```sql
-- Events with correlation score > 0.7
SELECT 
    e.id,
    e.title,
    e.date,
    e.category,
    cs.snapshot_time,
    ecc.correlation_score,
    ecc.total_matches
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE ecc.correlation_score >= 0.7
ORDER BY ecc.correlation_score DESC;
```

#### Find Events During Specific Lagna

```sql
-- All events that occurred during Scorpio Lagna
SELECT 
    e.title,
    e.date,
    e.category,
    cs.lagna_rasi,
    cs.snapshot_time,
    ecc.correlation_score
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE cs.lagna_rasi = 'Scorpio'
ORDER BY e.date DESC;
```

#### Count Events by Lagna

```sql
-- How many events occurred in each Lagna
SELECT 
    cs.lagna_rasi,
    COUNT(DISTINCT e.id) as event_count,
    AVG(ecc.correlation_score) as avg_correlation,
    MAX(ecc.correlation_score) as max_correlation
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
GROUP BY cs.lagna_rasi
ORDER BY event_count DESC;
```

### Advanced Queries

#### Find Events During Mars Retrograde in 8th House

```sql
-- Events correlated with snapshots where Mars is retrograde in 8th house
SELECT 
    e.title,
    e.date,
    e.category,
    ecc.correlation_score,
    cs.snapshot_time
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE 
    'Mars' = ANY(cs.retrograde_planets)
    AND (cs.planetary_positions->'Mars'->>'house')::int = 8
ORDER BY ecc.correlation_score DESC;
```

#### Analyze Disaster Frequency by Lagna

```sql
-- Natural disasters by Lagna
SELECT 
    cs.lagna_rasi,
    COUNT(*) as disaster_count,
    AVG(ecc.correlation_score) as avg_correlation
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE e.category = 'Natural Disaster'
GROUP BY cs.lagna_rasi
ORDER BY disaster_count DESC;
```

#### Find Planetary Patterns for High-Impact Events

```sql
-- Which planets are most common in high-impact event correlations?
SELECT 
    planet_name,
    COUNT(*) as event_count,
    AVG(correlation_score) as avg_score
FROM (
    SELECT 
        e.id,
        ecc.correlation_score,
        jsonb_array_elements_text(cs.retrograde_planets) as planet_name
    FROM events e
    JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
    JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
    WHERE e.impact_level IN ('high', 'critical')
        AND ecc.correlation_score >= 0.5
) subquery
GROUP BY planet_name
ORDER BY event_count DESC;
```

#### Compare Correlation Scores by Event Category

```sql
-- Average correlation by event category
SELECT 
    e.category,
    COUNT(DISTINCT e.id) as event_count,
    AVG(ecc.correlation_score) as avg_correlation,
    MAX(ecc.correlation_score) as max_correlation,
    MIN(ecc.correlation_score) as min_correlation
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
GROUP BY e.category
ORDER BY avg_correlation DESC;
```

#### Find Matching Factors for Specific Events

```sql
-- Detailed matching factors for a specific event
SELECT 
    e.title,
    ecc.correlation_score,
    ecc.total_matches,
    ecc.matching_factors
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
WHERE e.id = 123  -- Replace with actual event ID
ORDER BY ecc.correlation_score DESC;
```

#### Time-Based Analysis

```sql
-- Events and correlations by hour of day
SELECT 
    EXTRACT(HOUR FROM cs.snapshot_time) as hour_of_day,
    COUNT(DISTINCT e.id) as event_count,
    AVG(ecc.correlation_score) as avg_correlation
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
GROUP BY EXTRACT(HOUR FROM cs.snapshot_time)
ORDER BY hour_of_day;
```

---

## 6. Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL database (Supabase)
- OpenAI API key
- GitHub account (for Actions)
- Git installed

### Step 1: Apply Database Migrations

1. **Open Supabase Dashboard** → SQL Editor

2. **Run migrations in order:**
   ```sql
   -- Migration 002: Event chart data
   -- Run: database_migrations/002_create_event_chart_data_table.sql
   
   -- Migration 008: Cosmic snapshots
   -- Run: database_migrations/008_create_cosmic_snapshots.sql
   
   -- Migration 009: Event-cosmic correlations
   -- Run: database_migrations/009_create_event_cosmic_correlations.sql
   ```

3. **Verify tables created:**
   ```sql
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public' 
     AND table_name IN ('cosmic_snapshots', 'event_cosmic_correlations', 'event_chart_data');
   ```

### Step 2: Install Dependencies

```bash
cd /path/to/CosmicDiary/CosmicDiary

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install Python packages
pip install -r requirements.txt
```

**Required packages:**
- `pyswisseph==2.10.3.2` (Swiss Ephemeris)
- `supabase==2.0.0` (Database client)
- `openai==1.6.1` (Event detection)
- `pytz==2024.1` (Timezone handling)
- `timezonefinder==6.5.2` (Timezone detection)

### Step 3: Set Environment Variables

Create `.env.local` in `CosmicDiary/` directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# Flask API (if running locally)
FLASK_API_URL=http://localhost:8000
```

### Step 4: Test Locally

```bash
# Test cosmic snapshot calculation
python3 test_cosmic_collection.py

# Test full collection script
python3 collect_events_with_cosmic_state.py
```

**Expected output:**
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
```

### Step 5: Configure GitHub Actions

1. **Go to GitHub Repository** → Settings → Secrets and variables → Actions

2. **Add Secrets:**
   - `OPENAI_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `FLASK_API_URL` (optional, for backend API)

3. **Verify Workflow:**
   - Check `.github/workflows/event-collection.yml` exists
   - Schedule: `cron: '30 */2 * * *'` (every 2 hours)

4. **Test Workflow:**
   - Go to Actions tab
   - Click "Event Collection with Cosmic State"
   - Click "Run workflow" → "Run workflow"

### Step 6: Verify First Run

After first GitHub Actions run:

1. **Check Database:**
   ```sql
   -- Should have 1 snapshot
   SELECT COUNT(*) FROM cosmic_snapshots;
   
   -- Should have events (if detected)
   SELECT COUNT(*) FROM events;
   
   -- Should have correlations (if events have charts)
   SELECT COUNT(*) FROM event_cosmic_correlations;
   ```

2. **Check Workflow Logs:**
   - Go to Actions → Latest run → View logs
   - Verify all 4 steps completed
   - Check for errors

---

## 7. Testing

### Automated Tests

**Run test suite:**
```bash
python3 test_cosmic_collection.py
```

**Tests included:**
- ✅ Cosmic snapshot calculation
- ✅ Event chart calculation
- ✅ Aspect calculation
- ✅ Correlation analysis
- ✅ Retrograde identification

### Manual Testing

#### Test 1: Cosmic Snapshot

```bash
python3 -c "
from collect_events_with_cosmic_state import capture_cosmic_snapshot
snapshot_id, chart = capture_cosmic_snapshot()
print(f'Snapshot ID: {snapshot_id}')
print(f'Lagna: {chart[\"ascendant_rasi\"]}')
"
```

#### Test 2: Event Detection

```bash
python3 -c "
from collect_events_with_cosmic_state import detect_events_openai
events = detect_events_openai()
print(f'Events detected: {len(events)}')
"
```

#### Test 3: Full Workflow

```bash
python3 collect_events_with_cosmic_state.py
```

**Verify output:**
- ✅ Snapshot captured
- ✅ Events detected (10-15)
- ✅ Event charts calculated
- ✅ Correlations created

### Database Verification

#### Check Snapshot Quality

```sql
-- Verify snapshot has all required data
SELECT 
    id,
    snapshot_time,
    lagna_rasi,
    lagna_rasi_number,
    array_length(retrograde_planets, 1) as retrograde_count,
    jsonb_array_length(house_cusps) as house_count
FROM cosmic_snapshots
ORDER BY snapshot_time DESC
LIMIT 5;
```

#### Check Correlation Quality

```sql
-- Verify correlations have scores
SELECT 
    correlation_score,
    total_matches,
    COUNT(*) as count
FROM event_cosmic_correlations
GROUP BY correlation_score, total_matches
ORDER BY correlation_score DESC;
```

---

## 8. Monitoring

### What to Monitor

#### 1. GitHub Actions Run Status

**Check:**
- Actions tab → Latest runs
- Ensure runs complete successfully
- Runs should occur every 2 hours

**Alert if:**
- ❌ Workflow fails
- ❌ Runs are delayed
- ❌ No runs in 4+ hours

#### 2. Database Growth

**Expected growth:**
- **Snapshots**: 12 per day (every 2 hours)
- **Events**: 120-180 per day (10-15 per run)
- **Correlations**: ~120-180 per day (one per event)

**Monitor:**
```sql
-- Snapshot count (should be ~12 per day)
SELECT 
    DATE(snapshot_time) as date,
    COUNT(*) as snapshot_count
FROM cosmic_snapshots
GROUP BY DATE(snapshot_time)
ORDER BY date DESC
LIMIT 7;

-- Storage size
SELECT 
    pg_size_pretty(pg_total_relation_size('cosmic_snapshots')) as snapshot_size,
    pg_size_pretty(pg_total_relation_size('event_cosmic_correlations')) as correlation_size;
```

#### 3. Correlation Scores

**Expected range:**
- Average: 0.3 - 0.5 (medium correlation)
- High scores (>0.7): Should be 5-10% of correlations
- Low scores (<0.3): Should be 20-30% of correlations

**Monitor:**
```sql
-- Correlation score distribution
SELECT 
    CASE 
        WHEN correlation_score >= 0.7 THEN 'Very High'
        WHEN correlation_score >= 0.5 THEN 'High'
        WHEN correlation_score >= 0.3 THEN 'Medium'
        ELSE 'Low'
    END as strength,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM event_cosmic_correlations
GROUP BY strength
ORDER BY strength DESC;
```

#### 4. Event Count Per Run

**Expected:**
- 10-15 events per run
- 120-180 events per day

**Monitor:**
```sql
-- Events per day
SELECT 
    DATE(created_at) as date,
    COUNT(*) as event_count
FROM events
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Health Check Dashboard Query

```sql
-- Overall system health
SELECT 
    'Snapshots (Last 24h)' as metric,
    COUNT(*)::text as value
FROM cosmic_snapshots
WHERE snapshot_time >= NOW() - INTERVAL '24 hours'

UNION ALL

SELECT 
    'Events (Last 24h)' as metric,
    COUNT(*)::text as value
FROM events
WHERE created_at >= NOW() - INTERVAL '24 hours'

UNION ALL

SELECT 
    'Avg Correlation Score' as metric,
    ROUND(AVG(correlation_score)::numeric, 3)::text as value
FROM event_cosmic_correlations

UNION ALL

SELECT 
    'High Correlations (>0.7)' as metric,
    COUNT(*)::text as value
FROM event_cosmic_correlations
WHERE correlation_score >= 0.7;
```

---

## 9. Troubleshooting

### Common Issues and Solutions

#### Issue 1: Swiss Ephemeris Data Files Missing

**Symptoms:**
```
Error: Swiss Ephemeris data files not found
```

**Solution:**
```bash
# pyswisseph should auto-download, but if not:
# Check if ephemeris files exist
python3 -c "import swisseph as swe; print(swe.version)"
# Should print version without errors

# If error, reinstall:
pip uninstall pyswisseph
pip install pyswisseph==2.10.3.2
```

#### Issue 2: OpenAI API Rate Limits

**Symptoms:**
```
Error: Rate limit exceeded
Events detected: 0
```

**Solution:**
- Check OpenAI usage dashboard
- Wait for rate limit reset
- Consider upgrading OpenAI plan
- Reduce `max_tokens` in API call

#### Issue 3: Database Connection Timeout

**Symptoms:**
```
Error: Connection timeout
Failed to insert cosmic snapshot
```

**Solution:**
- Check Supabase project is active
- Verify `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
- Check network connectivity
- Increase timeout in connection string

#### Issue 4: Correlation Score Always 0

**Symptoms:**
- All correlations have score 0.0
- `total_matches` is always 0

**Possible Causes:**
1. **Event charts not calculated:**
   ```sql
   -- Check if events have charts
   SELECT COUNT(*) FROM event_chart_data;
   -- Should match event count
   ```

2. **Missing event time/location:**
   ```sql
   -- Find events without time/location
   SELECT id, title, event_time, latitude, longitude
   FROM events
   WHERE event_time IS NULL 
      OR latitude IS NULL 
      OR longitude IS NULL;
   ```

3. **Chart calculation failed:**
   - Check logs for chart calculation errors
   - Verify `astro_calculations.py` is working
   - Test chart calculation manually

**Solution:**
```bash
# Test chart calculation
python3 -c "
from astro_calculations import calculate_complete_chart
from datetime import date, time

chart = calculate_complete_chart(
    event_date=date(2025, 12, 12),
    event_time=time(10, 30, 0),
    latitude=28.6139,
    longitude=77.2090,
    timezone_str='Asia/Kolkata'
)
print('Chart calculated:', 'ascendant_rasi' in chart)
"
```

#### Issue 5: No Events Detected

**Symptoms:**
```
Events detected: 0
STEP 2: No events found
```

**Possible Causes:**
- OpenAI API key invalid
- No significant events in time window
- OpenAI API error

**Solution:**
- Verify `OPENAI_API_KEY` is set correctly
- Check OpenAI API status
- Test OpenAI connection:
  ```bash
  python3 -c "
  from openai import OpenAI
  client = OpenAI(api_key='your-key')
  print('API key valid')
  "
  ```

#### Issue 6: GitHub Actions Fails

**Symptoms:**
- Workflow shows red ❌
- Error in logs

**Common Causes:**
1. **Missing secrets:**
   - Check all required secrets are set
   - Verify secret names match workflow

2. **Import errors:**
   - Ensure all Python files are in repository
   - Check `collect_events_with_cosmic_state.py` imports

3. **Dependency issues:**
   - Verify `requirements.txt` includes all packages
   - Check Python version (3.10+)

**Solution:**
- Review workflow logs for specific error
- Test script locally first
- Check secrets are set correctly

---

## 10. Future Enhancements

### Planned Features

#### 1. Multiple Reference Locations

**Current**: Single reference location (Delhi, India)

**Enhancement**: Support multiple reference locations
- New York, USA
- London, UK
- Tokyo, Japan
- Mumbai, India

**Implementation:**
- Add `reference_location` field to snapshot selection
- Run collection for each location
- Compare correlations across locations

#### 2. Dasha Period Tracking

**Enhancement**: Track planetary periods (Dasha)
- Calculate current Dasha for each snapshot
- Correlate events with active Dasha periods
- Analyze Dasha-event relationships

**Tables needed:**
- `dasha_periods` - Store Dasha calculations
- `event_dasha_correlations` - Link events to Dasha

#### 3. Transit Analysis

**Enhancement**: Track planetary transits
- Identify major transits (Saturn return, Jupiter transit, etc.)
- Correlate events with transit periods
- Predict potential event windows

**Features:**
- Transit alerts
- Transit-event correlation analysis
- Historical transit patterns

#### 4. Pattern Recognition with ML

**Enhancement**: Machine learning pattern recognition
- Train models on correlation patterns
- Identify hidden patterns
- Predict event likelihood based on planetary state

**Techniques:**
- Time series analysis
- Classification models
- Clustering analysis

#### 5. Predictive Capabilities

**Enhancement**: Event prediction system
- Based on historical correlations
- Alert when similar planetary patterns emerge
- Risk assessment for event types

**Features:**
- Prediction dashboard
- Alert system
- Confidence scoring

### Research Opportunities

1. **Temporal Patterns**: Do events cluster in specific time windows?
2. **Geographic Patterns**: Do correlations vary by location?
3. **Planetary Cycles**: Long-term pattern analysis (Jupiter 12-year cycle, etc.)
4. **Event Type Analysis**: Which planets correlate with which event categories?
5. **Retrograde Impact**: Do retrograde periods show different patterns?

### Data Export and Analysis

**Future Tools:**
- Export correlations to CSV/Excel
- Statistical analysis dashboard
- Visualization tools (charts, graphs)
- Research API endpoints

---

## Appendix: Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `collect_events_with_cosmic_state.py` | Main collection script |
| `astro_calculations.py` | Chart calculations |
| `aspect_calculator.py` | Aspect calculations |
| `correlation_analyzer.py` | Correlation analysis |
| `test_cosmic_collection.py` | Test suite |

### Key Database Tables

| Table | Purpose |
|-------|---------|
| `cosmic_snapshots` | Planetary state every 2 hours |
| `event_cosmic_correlations` | Correlation results |
| `event_chart_data` | Event astrological charts |
| `events` | Event details |

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `SUPABASE_URL` | ✅ Yes | Database connection |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ Yes | Database authentication |
| `OPENAI_API_KEY` | ✅ Yes | Event detection |
| `FLASK_API_URL` | ⚠️ Optional | Backend API URL |

### Correlation Score Reference

| Score | Category | Meaning |
|-------|----------|---------|
| 0.7-1.0 | Very High | Strong match |
| 0.5-0.69 | High | Good match |
| 0.3-0.49 | Medium | Moderate match |
| 0.0-0.29 | Low | Weak match |

---

## Conclusion

This guide provides a complete understanding of the Cosmic Collection System. The system captures planetary states every 2 hours, detects events, calculates charts, and correlates patterns for astrological research.

**Key Takeaways:**
- ✅ System runs automatically via GitHub Actions
- ✅ Captures complete planetary state every 2 hours
- ✅ Correlates events with cosmic snapshots
- ✅ Stores data for long-term research
- ✅ Provides foundation for pattern analysis

**Next Steps:**
1. Set up the system following Setup Instructions
2. Monitor initial runs for data quality
3. Explore Research Queries to analyze patterns
4. Contribute findings and improvements

---

**Last Updated**: 2025-12-12  
**Version**: 1.0  
**Author**: Cosmic Diary System

