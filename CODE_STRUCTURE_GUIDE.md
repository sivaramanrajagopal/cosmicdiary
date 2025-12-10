# 📁 Code Structure & Organization Guide

This document explains how the codebase is organized and how different parts work together.

---

## 🗂️ Directory Structure

```
CosmicDiary/
│
├── 📂 src/                          # Source code
│   ├── 📂 app/                      # Next.js App Router (file-based routing)
│   │   ├── 📄 page.tsx             # Home page (/) 
│   │   ├── 📄 layout.tsx           # Root layout (wraps all pages)
│   │   ├── 📄 globals.css          # Global Tailwind styles
│   │   │
│   │   ├── 📂 events/              # Events section
│   │   │   ├── 📄 page.tsx         # List all events (/events)
│   │   │   ├── 📂 new/
│   │   │   │   └── 📄 page.tsx     # Create event form (/events/new)
│   │   │   └── 📂 [id]/            # Dynamic route
│   │   │       └── 📄 page.tsx     # Event detail (/events/123)
│   │   │
│   │   ├── 📂 planets/             # Planetary positions viewer
│   │   │   └── 📄 page.tsx         # Planets page (/planets)
│   │   │
│   │   ├── 📂 analysis/            # Astrological analysis
│   │   │   └── 📄 page.tsx         # Analysis dashboard (/analysis)
│   │   │
│   │   ├── 📂 house-analysis/      # ⭐ House mappings & aspects
│   │   │   └── 📄 page.tsx         # House analysis table (/house-analysis)
│   │   │
│   │   └── 📂 api/                 # API Routes (Serverless functions)
│   │       ├── 📂 events/
│   │       │   ├── 📄 route.ts                    # GET/POST /api/events
│   │       │   ├── 📂 [id]/
│   │       │   │   └── 📄 route.ts                # GET /api/events/[id]
│   │       │   ├── 📂 import/
│   │       │   │   └── 📄 route.ts                # POST /api/events/import
│   │       │   └── 📂 recalculate-correlations/
│   │       │       └── 📄 route.ts                # GET/POST recalculation
│   │       └── 📂 planetary-data/
│   │           └── 📄 route.ts                    # GET /api/planetary-data
│   │
│   ├── 📂 lib/                     # Shared libraries & utilities
│   │   ├── 📄 types.ts             # TypeScript type definitions
│   │   ├── 📄 supabase.ts          # Supabase client initialization
│   │   ├── 📄 database.ts          # Database CRUD operations
│   │   ├── 📄 api.ts               # Frontend API client functions
│   │   ├── 📄 astrologyAnalysis.ts # Correlation analysis logic
│   │   ├── 📄 houseMapping.ts      # ⭐ House mapping & aspect calculations
│   │   └── 📄 storeCorrelations.ts # Store correlations/mappings/aspects
│   │
│   └── 📂 components/              # Reusable React components
│       └── 📄 TransitTable.tsx     # Planetary positions table component
│
├── 📂 Python Scripts/              # Backend automation
│   ├── 📄 api_server.py            # Flask API server (Swiss Ephemeris)
│   ├── 📄 daily_planetary_job.py   # Cron job: Daily planetary calculations
│   ├── 📄 import_automated_events.py # Cron job: Event collection
│   ├── 📄 email_reports.py         # Cron job: Email reports
│   ├── 📄 test_supabase_connection.py # Testing utility
│   └── 📄 test_full_setup.py       # Integration tests
│
├── 📂 Configuration Files/
│   ├── 📄 database_schema.sql      # Complete database schema
│   ├── 📄 package.json             # Node.js dependencies
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 tsconfig.json            # TypeScript configuration
│   ├── 📄 tailwind.config.js       # Tailwind CSS configuration
│   ├── 📄 next.config.js           # Next.js configuration
│   └── 📄 .env.local               # Environment variables (not in git)
│
└── 📂 Documentation/
    ├── 📄 COMPLETE_SYSTEM_DOCUMENTATION.md  # Main documentation
    ├── 📄 CODE_STRUCTURE_GUIDE.md           # This file
    ├── 📄 QUERY_HOUSE_MAPPINGS.md           # SQL examples
    ├── 📄 QUERY_PLANETARY_DATA.md           # Planetary queries
    └── 📄 README.md                         # Quick start
```

---

## 🔄 Code Flow & Data Layers

### Layer 1: Presentation (Frontend Pages)

**Location:** `src/app/**/page.tsx`

**Responsibilities:**
- Display data to users
- Handle user interactions
- Format and present information

**Pattern:**
```typescript
// Server Component (default)
export default async function PageName() {
  // Fetch data directly from database
  const data = await getDataFromDatabase();
  
  // Render UI
  return <div>...</div>;
}
```

**Examples:**
- `src/app/page.tsx` - Home page
- `src/app/events/page.tsx` - Events list
- `src/app/house-analysis/page.tsx` - House analysis table

