-- ============================================================================
-- Migration 008: Create Cosmic Snapshots Table
-- ============================================================================
-- 
-- Description:
--   Creates a table to store planetary state snapshots captured every 2 hours
--   for correlation analysis. Each snapshot represents the complete astrological
--   state at a specific moment, including ascendant, planetary positions, aspects,
--   and special configurations. This enables temporal analysis of planetary
--   influences and event correlations.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- Purpose:
--   - Track planetary positions every 2 hours for temporal correlation
--   - Enable analysis of planetary patterns over time
--   - Support correlation between events and planetary states
--   - Store active aspects and yogas at each snapshot
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the migration
--   5. Verify the new table and its structure in the Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/008_create_cosmic_snapshots_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Create cosmic_snapshots Table
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cosmic_snapshots (
    id BIGSERIAL PRIMARY KEY,
    
    -- Snapshot Timestamp
    snapshot_time TIMESTAMPTZ NOT NULL,
    
    -- Reference Location (default: Delhi, India)
    reference_location TEXT DEFAULT 'Delhi, India',
    reference_latitude REAL DEFAULT 28.6139 CHECK (reference_latitude >= -90 AND reference_latitude <= 90),
    reference_longitude REAL DEFAULT 77.2090 CHECK (reference_longitude >= -180 AND reference_longitude <= 180),
    reference_timezone TEXT DEFAULT 'Asia/Kolkata',
    
    -- Lagna (Ascendant) Information
    lagna_degree REAL NOT NULL CHECK (lagna_degree >= 0 AND lagna_degree < 360),
    lagna_rasi TEXT NOT NULL,
    lagna_rasi_number INT NOT NULL CHECK (lagna_rasi_number BETWEEN 1 AND 12),
    lagna_nakshatra TEXT,
    lagna_lord TEXT NOT NULL,
    
    -- Chart Data
    house_cusps JSONB NOT NULL, -- Array of 12 house cusp degrees [h1_deg, h2_deg, ..., h12_deg]
    planetary_positions JSONB NOT NULL, -- All 9 planets with positions, houses, rasis, nakshatras
    active_aspects JSONB, -- All planetary aspects active at this moment
    retrograde_planets TEXT[], -- Array of planet names currently retrograde (e.g., ['Jupiter', 'Saturn'])
    dominant_planets JSONB, -- Strongest planets by dig bala and strength
    active_yogas JSONB, -- Special planetary combinations (yogas) active at this time
    
    -- Moon Details (fast-changing, important for timing)
    moon_rasi TEXT,
    moon_nakshatra TEXT,
    moon_tithi TEXT, -- Lunar day (e.g., 'Shukla Paksha Panchami')
    
    -- Calculation Metadata
    ayanamsa REAL NOT NULL, -- Ayanamsa value used (e.g., Lahiri)
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE cosmic_snapshots IS 
'Stores planetary state snapshots captured every 2 hours for temporal correlation analysis. Each row represents the complete astrological configuration at a specific moment, enabling analysis of planetary patterns and event correlations over time.';

COMMENT ON COLUMN cosmic_snapshots.snapshot_time IS 
'The exact timestamp when this planetary snapshot was captured (TIMESTAMPTZ format). Used for temporal ordering and correlation with events.';

COMMENT ON COLUMN cosmic_snapshots.reference_location IS 
'Text description of the reference location used for calculations (e.g., "Delhi, India"). Default: Delhi, India.';

COMMENT ON COLUMN cosmic_snapshots.reference_latitude IS 
'Latitude in degrees of the reference location. Default: 28.6139 (Delhi). Range: -90 to 90.';

COMMENT ON COLUMN cosmic_snapshots.reference_longitude IS 
'Longitude in degrees of the reference location. Default: 77.2090 (Delhi). Range: -180 to 180.';

COMMENT ON COLUMN cosmic_snapshots.reference_timezone IS 
'IANA timezone string for the reference location (e.g., "Asia/Kolkata"). Default: Asia/Kolkata.';

COMMENT ON COLUMN cosmic_snapshots.lagna_degree IS 
'The degree of the Lagna (Ascendant) in the zodiac (0-360 degrees).';

COMMENT ON COLUMN cosmic_snapshots.lagna_rasi IS 
'The zodiac sign (Rasi) of the Lagna (e.g., "Aries", "Taurus").';

COMMENT ON COLUMN cosmic_snapshots.lagna_rasi_number IS 
'The numerical representation of the Lagna Rasi (1 for Aries, 2 for Taurus, ..., 12 for Pisces).';

COMMENT ON COLUMN cosmic_snapshots.lagna_nakshatra IS 
'The Nakshatra (lunar mansion) in which the Lagna falls (e.g., "Ashwini", "Bharani").';

COMMENT ON COLUMN cosmic_snapshots.lagna_lord IS 
'The planetary ruler of the Lagna Rasi (e.g., "Mars" for Aries, "Venus" for Taurus).';

COMMENT ON COLUMN cosmic_snapshots.house_cusps IS 
'JSONB array containing the starting degrees of the 12 astrological houses. Format: [House1_Cusp_Deg, House2_Cusp_Deg, ..., House12_Cusp_Deg]. Example: [45.5, 75.2, 105.8, 135.3, 165.1, 195.6, 225.4, 255.9, 285.7, 315.2, 345.8, 15.3].';

COMMENT ON COLUMN cosmic_snapshots.planetary_positions IS 
'JSONB object containing detailed positions for all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu). Each planet includes longitude, latitude, speed, is_retrograde, rasi, nakshatra, house placement, and lord. See example structure below.';

COMMENT ON COLUMN cosmic_snapshots.active_aspects IS 
'JSONB array of all planetary aspects active at this snapshot time. Includes drishti (glances), conjunctions, and special aspects. See example structure below.';

COMMENT ON COLUMN cosmic_snapshots.retrograde_planets IS 
'Array of planet names that are currently retrograde at this snapshot time. Example: ["Jupiter", "Saturn", "Rahu", "Ketu"]. Empty array [] if no planets are retrograde.';

COMMENT ON COLUMN cosmic_snapshots.dominant_planets IS 
'JSONB array of the strongest planets at this snapshot, ordered by strength. Includes strength scores and reasons (exalted, dig bala, own sign, etc.). See example structure below.';

COMMENT ON COLUMN cosmic_snapshots.active_yogas IS 
'JSONB array of special planetary combinations (yogas) active at this snapshot. Examples include Raj Yoga, Dhan Yoga, Vipreet Raj Yoga, etc. See example structure below.';

COMMENT ON COLUMN cosmic_snapshots.moon_rasi IS 
'The zodiac sign (Rasi) where the Moon is placed (e.g., "Cancer", "Leo"). Important for timing and emotional influences.';

COMMENT ON COLUMN cosmic_snapshots.moon_nakshatra IS 
'The Nakshatra where the Moon is placed (e.g., "Punarvasu", "Pushya"). Used for muhurta and timing calculations.';

COMMENT ON COLUMN cosmic_snapshots.moon_tithi IS 
'The lunar day (Tithi) at this snapshot (e.g., "Shukla Paksha Panchami", "Krishna Paksha Dwadashi"). Important for Vedic timing.';

COMMENT ON COLUMN cosmic_snapshots.ayanamsa IS 
'The Ayanamsa value (precession correction) used for sidereal calculations (e.g., Lahiri). Typically around 24 degrees for current era.';

-- ----------------------------------------------------------------------------
-- Indexes for Performance
-- ----------------------------------------------------------------------------

-- Index on snapshot_time for temporal queries (DESC for most recent first)
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_time 
ON cosmic_snapshots(snapshot_time DESC);

COMMENT ON INDEX idx_cosmic_snapshots_time IS 
'Index on snapshot_time for efficient temporal queries. DESC order optimizes queries for most recent snapshots first.';

-- Index on lagna_rasi for filtering by ascendant sign
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_lagna 
ON cosmic_snapshots(lagna_rasi);

COMMENT ON INDEX idx_cosmic_snapshots_lagna IS 
'Index on lagna_rasi for filtering snapshots by ascendant sign. Useful for analyzing patterns based on Lagna.';

-- Composite index on snapshot_time and lagna_rasi for combined queries
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_time_lagna 
ON cosmic_snapshots(snapshot_time DESC, lagna_rasi);

-- GIN index on planetary_positions for efficient JSONB queries
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_positions_gin 
ON cosmic_snapshots USING GIN (planetary_positions);

COMMENT ON INDEX idx_cosmic_snapshots_positions_gin IS 
'GIN index on planetary_positions JSONB for efficient queries filtering by planet positions, houses, or rasis.';

-- GIN index on active_aspects for efficient aspect queries
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_aspects_gin 
ON cosmic_snapshots USING GIN (active_aspects);

COMMENT ON INDEX idx_cosmic_snapshots_aspects_gin IS 
'GIN index on active_aspects JSONB for efficient queries filtering by active planetary aspects.';

-- Index on retrograde_planets array for filtering by retrograde status
CREATE INDEX IF NOT EXISTS idx_cosmic_snapshots_retrograde 
ON cosmic_snapshots USING GIN (retrograde_planets);

COMMENT ON INDEX idx_cosmic_snapshots_retrograde IS 
'GIN index on retrograde_planets array for efficient queries filtering snapshots where specific planets are retrograde.';

-- ----------------------------------------------------------------------------
-- Row Level Security (RLS)
-- ----------------------------------------------------------------------------

ALTER TABLE cosmic_snapshots ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations on cosmic_snapshots (can be restricted later)
DROP POLICY IF EXISTS "Allow all operations on cosmic_snapshots" ON cosmic_snapshots;
CREATE POLICY "Allow all operations on cosmic_snapshots" ON cosmic_snapshots
    FOR ALL USING (true) WITH CHECK (true);

-- ----------------------------------------------------------------------------
-- Example JSONB Structures (for reference)
-- ----------------------------------------------------------------------------

/*
Example planetary_positions JSONB structure:
{
  "Sun": {
    "longitude": 232.5,
    "latitude": 0.0,
    "speed": 1.0,
    "is_retrograde": false,
    "rasi": {"name": "Scorpio", "number": 8, "lord": "Mars"},
    "nakshatra": {"name": "Jyeshtha", "number": 18, "pada": 2},
    "house": 3
  },
  "Moon": {
    "longitude": 147.32,
    "latitude": 0.31,
    "speed": 13.2,
    "is_retrograde": false,
    "rasi": {"name": "Leo", "number": 5, "lord": "Sun"},
    "nakshatra": {"name": "Purva Phalguni", "number": 11, "pada": 3},
    "house": 11
  },
  "Mars": {
    "longitude": 242.67,
    "latitude": 1.2,
    "speed": 0.5,
    "is_retrograde": false,
    "rasi": {"name": "Sagittarius", "number": 9, "lord": "Jupiter"},
    "nakshatra": {"name": "Mula", "number": 19, "pada": 1},
    "house": 4
  },
  "Mercury": {...},
  "Jupiter": {...},
  "Venus": {...},
  "Saturn": {...},
  "Rahu": {...},
  "Ketu": {...}
}

Example active_aspects JSONB structure:
[
  {
    "planet": "Mars",
    "from_house": 1,
    "to_house": 8,
    "type": "drishti_8th",
    "strength": "strong",
    "target_planet": null,
    "target_house": 8
  },
  {
    "planet": "Jupiter",
    "from_house": 5,
    "to_house": 9,
    "type": "drishti_9th",
    "strength": "moderate",
    "target_planet": null,
    "target_house": 9
  },
  {
    "planet": "Saturn",
    "from_house": 7,
    "to_house": 1,
    "type": "drishti_7th",
    "strength": "strong",
    "target_planet": "Sun",
    "target_house": 1
  },
  {
    "planet": "Sun",
    "from_house": 1,
    "to_house": 1,
    "type": "conjunction",
    "strength": "strong",
    "target_planet": "Mercury",
    "target_house": 1
  }
]

Example dominant_planets JSONB structure:
[
  {
    "planet": "Jupiter",
    "strength_score": 0.85,
    "reasons": ["exalted", "dig_bala"],
    "house": 9,
    "rasi": "Cancer",
    "rank": 1
  },
  {
    "planet": "Venus",
    "strength_score": 0.78,
    "reasons": ["own_sign", "dig_bala"],
    "house": 2,
    "rasi": "Taurus",
    "rank": 2
  },
  {
    "planet": "Sun",
    "strength_score": 0.72,
    "reasons": ["dig_bala"],
    "house": 1,
    "rasi": "Leo",
    "rank": 3
  }
]

Example active_yogas JSONB structure:
[
  {
    "yoga_name": "Raj Yoga",
    "description": "Planets in kendras and trikonas",
    "planets_involved": ["Jupiter", "Venus"],
    "houses_involved": [1, 9],
    "strength": "strong",
    "effects": ["wealth", "authority", "prosperity"]
  },
  {
    "yoga_name": "Dhan Yoga",
    "description": "Lords of 2nd and 11th in favorable positions",
    "planets_involved": ["Venus", "Mercury"],
    "houses_involved": [2, 11],
    "strength": "moderate",
    "effects": ["wealth", "material gains"]
  },
  {
    "yoga_name": "Vipreet Raj Yoga",
    "description": "Lords of 6th, 8th, or 12th in kendras",
    "planets_involved": ["Mars"],
    "houses_involved": [6, 1],
    "strength": "moderate",
    "effects": ["transformation", "overcoming obstacles"]
  }
]

Example house_cusps JSONB array:
[45.5, 75.2, 105.8, 135.3, 165.1, 195.6, 225.4, 255.9, 285.7, 315.2, 345.8, 15.3]
Index 0 = House 1 cusp, Index 1 = House 2 cusp, ..., Index 11 = House 12 cusp
*/

-- ----------------------------------------------------------------------------
-- Verification Queries (Run these after migration to verify)
-- ----------------------------------------------------------------------------

-- Verify table was created:
-- SELECT table_name 
-- FROM information_schema.tables 
-- WHERE table_name = 'cosmic_snapshots';

-- Verify columns:
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'cosmic_snapshots'
-- ORDER BY ordinal_position;

-- Verify constraints:
-- SELECT conname, contype, pg_get_constraintdef(oid) as definition
-- FROM pg_constraint
-- WHERE conrelid = 'cosmic_snapshots'::regclass;

-- Verify indexes:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'cosmic_snapshots'
-- ORDER BY indexname;

-- Verify RLS is enabled:
-- SELECT tablename, rowsecurity
-- FROM pg_tables
-- WHERE tablename = 'cosmic_snapshots';

-- ============================================================================
-- End of Migration 008
-- ============================================================================

COMMIT;

