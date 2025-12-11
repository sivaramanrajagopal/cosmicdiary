-- ============================================================================
-- Migration 002: Create Event Chart Data Table
-- ============================================================================
-- 
-- Description:
--   Creates a new table to store complete astrological chart data for each 
--   event. This includes ascendant information, house cusps, planetary 
--   positions with house placements, and planetary strength calculations.
--   Enables precise astrological analysis based on event time and location.
--
-- Date Created: 2025-12-11
-- Author: Cosmic Diary Migration System
--
-- Table Purpose:
--   Stores calculated astrological chart data for events that have both
--   time and location information. One chart per event (1:1 relationship).
--
-- Dependencies:
--   - Requires events table to exist
--   - Requires event to have event_time, timezone, latitude, longitude
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the migration
--   5. Verify the table was created in Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/002_create_event_chart_data_table_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Create Event Chart Data Table
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS event_chart_data (
    -- Primary Key
    id BIGSERIAL PRIMARY KEY,
    
    -- Foreign Key to Events (1:1 relationship - one chart per event)
    event_id BIGINT NOT NULL UNIQUE REFERENCES events(id) ON DELETE CASCADE,
    
    -- ========================================================================
    -- Ascendant Information
    -- ========================================================================
    
    -- Ascendant degree (0-360 degrees)
    ascendant_degree REAL NOT NULL CHECK (ascendant_degree >= 0 AND ascendant_degree < 360),
    
    -- Ascendant Rasi (Zodiac sign)
    ascendant_rasi TEXT NOT NULL,
    ascendant_rasi_number INT NOT NULL CHECK (ascendant_rasi_number BETWEEN 1 AND 12),
    
    -- Ascendant Nakshatra (optional - may not always be calculated)
    ascendant_nakshatra TEXT,
    
    -- Planet ruling the ascendant Rasi
    ascendant_lord TEXT NOT NULL,
    
    -- ========================================================================
    -- House System
    -- ========================================================================
    
    -- House cusps: Array of 12 house cusp degrees [1st, 2nd, ..., 12th]
    -- Each value is the degree of the cusp (0-360)
    house_cusps JSONB NOT NULL,
    
    -- House system used for calculation
    house_system TEXT DEFAULT 'Placidus' CHECK (house_system IN ('Placidus', 'Koch', 'Equal', 'Whole Sign')),
    
    -- ========================================================================
    -- Calculation Details
    -- ========================================================================
    
    -- Julian Day number used for astronomical calculations
    julian_day REAL NOT NULL,
    
    -- Sidereal time at event location (optional)
    sidereal_time REAL,
    
    -- Ayanamsa value used (Lahiri standard)
    ayanamsa REAL NOT NULL,
    
    -- ========================================================================
    -- Planetary Data
    -- ========================================================================
    
    -- Complete planetary positions with house placements
    -- Structure: See example below in comments
    planetary_positions JSONB NOT NULL,
    
    -- Planetary strength calculations
    -- Structure: See example below in comments
    planetary_strengths JSONB,
    
    -- ========================================================================
    -- Timestamps
    -- ========================================================================
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- Table Comments
-- ----------------------------------------------------------------------------

COMMENT ON TABLE event_chart_data IS 
'Stores complete astrological chart calculations for events. One chart per event (1:1 relationship). 
Contains ascendant, house cusps, planetary positions with house placements, and planetary strengths. 
Requires event to have event_time, timezone, latitude, and longitude for accurate calculations.';

COMMENT ON COLUMN event_chart_data.id IS 
'Primary key - unique identifier for each chart record.';

COMMENT ON COLUMN event_chart_data.event_id IS 
'Foreign key to events table. UNIQUE constraint ensures one chart per event. 
Cascades delete when event is removed.';

COMMENT ON COLUMN event_chart_data.ascendant_degree IS 
'Ascendant degree in ecliptic longitude (0-360 degrees). The exact point rising on the eastern horizon at event time and location.';

COMMENT ON COLUMN event_chart_data.ascendant_rasi IS 
'Zodiac sign (Rasi) of the ascendant. Examples: ''Aries'', ''Taurus'', ''Scorpio''.';

COMMENT ON COLUMN event_chart_data.ascendant_rasi_number IS 
'Numerical representation of ascendant Rasi (1=Aries, 2=Taurus, ..., 12=Pisces).';

COMMENT ON COLUMN event_chart_data.ascendant_nakshatra IS 
'Nakshatra (lunar mansion) of the ascendant. Optional field as calculation may vary.';

COMMENT ON COLUMN event_chart_data.ascendant_lord IS 
'Planet ruling the ascendant Rasi. Examples: ''Mars'' (Aries, Scorpio), ''Venus'' (Taurus, Libra).';

COMMENT ON COLUMN event_chart_data.house_cusps IS 
'JSONB array of 12 house cusp degrees. Format: [house1_degree, house2_degree, ..., house12_degree]. 
Each degree is 0-360. Example: [45.5, 75.2, 105.8, ..., 15.3]';

COMMENT ON COLUMN event_chart_data.house_system IS 
'House system used for calculation. Options: ''Placidus'' (default), ''Koch'', ''Equal'', ''Whole Sign''.';

COMMENT ON COLUMN event_chart_data.julian_day IS 
'Julian Day number used for astronomical calculations. Standard reference for date/time in astronomy.';

COMMENT ON COLUMN event_chart_data.sidereal_time IS 
'Sidereal time at event location (optional). Used for house cusp calculations.';

COMMENT ON COLUMN event_chart_data.ayanamsa IS 
'Ayanamsa value used (Lahiri standard). The difference between tropical and sidereal zodiac.';

COMMENT ON COLUMN event_chart_data.planetary_positions IS 
'Complete planetary positions with house placements. JSONB structure with all 9 planets. 
See example structure in migration comments.';

COMMENT ON COLUMN event_chart_data.planetary_strengths IS 
'Planetary strength calculations. Includes exaltation, debilitation, own sign, directional strength, etc. 
See example structure in migration comments.';

COMMENT ON COLUMN event_chart_data.created_at IS 
'Timestamp when chart data was first calculated and stored.';

COMMENT ON COLUMN event_chart_data.updated_at IS 
'Timestamp when chart data was last updated.';

-- ----------------------------------------------------------------------------
-- Create Indexes for Performance
-- ----------------------------------------------------------------------------

-- Index on event_id for fast lookups (foreign key)
CREATE INDEX IF NOT EXISTS idx_chart_data_event 
ON event_chart_data(event_id);

COMMENT ON INDEX idx_chart_data_event IS 
'Index on event_id for fast chart lookups by event. Essential for joining with events table.';

-- Index on ascendant Rasi for filtering by ascendant sign
CREATE INDEX IF NOT EXISTS idx_chart_data_ascendant_rasi 
ON event_chart_data(ascendant_rasi);

COMMENT ON INDEX idx_chart_data_ascendant_rasi IS 
'Index on ascendant_rasi for filtering events by ascendant sign. Useful for astrological analysis.';

-- GIN index on house_cusps for JSONB queries
CREATE INDEX IF NOT EXISTS idx_chart_data_cusps_gin 
ON event_chart_data USING GIN (house_cusps);

COMMENT ON INDEX idx_chart_data_cusps_gin IS 
'GIN index on house_cusps JSONB for efficient queries on house cusp data. Enables fast searches within house cusp arrays.';

-- GIN index on planetary_positions for JSONB queries
CREATE INDEX IF NOT EXISTS idx_chart_data_positions_gin 
ON event_chart_data USING GIN (planetary_positions);

COMMENT ON INDEX idx_chart_data_positions_gin IS 
'GIN index on planetary_positions JSONB for efficient queries on planetary data. Enables fast searches for specific planet positions or house placements.';

-- GIN index on planetary_strengths for JSONB queries
CREATE INDEX IF NOT EXISTS idx_chart_data_strengths_gin 
ON event_chart_data USING GIN (planetary_strengths);

COMMENT ON INDEX idx_chart_data_strengths_gin IS 
'GIN index on planetary_strengths JSONB for efficient queries on planetary strength data. Enables fast searches for specific strength conditions.';

-- Composite index on ascendant Rasi and number for combined queries
CREATE INDEX IF NOT EXISTS idx_chart_data_ascendant_composite 
ON event_chart_data(ascendant_rasi, ascendant_rasi_number);

COMMENT ON INDEX idx_chart_data_ascendant_composite IS 
'Composite index on ascendant_rasi and ascendant_rasi_number for efficient combined queries on ascendant information.';

-- ----------------------------------------------------------------------------
-- Create Trigger for updated_at
-- ----------------------------------------------------------------------------

-- Function to update updated_at timestamp (reuse if exists from main schema)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at
DROP TRIGGER IF EXISTS update_chart_data_updated_at ON event_chart_data;
CREATE TRIGGER update_chart_data_updated_at
    BEFORE UPDATE ON event_chart_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ----------------------------------------------------------------------------
-- Row Level Security (RLS)
-- ----------------------------------------------------------------------------

ALTER TABLE event_chart_data ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations (adjust as needed for your security requirements)
DROP POLICY IF EXISTS "Allow all operations on chart_data" ON event_chart_data;
CREATE POLICY "Allow all operations on chart_data" ON event_chart_data
    FOR ALL USING (true) WITH CHECK (true);

COMMENT ON POLICY "Allow all operations on chart_data" ON event_chart_data IS 
'RLS policy allowing all operations on chart data. Modify based on your security requirements.';

COMMIT;

-- ============================================================================
-- Example Data Structures
-- ============================================================================
--
-- Example planetary_positions JSONB structure:
-- {
--   "Sun": {
--     "longitude": 232.43,
--     "latitude": 0.0,
--     "speed": 1.0,
--     "is_retrograde": false,
--     "rasi": {
--       "name": "Scorpio",
--       "number": 8,
--       "lord": "Mars"
--     },
--     "nakshatra": {
--       "name": "Jyeshta",
--       "number": 18,
--       "pada": 2
--     },
--     "house": 3
--   },
--   "Moon": { ... },
--   "Mercury": { ... },
--   "Venus": { ... },
--   "Mars": { ... },
--   "Jupiter": { ... },
--   "Saturn": { ... },
--   "Rahu": { ... },
--   "Ketu": { ... }
-- }
--
-- Example planetary_strengths JSONB structure:
-- {
--   "Sun": {
--     "exalted": false,
--     "debilitated": false,
--     "own_sign": false,
--     "dig_bala": true,
--     "combusted": false,
--     "strength_score": 0.65
--   },
--   "Moon": { ... },
--   ... all 9 planets
-- }
--
-- Example house_cusps JSONB array:
-- [45.5, 75.2, 105.8, 135.3, 165.1, 195.6, 225.4, 255.9, 285.7, 315.2, 345.8, 15.3]
-- Index 0 = House 1, Index 1 = House 2, ..., Index 11 = House 12
--
-- ============================================================================
-- Verification Queries (Run these after migration to verify)
-- ============================================================================

-- Verify table was created:
-- SELECT table_name 
-- FROM information_schema.tables 
-- WHERE table_name = 'event_chart_data';

-- Verify columns:
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'event_chart_data'
-- ORDER BY ordinal_position;

-- Verify constraints:
-- SELECT conname, contype, pg_get_constraintdef(oid) as definition
-- FROM pg_constraint
-- WHERE conrelid = 'event_chart_data'::regclass;

-- Verify indexes:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'event_chart_data'
-- ORDER BY indexname;

-- Verify foreign key:
-- SELECT
--     tc.constraint_name,
--     tc.table_name,
--     kcu.column_name,
--     ccu.table_name AS foreign_table_name,
--     ccu.column_name AS foreign_column_name
-- FROM information_schema.table_constraints AS tc
-- JOIN information_schema.key_column_usage AS kcu
--     ON tc.constraint_name = kcu.constraint_name
-- JOIN information_schema.constraint_column_usage AS ccu
--     ON ccu.constraint_name = tc.constraint_name
-- WHERE tc.constraint_type = 'FOREIGN KEY'
--     AND tc.table_name = 'event_chart_data';

-- ============================================================================
-- End of Migration 002
-- ============================================================================