---

### Layer 2: API Routes (Serverless Functions)

**Location:** `src/app/api/**/route.ts`

**Responsibilities:**
- Handle HTTP requests
- Validate input
- Call business logic
- Return JSON responses

**Pattern:**
```typescript
export async function GET(request: NextRequest) {
  // Get query params
  const params = request.nextUrl.searchParams;
  
  // Call database functions
  const data = await getData();
  
  // Return JSON
  return NextResponse.json(data);
}
```

**Examples:**
- `src/app/api/events/route.ts` - Event CRUD
- `src/app/api/planetary-data/route.ts` - Planetary data fetching

---

### Layer 3: Business Logic

**Location:** `src/lib/**`

#### 3.1 Database Layer (`database.ts`)

**Functions:**
- `getEvents()` - Fetch events
- `createEvent()` - Create event
- `getPlanetaryData()` - Fetch planetary positions
- `createHouseMapping()` - Store house mapping
- `createPlanetaryAspect()` - Store aspect
- `createCorrelation()` - Store correlation

**Pattern:**
```typescript
export async function getData() {
  const { data, error } = await supabase
    .from('table_name')
    .select('*');
  
  if (error) return null;
  return data;
}
```

---

#### 3.2 Astrological Logic

**`houseMapping.ts`** - House & Aspect Calculations
- `mapEventToHouse()` - Maps event to house (1-12)
- `calculatePlanetaryAspects()` - Calculates aspects to house
- `getAspectingHouses()` - Which houses a planet aspects
- `getAspectType()` - Determines aspect type

**`astrologyAnalysis.ts`** - Correlation Analysis
- `analyzeEventPlanetaryCorrelation()` - Main analysis function
- `findSignificantPlanets()` - Identifies important planets
- `generateCorrelations()` - Creates correlation objects

**`storeCorrelations.ts`** - Storage Orchestration
- `calculateAndStoreCorrelations()` - Complete calculation & storage
- `recalculateAllCorrelations()` - Batch recalculation

---

### Layer 4: External Services

#### Flask API (`api_server.py`)

**Endpoints:**
- `/health` - Health check
- `/api/planets/daily?date=YYYY-MM-DD` - Calculate planetary positions

**Responsibilities:**
- Swiss Ephemeris calculations
- Rasi/Nakshatra determination
- Retrograde detection

---

#### Supabase Database

**Tables:**
1. `events` - Event records
2. `planetary_data` - Daily planetary positions
3. `event_planetary_correlations` - Planet-event correlations
4. `event_house_mappings` - House mappings
5. `event_planetary_aspects` - Planetary aspects

---

## 🔀 Data Flow Examples

### Example 1: Creating an Event

```
User fills form
    ↓
Submit to /events/new page
    ↓
POST /api/events
    ↓
createEvent() in database.ts
    ↓
Insert into events table
    ↓
Return created event
    ↓
Async: calculateAndStoreCorrelations()
    ├─ mapEventToHouse()
    │  └─ Store in event_house_mappings
    ├─ calculatePlanetaryAspects()
    │  └─ Store in event_planetary_aspects
    └─ analyzeEventPlanetaryCorrelation()
       └─ Store in event_planetary_correlations
```

### Example 2: Viewing Planetary Data

```
User visits /planets?date=2025-12-10
    ↓
Planets page component
    ↓
Fetch from /api/planetary-data?date=2025-12-10
    ↓
Check database first (getPlanetaryData())
    ↓
Not found? Call Flask API
    ↓
Flask calculates with Swiss Ephemeris
    ↓
Store in database (createPlanetaryData())
    ↓
Return to frontend
    ↓
Display in TransitTable component
```

### Example 3: House Analysis Page

```
User visits /house-analysis
    ↓
HouseAnalysisPage component
    ↓
Loop through all events:
    ├─ getHouseMapping(event.id)
    └─ getPlanetaryAspects(event.id)
    ↓
Aggregate data
    ↓
Display in table format
```

---

## 📦 Key Modules Explained

### `src/lib/types.ts`

**Purpose:** TypeScript type definitions

**Key Interfaces:**
- `Event` - Event structure
- `Planet` - Planet position data
- `PlanetaryData` - Planetary data wrapper
- `EventHouseMapping` - House mapping structure
- `EventPlanetaryAspect` - Aspect data structure

**Usage:**
```typescript
import { Event, Planet } from '@/lib/types';
```

---

### `src/lib/supabase.ts`

**Purpose:** Supabase client initialization

**Key Features:**
- Validates environment variables
- Creates Supabase client
- Error handling for missing config

---

### `src/lib/database.ts`

**Purpose:** All database operations

**Categories:**
1. **Event Operations**
   - `getEvents()`, `getEventById()`, `createEvent()`

2. **Planetary Data Operations**
   - `getPlanetaryData()`, `createPlanetaryData()`

3. **Correlation Operations**
   - `getEventCorrelations()`, `createCorrelation()`

