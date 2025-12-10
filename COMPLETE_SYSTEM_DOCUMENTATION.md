# 🌙 Cosmic Diary - Complete System Documentation

**Version:** 1.0  
**Last Updated:** December 2025  
**Astrological Research Platform for Event-Planetary Correlation Analysis**

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Requirements & Goals](#requirements--goals)
3. [System Architecture](#system-architecture)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Code Structure](#code-structure)
7. [Environment Configuration](#environment-configuration)
8. [Installation & Setup](#installation--setup)
9. [Features & Outcomes](#features--outcomes)
10. [Usage Guide](#usage-guide)

---

## 📊 Executive Summary

**Cosmic Diary** is a full-stack astrological research application that correlates world events with planetary positions using Swiss Ephemeris calculations. The system follows traditional Vedic astrology principles (Parasara method) to map events to astrological houses (Bhavas) and calculate planetary aspects (Drishti).

### Key Achievements:
- ✅ Event recording and management system
- ✅ Daily planetary data calculation using Swiss Ephemeris
- ✅ Automatic house mapping (Kalapurushan method)
- ✅ Planetary aspect calculation (Drishti system)
- ✅ Astrological correlation analysis
- ✅ Automated data collection via cron jobs
- ✅ Email reporting system
- ✅ Comprehensive analysis dashboard

---

## 🎯 Requirements & Goals

### Primary Requirements

1. **Event Recording**
   - Record world and personal events with metadata
   - Store event details: date, category, location, impact level
   - Support geolocation (latitude/longitude) for future ascendant calculations

2. **Planetary Calculations**
   - Calculate accurate planetary positions using Swiss Ephemeris
   - Use Lahiri Ayanamsa for sidereal calculations
   - Support all 9 planets: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu, Ketu
   - Calculate Rasi, Nakshatra, Retrograde status

3. **House Mapping (Kalapurushan)**
   - Map events to houses (1-12) based on traditional significations
   - Aries = House 1, Taurus = House 2, ... Pisces = House 12
   - Use event category and significations for mapping

4. **Planetary Aspects (Drishti)**
   - Calculate which planets aspect event houses
   - **Jupiter**: Aspects 5th, 7th, 9th houses
   - **Saturn**: Aspects 3rd, 7th, 10th houses
   - **Mars**: Aspects 4th, 7th, 8th houses
   - **Rahu/Ketu**: Aspects 3rd, 7th, 11th houses + dustana (6, 8, 12)
   - **Sun/Moon/Mercury/Venus**: Aspect 7th house only

5. **Data Storage & Analysis**
   - Store all calculations in database
   - Enable pattern analysis and correlations
   - Support historical data queries

6. **Automation**
   - Daily planetary data calculation (via cron)
   - Automated event collection (optional)
   - Email reports (optional)

---

## 🏗️ System Architecture

### Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 15)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Home   │  │  Events  │  │ Planets  │  │ Analysis │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         House Analysis Page (New)                    │    │
│  │  - House Mappings Table                              │    │
│  │  - Planetary Aspects Display                         │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              API LAYER (Next.js API Routes)                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │ /api/events          - CRUD operations              │     │
│  │ /api/planetary-data  - Fetch planetary positions    │     │
│  │ /api/events/recalculate-correlations - Recalculate  │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────────┐         ┌──────────────────┐
│  SUPABASE DB     │         │  FLASK API       │
│  (PostgreSQL)    │         │  (Swiss Ephem)   │
│                  │         │                  │
│  - Events        │         │  - Calculate     │
│  - Planetary Data│         │    positions     │
│  - Correlations  │         │  - Swiss Ephem   │
│  - House Maps    │         │    integration   │
│  - Aspects       │         │                  │
└──────────────────┘         └──────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│              AUTOMATION LAYER (Python Scripts)               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ daily_planetary_job.py   - Daily calculations      │     │
│  │ import_automated_events.py - Event collection      │     │
│  │ email_reports.py          - Email summaries        │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │           CRON JOBS (Scheduled Tasks)               │     │
│  │  - Daily at midnight: Planetary data                │     │
│  │  - Twice daily: Event collection                    │     │
│  │  - Daily/Weekly: Email reports                      │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- Next.js 15 (App Router)
- React Server Components
- TypeScript 5
- Tailwind CSS 3.4

**Backend:**
- Next.js API Routes (Serverless functions)
- Flask (Python) for Swiss Ephemeris calculations
- Python 3.9+ for automation scripts

**Database:**
- Supabase (PostgreSQL)
- JSONB for flexible planetary data storage
- Row Level Security (RLS) enabled

**Libraries:**
- `@supabase/supabase-js` - Database client
- `pyswisseph` - Swiss Ephemeris Python bindings
- `python-dotenv` - Environment management
- `date-fns` - Date formatting

---

## 🗄️ Database Schema

### Tables Overview

#### 1. `events`
Stores all recorded events (world and personal).

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    location TEXT,
    latitude REAL,
    longitude REAL,
    impact_level TEXT CHECK(impact_level IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
    event_type TEXT CHECK(event_type IN ('world', 'personal')) DEFAULT 'world',
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Key Fields:**
- `id`: Auto-incrementing primary key
- `date`: Event date
- `category`: Event category (e.g., "Natural Disaster", "Economic Event")
- `impact_level`: Event severity
- `tags`: Array of tags (JSONB)

**Indexes:**
- `idx_events_date` - Fast date queries
- `idx_events_category` - Category filtering
- `idx_events_type` - Type filtering
- `idx_events_impact` - Impact level queries

---

#### 2. `planetary_data`
Stores daily planetary positions calculated from Swiss Ephemeris.

```sql
CREATE TABLE planetary_data (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    planetary_data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**JSONB Structure:**
```json
{
  "planets": [
    {
      "name": "Sun",
      "longitude": 232.43,
      "latitude": 0,
      "is_retrograde": false,
      "nakshatra": 18,
      "rasi": {
        "name": "Scorpio",
        "number": 8,
        "lord": {
          "name": "Mars"
        }
      }
    },
    ... 8 more planets
  ]
}
```

**Indexes:**
- `idx_planetary_data_date` - Fast date lookups
- `idx_planetary_data_gin` - GIN index for JSONB queries

---

#### 3. `event_planetary_correlations`
Stores planetary correlations with events (based on category, retrograde, etc.).

```sql
CREATE TABLE event_planetary_correlations (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    planet_name TEXT NOT NULL,
    planet_position JSONB,
    correlation_score REAL NOT NULL CHECK(correlation_score >= 0 AND correlation_score <= 1),
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, planet_name)
);
```

**Key Fields:**
- `correlation_score`: 0.0 to 1.0 (relevance score)
- `reason`: Explanation for correlation
- `planet_position`: Full planet data (JSONB)

**Indexes:**
- `idx_correlations_event` - Event lookups
- `idx_correlations_date` - Date filtering
- `idx_correlations_planet` - Planet filtering
- `idx_correlations_score` - Score-based sorting

---

#### 4. `event_house_mappings` ⭐ NEW
Maps events to astrological houses (Kalapurushan method).

```sql
CREATE TABLE event_house_mappings (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    house_number INT NOT NULL CHECK (house_number BETWEEN 1 AND 12),
    rasi_name TEXT NOT NULL,
    house_significations TEXT[] DEFAULT '{}',
    mapping_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id)
);
```

**Key Fields:**
- `house_number`: 1-12 (Aries to Pisces)
- `rasi_name`: Rasi name (e.g., "Scorpio", "Aries")
- `house_significations`: Array of matching significations
- `mapping_reason`: Why this house was selected

**Indexes:**
- `idx_house_mappings_event` - Event lookups
- `idx_house_mappings_house` - House filtering
- `idx_house_mappings_rasi` - Rasi filtering

---

#### 5. `event_planetary_aspects` ⭐ NEW
Stores planetary aspects to event houses (Drishti system).

```sql
CREATE TABLE event_planetary_aspects (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    house_number INT NOT NULL CHECK (house_number BETWEEN 1 AND 12),
    planet_name TEXT NOT NULL,
    aspect_type TEXT NOT NULL CHECK (aspect_type IN (
        'conjunction', 'drishti_3rd', 'drishti_4th', 'drishti_5th', 
        'drishti_7th', 'drishti_8th', 'drishti_9th', 'drishti_10th', 
        'drishti_11th', 'dustana'
    )),
    planet_longitude REAL NOT NULL,
    planet_rasi TEXT NOT NULL,
    aspect_strength TEXT CHECK (aspect_strength IN ('strong', 'moderate', 'weak')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, house_number, planet_name, aspect_type)
);
```

**Key Fields:**
- `aspect_type`: Type of aspect (conjunction, drishti_Xth, dustana)
- `aspect_strength`: Aspect strength (strong, moderate, weak)
- `planet_rasi`: Rasi where planet is positioned

**Indexes:**
- `idx_aspects_event` - Event lookups
- `idx_aspects_house` - House filtering
- `idx_aspects_planet` - Planet filtering
- `idx_aspects_type` - Aspect type filtering

---

### Relationships

```
events (1) ──→ (many) event_planetary_correlations
events (1) ──→ (1) event_house_mappings
events (1) ──→ (many) event_planetary_aspects
planetary_data (independent by date)
```

---

## 🔌 API Endpoints

### Frontend API Routes (Next.js)

#### 1. Events API

**GET `/api/events`**
- Fetch all events
- Query params: `?date=2025-12-10` (optional filter)
- Returns: Array of Event objects

**POST `/api/events`**
- Create new event
- Body: Event data (date, title, category, etc.)
- Auto-calculates: Correlations, house mappings, aspects
- Returns: Created event

**GET `/api/events/[id]`**
- Fetch single event by ID
- Returns: Event object

**POST `/api/events/import`**
- Bulk import events
- Body: Array of event objects or single object
- Returns: Import summary

**GET/POST `/api/events/recalculate-correlations`**
- Recalculate correlations, house mappings, aspects for all events
- Runs in background
- Returns: Status message

---

#### 2. Planetary Data API

**GET `/api/planetary-data?date=2025-12-10`**
- Fetch planetary positions for a date
- Checks database first
- Falls back to Flask API if not found
- Auto-stores calculated data
- Returns: PlanetaryData object

---

### Flask API (Python)

**GET `/health`**
- Health check endpoint
- Returns: Service status, Swiss Ephemeris version

**GET `/api/planets/daily?date=2025-12-10`**
- Calculate planetary positions for a date
- Uses Swiss Ephemeris (Lahiri Ayanamsa)
- Returns: Complete planetary data for all 9 planets

**Structure:**
```json
{
  "date": "2025-12-10",
  "planetary_data": {
    "planets": [
      {
        "name": "Sun",
        "longitude": 233.11,
        "latitude": 0,
        "is_retrograde": false,
        "nakshatra": 18,
        "rasi": {
          "name": "Scorpio",
          "number": 8,
          "lord": {"name": "Mars"}
        }
      },
      ... 8 more planets
    ]
  }
}
```

---

## 📁 Code Structure

```
CosmicDiary/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── page.tsx                  # Home page
│   │   ├── layout.tsx                # Root layout
│   │   ├── globals.css               # Global styles
│   │   ├── events/
│   │   │   ├── page.tsx              # Events list
│   │   │   ├── new/
│   │   │   │   └── page.tsx          # Create event form
│   │   │   └── [id]/
│   │   │       └── page.tsx          # Event detail (with house/aspects)
│   │   ├── planets/
│   │   │   └── page.tsx              # Planetary positions viewer
│   │   ├── analysis/
│   │   │   └── page.tsx              # Astrological analysis
│   │   ├── house-analysis/           # ⭐ NEW
│   │   │   └── page.tsx              # House mappings & aspects table
│   │   └── api/
│   │       ├── events/
│   │       │   ├── route.ts          # GET/POST /api/events
│   │       │   ├── [id]/
│   │       │   │   └── route.ts      # GET /api/events/[id]
│   │       │   ├── import/
│   │       │   │   └── route.ts      # POST /api/events/import
│   │       │   └── recalculate-correlations/
│   │       │       └── route.ts      # GET/POST recalculation
│   │       └── planetary-data/
│   │           └── route.ts          # GET /api/planetary-data
│   ├── lib/
│   │   ├── types.ts                  # TypeScript interfaces
│   │   ├── supabase.ts               # Supabase client
│   │   ├── database.ts               # Database functions
│   │   ├── api.ts                    # Frontend API client
│   │   ├── astrologyAnalysis.ts      # Analysis logic
│   │   ├── houseMapping.ts           # ⭐ NEW - House mapping & aspects
│   │   └── storeCorrelations.ts      # Store correlations, mappings, aspects
│   └── components/
│       └── TransitTable.tsx          # Planetary positions table
│
├── api_server.py                     # Flask API (Swiss Ephemeris)
├── daily_planetary_job.py            # Cron job: Daily calculations
├── import_automated_events.py        # Cron job: Event collection
├── email_reports.py                  # Cron job: Email reports
├── database_schema.sql               # Complete database schema
│
├── requirements.txt                  # Python dependencies
├── package.json                      # Node.js dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
│
└── Documentation/
    ├── COMPLETE_SYSTEM_DOCUMENTATION.md  # This file
    ├── QUERY_HOUSE_MAPPINGS.md           # SQL query examples
    ├── QUERY_PLANETARY_DATA.md           # Planetary data queries
    └── README.md                         # Quick start guide
```

---

## 🔑 Environment Configuration

### Required Environment Variables

Create `.env.local` file in the `CosmicDiary` directory:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# Flask API Configuration (optional, defaults to localhost:8000)
FLASK_API_URL=http://localhost:8000

# OpenAI API (optional, for automated event collection)
OPENAI_API_KEY=your-openai-api-key-here

# Email Configuration (optional, for email reports)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
```

### Key Sources

1. **Supabase Keys:**
   - Go to Supabase Dashboard → Project Settings → API
   - Copy `Project URL` → `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL`
   - Copy `anon public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Copy `service_role` key → `SUPABASE_SERVICE_ROLE_KEY`

2. **OpenAI API Key:**
   - Get from https://platform.openai.com/api-keys
   - Only needed for automated event collection

3. **Email Password:**
   - Gmail: Use App Password (not regular password)
   - Generate at: Google Account → Security → 2-Step Verification → App Passwords

---

## 🚀 Installation & Setup

### Prerequisites

- Node.js 18+
- Python 3.9+
- Supabase account
- (Optional) OpenAI API key
- (Optional) Email credentials

### Step 1: Clone Repository

```bash
git clone https://github.com/sivaramanrajagopal/cosmicdiary.git
cd cosmicdiary/CosmicDiary
```

### Step 2: Install Dependencies

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

1. Create Supabase project at https://supabase.com
2. Go to SQL Editor
3. Copy entire `database_schema.sql` file
4. Paste and run in SQL Editor
5. Verify tables created: Check Table Editor

### Step 4: Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local with your keys
```

### Step 5: Start Services

**Terminal 1 - Flask API:**
```bash
cd CosmicDiary
python3 api_server.py
# Running on http://localhost:8000
```

**Terminal 2 - Next.js Frontend:**
```bash
cd CosmicDiary
npm run dev
# Running on http://localhost:3000 (or 3002 if 3000 is in use)
```

### Step 6: Setup Cron Jobs (Optional)

```bash
cd CosmicDiary
chmod +x setup_cron.sh
./setup_cron.sh
```

This sets up:
- Daily planetary calculations (midnight)
- Event collection (twice daily)
- Email reports (daily/weekly)

---

## ✨ Features & Outcomes

### 1. Event Management

**What it does:**
- Create, view, edit, delete events
- Categorize events (Natural Disaster, War, Economic, etc.)
- Set impact levels (low, medium, high, critical)
- Add tags and metadata

**Outcome:**
- Organized event database
- Searchable and filterable events
- Geolocation support for future features

---

### 2. Planetary Position Calculations

**What it does:**
- Calculates accurate planetary positions using Swiss Ephemeris
- Uses Lahiri Ayanamsa for sidereal calculations
- Determines Rasi, Nakshatra, Retrograde status
- Stores daily data automatically

**Outcome:**
- Accurate astrological data for any date
- Historical planetary positions
- On-demand calculations for any date

---

### 3. House Mapping (Kalapurushan)

**What it does:**
- Maps events to houses (1-12) based on category and significations
- Uses traditional house significations
- Stores mapping reason

**Mapping Logic:**
- Event category → House significations matching
- Example: "Natural Disaster" → House 6 (Enemies/Diseases) or House 8 (Transformation)
- Example: "Economic Event" → House 2 (Wealth) or House 11 (Gains)

**Outcome:**
- Every event has an associated house
- Enables house-based analysis
- Foundation for aspect calculations

---

### 4. Planetary Aspects (Drishti)

**What it does:**
- Calculates which planets aspect the event's house
- Uses traditional Drishti system
- Tracks aspect strength

**Aspect System:**
- **Jupiter**: 5th, 7th, 9th houses from its position
- **Saturn**: 3rd, 7th, 10th houses
- **Mars**: 4th, 7th, 8th houses
- **Rahu/Ketu**: 3rd, 7th, 11th + dustana (6, 8, 12)
- **Sun/Moon/Mercury/Venus**: 7th house only
- **Conjunction**: Planet in the same house as event

**Outcome:**
- Complete aspect analysis for each event
- Identifies significant planetary influences
- Enables pattern recognition

---

### 5. Correlation Analysis

**What it does:**
- Analyzes planetary influences on events
- Identifies significant planets based on:
  - Event category matching planet significations
  - Retrograde planets
  - Dominant Rasi lords
  - Impact level associations

**Outcome:**
- Automated astrological insights
- Pattern identification
- Research-ready data

---

### 6. Analysis Dashboard

**Pages:**

1. **Home (`/`)**
   - Recent events overview
   - Quick navigation
   - System status

2. **Events (`/events`)**
   - List all events
   - Filter by date, category
   - Search functionality

3. **Planets (`/planets`)**
   - View planetary positions for any date
   - Interactive date picker
   - Transit table display

4. **Analysis (`/analysis`)**
   - Astrological analysis overview
   - Planetary patterns
   - Category-planetary correlations
   - Retrograde analysis

5. **House Analysis (`/house-analysis`)** ⭐ NEW
   - Complete table view of house mappings
   - Planetary aspects display
   - House distribution statistics
   - Aspect type distribution

---

## 📊 Output & Outcomes

### Data Stored Per Event

When an event is created, the system automatically stores:

1. **Event Record** (`events` table)
   - Basic event information

2. **House Mapping** (`event_house_mappings` table)
   - House number (1-12)
   - Rasi name
   - Significations
   - Mapping reason

3. **Planetary Aspects** (`event_planetary_aspects` table)
   - All planets aspecting the event's house
   - Aspect types and strengths
   - Planet positions

4. **Planetary Correlations** (`event_planetary_correlations` table)
   - Significant planets based on category
   - Retrograde planets
   - Correlation scores

### Analysis Capabilities

1. **House-Based Analysis**
   - Which houses are most active for certain event types
   - House distribution patterns
   - Event clustering by house

2. **Aspect Analysis**
   - Which planets commonly aspect specific houses
   - Aspect type patterns (e.g., Mars aspecting 8th house during disasters)
   - Aspect strength correlations with event impact

3. **Temporal Analysis**
   - Planetary patterns over time
   - Retrograde influences
   - Rasi and Nakshatra dominance

4. **Category Analysis**
   - Which planets correlate with which event categories
   - House-aspect combinations for event types
   - Historical pattern recognition

---

## 🔄 Data Flow

### Event Creation Flow

```
User Creates Event
    ↓
POST /api/events
    ↓
Store Event in Database
    ↓
┌───────────────────────────────────────┐
│ Automatic Calculations (Async)        │
├───────────────────────────────────────┤
│ 1. Get Planetary Data for Event Date  │
│    ├─ Check Database                  │
│    └─ Fallback to Flask API          │
│                                        │
│ 2. Map Event to House                 │
│    ├─ Analyze category                │
│    ├─ Match significations            │
│    └─ Store in event_house_mappings   │
│                                        │
│ 3. Calculate Planetary Aspects        │
│    ├─ Get planet positions            │
│    ├─ Calculate aspects to house      │
│    └─ Store in event_planetary_aspects│
│                                        │
│ 4. Calculate Correlations             │
│    ├─ Identify significant planets    │
│    ├─ Check retrograde status         │
│    └─ Store in event_planetary_       │
│       correlations                     │
└───────────────────────────────────────┘
    ↓
Event Created with Full Analysis
```

### Daily Planetary Data Flow

```
Cron Job (Midnight)
    ↓
daily_planetary_job.py
    ↓
Fetch from Flask API (/api/planets/daily)
    ↓
Swiss Ephemeris Calculation
    ↓
Store in planetary_data table
    ↓
Data Available for Event Analysis
```

---

## 🧪 Testing & Verification

### Test Event Creation

```bash
# Create a test event
curl -X POST http://localhost:3002/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-10",
    "title": "Test Natural Disaster",
    "category": "Natural Disaster",
    "impact_level": "high",
    "event_type": "world"
  }'
```

**Expected Result:**
- Event created in database
- House mapping stored (likely House 6 or 8)
- Planetary aspects calculated
- Correlations stored

### Verify Data

**In Supabase SQL Editor:**
```sql
-- Check event
SELECT * FROM events ORDER BY created_at DESC LIMIT 1;

-- Check house mapping
SELECT * FROM event_house_mappings ORDER BY created_at DESC LIMIT 1;

-- Check aspects
SELECT * FROM event_planetary_aspects ORDER BY created_at DESC LIMIT 10;

-- Check correlations
SELECT * FROM event_planetary_correlations ORDER BY created_at DESC LIMIT 10;
```

---

## 📈 Performance Considerations

1. **Database Indexes**
   - All frequently queried fields are indexed
   - GIN index on JSONB for fast planetary data queries

2. **Async Processing**
   - Correlations/mappings calculated asynchronously
   - Doesn't block event creation

3. **Caching**
   - Planetary data stored in database (cached)
   - Flask API only called when needed

4. **Optimization**
   - Batch queries where possible
   - Efficient JSONB queries

---

## 🔮 Future Enhancements

1. **Ascendant-Based Charts**
   - Calculate actual ascendant for event location/time
   - Use geolocation to determine house system

2. **Advanced Aspects**
   - Conjunctions between planets
   - Planetary transits
   - Dasha/Bhukti periods

3. **Machine Learning**
   - Pattern prediction
   - Event probability scoring
   - Automated insights

4. **Visualizations**
   - Chart displays
   - Aspect diagrams
   - Timeline views

---

## 🐛 Troubleshooting

### Issue: Planetary data not found

**Solution:**
- Check Flask API is running (`http://localhost:8000/health`)
- Verify date format (YYYY-MM-DD)
- Check database for existing data

### Issue: House mappings not created

**Solution:**
- Verify `event_house_mappings` table exists
- Check event has valid category
- Run recalculation: `/api/events/recalculate-correlations`

### Issue: Aspects not calculated

**Solution:**
- Ensure planetary data exists for event date
- Check `event_planetary_aspects` table exists
- Verify house mapping was created first

---

## 📚 Key Files Reference

### Core Logic Files

- **`src/lib/houseMapping.ts`**: House mapping and aspect calculation logic
- **`src/lib/astrologyAnalysis.ts`**: Correlation analysis logic
- **`src/lib/storeCorrelations.ts`**: Database storage functions
- **`src/lib/database.ts`**: All database operations

### Configuration Files

- **`database_schema.sql`**: Complete database schema
- **`.env.local`**: Environment variables (not in git)
- **`package.json`**: Node.js dependencies
- **`requirements.txt`**: Python dependencies

### API Files

- **`api_server.py`**: Flask API server
- **`src/app/api/**`**: Next.js API routes

---

## ✅ Implementation Checklist

- [x] Database schema created
- [x] Event CRUD operations
- [x] Planetary data calculation (Swiss Ephemeris)
- [x] House mapping system (Kalapurushan)
- [x] Planetary aspects (Drishti)
- [x] Correlation analysis
- [x] Automated data collection
- [x] Email reporting
- [x] Analysis dashboard
- [x] House analysis page
- [x] Cron job setup
- [x] Error handling
- [x] Documentation

---

## 📞 Support & Maintenance

### Logs Location

- Planetary job: `logs/planetary.log`
- Event collection: `logs/event_collection.log`
- Email reports: `logs/email_reports.log`

### Database Maintenance

- Regular backups recommended
- Monitor table sizes
- Optimize indexes periodically

### Updates

- Pull latest from GitHub
- Run database migrations if needed
- Restart services

---

## 🎓 Astrological Concepts Explained

### Kalapurushan Chart

A fixed sign-based chart where:
- Aries always = 1st House
- Taurus always = 2nd House
- ... and so on

Used for general/universal analysis without calculating actual ascendant.

### House Significations

Each house rules specific life areas:
- **1st**: Self, personality
- **2nd**: Wealth, family
- **6th**: Enemies, diseases
- **8th**: Transformation, longevity
- **10th**: Career, karma
- **12th**: Losses, isolation

### Planetary Aspects (Drishti)

Planets "look at" or influence certain houses from their position. Different planets have different aspect patterns, creating complex interactions.

### Dustana Houses

Houses 6, 8, 12 are considered challenging (dustana). Rahu and Ketu have special influence on these houses.

---

## 📖 Additional Resources

- **Swiss Ephemeris**: https://www.astro.com/swisseph/
- **Supabase Docs**: https://supabase.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Traditional Vedic Astrology**: Parasara, Brihat Parashara Hora Shastra

---

**End of Documentation**

For questions or issues, refer to:
- `QUERY_HOUSE_MAPPINGS.md` - SQL query examples
- `QUERY_PLANETARY_DATA.md` - Planetary data queries
- GitHub Issues: https://github.com/sivaramanrajagopal/cosmicdiary/issues