4. **House Mapping Operations** ⭐
   - `getHouseMapping()`, `createHouseMapping()`

5. **Aspect Operations** ⭐
   - `getPlanetaryAspects()`, `createPlanetaryAspect()`

---

### `src/lib/houseMapping.ts` ⭐

**Purpose:** House mapping and aspect calculation logic

**Key Functions:**

1. **`mapEventToHouse(event)`**
   - Analyzes event category
   - Matches against house significations
   - Returns house mapping object

2. **`calculatePlanetaryAspects(event, houseMapping, planetaryData)`**
   - Gets all planet positions
   - Calculates which planets aspect the house
   - Determines aspect types and strengths
   - Returns array of aspects

3. **`getAspectingHouses(planet, planetName)`**
   - Calculates which houses a planet aspects
   - Based on Drishti rules

4. **`getAspectType(planet, planetName, aspectingHouses, targetHouse)`**
   - Determines specific aspect type
   - (conjunction, drishti_3rd, drishti_7th, etc.)

---

### `src/lib/storeCorrelations.ts`

**Purpose:** Orchestrates storage of all analysis data

**Key Function:**

**`calculateAndStoreCorrelations(event)`**
1. Gets planetary data for event date
2. Maps event to house
3. Calculates aspects
4. Analyzes correlations
5. Stores everything in database

**Used by:**
- Event creation API
- Recalculation endpoint

---

## 🎨 Component Architecture

### Server Components (Default)

**Location:** `src/app/**/page.tsx`

**Characteristics:**
- Async functions
- Direct database access
- No client-side JavaScript
- Fast initial load

**Example:**
```typescript
export default async function Page() {
  const data = await getData(); // Direct DB call
  return <div>{data}</div>;
}
```

---

### Client Components

**Location:** `src/app/**/page.tsx` (with `'use client'`)

**Use Cases:**
- Forms with state
- Interactive elements
- API calls from browser

**Example:**
```typescript
'use client';

export default function FormPage() {
  const [state, setState] = useState();
  // ...
}
```

---

### Shared Components

**Location:** `src/components/`

**Example: `TransitTable.tsx`**
- Reusable planetary positions table
- Used in planets page and event detail page

---

## 🔐 Security & Best Practices

### Environment Variables

**Never commit:**
- `.env.local`
- `.env` (with real keys)

**Always commit:**
- `.env.example` (with placeholders)

### Database Access

- Frontend uses `anon` key (public, limited by RLS)
- Backend scripts use `service_role` key (full access)
- RLS policies control access

### Error Handling

- All database functions return `null` on error
- API routes return appropriate HTTP status codes
- Console logging for debugging

---

## 🧪 Testing Approach

### Manual Testing

1. **Create Event**
   - Check all tables populated
   - Verify house mapping correct
   - Check aspects calculated

2. **Query Data**
   - Use Supabase SQL Editor
   - Run queries from `QUERY_HOUSE_MAPPINGS.md`

3. **Verify Calculations**
   - Compare with astrological software
   - Check aspect logic manually

### Automated Testing (Future)

- Unit tests for calculation functions
- Integration tests for API endpoints
- Database migration tests

---

## 🚀 Deployment Considerations

### Environment Setup

1. Set all environment variables in production
2. Run database migrations
3. Set up cron jobs on server
4. Configure email SMTP
5. Set up monitoring

### Scaling

- Next.js API routes auto-scale
- Supabase handles database scaling
- Flask API can be deployed separately (e.g., on Heroku, Railway)

---

## 📝 Code Style Guide

### TypeScript

- Use interfaces for all data structures
- Type all function parameters and returns
- Avoid `any` type

### Naming Conventions

- **Files**: camelCase (e.g., `houseMapping.ts`)
- **Components**: PascalCase (e.g., `EventDetailPage`)
- **Functions**: camelCase (e.g., `calculatePlanetaryAspects`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `RASI_TO_HOUSE`)

### File Organization

- One main export per file
- Related functions grouped together
- Keep files focused (single responsibility)

---

## 🔍 Debugging Guide

### Common Issues

1. **Planetary data missing**
   - Check Flask API running
   - Verify date format
   - Check database

2. **House mapping not created**
   - Verify event has category
   - Check calculation ran
   - Review logs

3. **Aspects not calculated**
   - Ensure planetary data exists
   - Check house mapping created
   - Verify aspect logic

### Debug Tools

- Browser DevTools for frontend
- Next.js server logs for API routes
- Flask console output
- Supabase SQL Editor for database

---

## 📚 Further Reading

- **Next.js App Router**: https://nextjs.org/docs/app
- **Supabase JS Client**: https://supabase.com/docs/reference/javascript
- **Swiss Ephemeris**: https://www.astro.com/swisseph/
- **TypeScript**: https://www.typescriptlang.org/docs/

---

**This guide should help you understand how everything fits together!**

