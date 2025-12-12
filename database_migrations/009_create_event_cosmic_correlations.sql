-- ============================================================================
-- Migration 009: Create Event-Cosmic Snapshot Correlations Table
-- ============================================================================
-- 
-- Description:
--   Creates a junction table to store correlation analysis between individual
--   events and cosmic snapshots. This enables identifying which planetary
--   states (captured every 2 hours) correlate most strongly with specific
--   events, revealing astrological patterns and timing influences.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- Purpose:
--   - Link events with relevant cosmic snapshots
--   - Store correlation scores and matching patterns
--   - Enable queries to find events correlated with specific planetary states
--   - Support temporal correlation analysis (events vs. planetary snapshots)
--
-- Relationships:
--   - Many-to-Many: Events can correlate with multiple snapshots
--   - Many-to-Many: Snapshots can correlate with multiple events
--   - One correlation record per event-snapshot pair (UNIQUE constraint)
--
-- How to Apply:
--   1. Ensure Migration 008 (cosmic_snapshots table) has been applied
--   2. Connect to your Supabase PostgreSQL database
--   3. Open the SQL Editor in Supabase Dashboard
--   4. Copy and paste this entire file
--   5. Execute the migration
--   6. Verify the new table and its structure in the Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/009_create_event_cosmic_correlations_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Create event_cosmic_correlations Table
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS event_cosmic_correlations (
    id BIGSERIAL PRIMARY KEY,
    
    -- Foreign Keys
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    snapshot_id BIGINT NOT NULL REFERENCES cosmic_snapshots(id) ON DELETE CASCADE,
    
    -- Correlation Analysis
    correlation_score REAL NOT NULL CHECK (correlation_score >= 0 AND correlation_score <= 1),
    matching_factors JSONB NOT NULL DEFAULT '[]'::JSONB, -- Array of matching patterns
    total_matches INT DEFAULT 0 CHECK (total_matches >= 0),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Unique constraint: one correlation per event-snapshot pair
    UNIQUE(event_id, snapshot_id)
);

COMMENT ON TABLE event_cosmic_correlations IS 
'Junction table storing correlation analysis between events and cosmic snapshots. Each row represents a correlation match between a specific event and a planetary state snapshot, including correlation score and detailed matching factors. Enables pattern recognition between events and planetary influences.';

COMMENT ON COLUMN event_cosmic_correlations.event_id IS 
'Foreign key to the events table. Links this correlation to a specific event. CASCADE delete ensures correlations are removed when events are deleted.';

COMMENT ON COLUMN event_cosmic_correlations.snapshot_id IS 
'Foreign key to the cosmic_snapshots table. Links this correlation to a specific planetary state snapshot. CASCADE delete ensures correlations are removed when snapshots are deleted.';

COMMENT ON COLUMN event_cosmic_correlations.correlation_score IS 
'Overall correlation strength between the event and cosmic snapshot, ranging from 0.0 (no correlation) to 1.0 (perfect correlation). Calculated from matching_factors.';

COMMENT ON COLUMN event_cosmic_correlations.matching_factors IS 
'JSONB array of all matching patterns found between the event and snapshot. Each factor includes type, description, significance level, and individual score. See example structure below.';

COMMENT ON COLUMN event_cosmic_correlations.total_matches IS 
'Count of matching factors found. Automatically calculated as the length of the matching_factors array. Useful for quick filtering without parsing JSONB.';

COMMENT ON COLUMN event_cosmic_correlations.created_at IS 
'Timestamp when this correlation was created/calculated. Used for tracking when correlations were identified.';

-- ----------------------------------------------------------------------------
-- Indexes for Performance
-- ----------------------------------------------------------------------------

-- Index on event_id for finding all correlations for a specific event
CREATE INDEX IF NOT EXISTS idx_correlations_event 
ON event_cosmic_correlations(event_id);

COMMENT ON INDEX idx_correlations_event IS 
'Index on event_id for efficient queries finding all cosmic snapshots correlated with a specific event.';

-- Index on snapshot_id for finding all events correlated with a specific snapshot
CREATE INDEX IF NOT EXISTS idx_correlations_snapshot 
ON event_cosmic_correlations(snapshot_id);

COMMENT ON INDEX idx_correlations_snapshot IS 
'Index on snapshot_id for efficient queries finding all events correlated with a specific planetary state snapshot.';

-- Index on correlation_score for filtering by correlation strength
CREATE INDEX IF NOT EXISTS idx_correlations_score 
ON event_cosmic_correlations(correlation_score DESC);

COMMENT ON INDEX idx_correlations_score IS 
'Index on correlation_score (DESC) for efficient queries filtering high-correlation matches. Optimizes queries like "find events with correlation > 0.7".';

-- Composite index on event_id and score for event-specific high correlations
CREATE INDEX IF NOT EXISTS idx_correlations_event_score 
ON event_cosmic_correlations(event_id, correlation_score DESC);

COMMENT ON INDEX idx_correlations_event_score IS 
'Composite index on event_id and correlation_score for efficient queries finding top correlations for specific events.';

-- GIN index on matching_factors for efficient JSONB queries
CREATE INDEX IF NOT EXISTS idx_correlations_factors_gin 
ON event_cosmic_correlations USING GIN (matching_factors);

COMMENT ON INDEX idx_correlations_factors_gin IS 
'GIN index on matching_factors JSONB for efficient queries filtering by matching factor types or descriptions. Enables searches like "find correlations with lagna_match factors".';

-- ----------------------------------------------------------------------------
-- Row Level Security (RLS)
-- ----------------------------------------------------------------------------

ALTER TABLE event_cosmic_correlations ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations on event_cosmic_correlations (can be restricted later)
DROP POLICY IF EXISTS "Allow all operations on event_cosmic_correlations" ON event_cosmic_correlations;
CREATE POLICY "Allow all operations on event_cosmic_correlations" ON event_cosmic_correlations
    FOR ALL USING (true) WITH CHECK (true);

-- ----------------------------------------------------------------------------
-- Trigger Function: Auto-update total_matches from matching_factors
-- ----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_correlation_total_matches()
RETURNS TRIGGER AS $$
BEGIN
    -- Update total_matches based on array length of matching_factors
    NEW.total_matches := jsonb_array_length(NEW.matching_factors);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION update_correlation_total_matches() IS 
'Trigger function that automatically updates total_matches column based on the length of matching_factors JSONB array. Ensures total_matches always reflects the actual number of factors.';

-- Create trigger to auto-update total_matches
DROP TRIGGER IF EXISTS trigger_update_correlation_total_matches ON event_cosmic_correlations;
CREATE TRIGGER trigger_update_correlation_total_matches
    BEFORE INSERT OR UPDATE ON event_cosmic_correlations
    FOR EACH ROW
    EXECUTE FUNCTION update_correlation_total_matches();

COMMENT ON TRIGGER trigger_update_correlation_total_matches ON event_cosmic_correlations IS 
'Automatically updates total_matches column whenever matching_factors is inserted or updated, ensuring consistency.';

-- ----------------------------------------------------------------------------
-- Example JSONB Structure for matching_factors (for reference)
-- ----------------------------------------------------------------------------

/*
Example matching_factors JSONB structure:

[
  {
    "type": "lagna_match",
    "description": "Both event chart and snapshot have Lagna in Scorpio",
    "significance": "Very High",
    "score": 0.3,
    "details": {
      "event_lagna": "Scorpio",
      "snapshot_lagna": "Scorpio",
      "lagna_degree_diff": 2.5
    }
  },
  {
    "type": "retrograde_match",
    "description": "Saturn retrograde in both charts",
    "significance": "High",
    "score": 0.15,
    "details": {
      "planet": "Saturn",
      "event_retrograde": true,
      "snapshot_retrograde": true
    }
  },
  {
    "type": "planetary_house_match",
    "description": "Jupiter in 9th house in both charts",
    "significance": "High",
    "score": 0.2,
    "details": {
      "planet": "Jupiter",
      "house": 9,
      "event_house": 9,
      "snapshot_house": 9
    }
  },
  {
    "type": "nakshatra_match",
    "description": "Moon in same Nakshatra (Punarvasu)",
    "significance": "Moderate",
    "score": 0.1,
    "details": {
      "planet": "Moon",
      "nakshatra": "Punarvasu",
      "event_nakshatra": "Punarvasu",
      "snapshot_nakshatra": "Punarvasu"
    }
  },
  {
    "type": "aspect_match",
    "description": "Mars aspects 8th house in both charts",
    "significance": "High",
    "score": 0.15,
    "details": {
      "planet": "Mars",
      "aspect_type": "drishti_8th",
      "target_house": 8,
      "event_aspects": ["8th"],
      "snapshot_aspects": ["8th"]
    }
  },
  {
    "type": "yoga_match",
    "description": "Raj Yoga active in both charts",
    "significance": "Very High",
    "score": 0.25,
    "details": {
      "yoga_name": "Raj Yoga",
      "event_yoga": true,
      "snapshot_yoga": true,
      "planets_involved": ["Jupiter", "Venus"]
    }
  },
  {
    "type": "tithi_match",
    "description": "Same Tithi in both charts",
    "significance": "Moderate",
    "score": 0.05,
    "details": {
      "tithi": "Shukla Paksha Panchami",
      "event_tithi": "Shukla Paksha Panchami",
      "snapshot_tithi": "Shukla Paksha Panchami"
    }
  },
  {
    "type": "dustana_match",
    "description": "Multiple planets in Dustana houses (6, 8, 12) in both",
    "significance": "High",
    "score": 0.2,
    "details": {
      "event_dustana_planets": ["Saturn", "Rahu"],
      "snapshot_dustana_planets": ["Saturn", "Rahu"],
      "common_dustana_planets": ["Saturn", "Rahu"]
    }
  }
]

Note: The correlation_score is typically the sum of all individual factor scores,
normalized to 0-1 range. In this example:
- Sum of scores: 0.3 + 0.15 + 0.2 + 0.1 + 0.15 + 0.25 + 0.05 + 0.2 = 1.4
- Normalized score (if max possible is 2.0): 1.4 / 2.0 = 0.7
- Or capped at 1.0: min(1.4, 1.0) = 1.0

Factor Types:
- lagna_match: Matching ascendant sign
- retrograde_match: Same planets retrograde
- planetary_house_match: Same planets in same houses
- planetary_rasi_match: Same planets in same rasis
- nakshatra_match: Same planets in same nakshatras
- aspect_match: Similar planetary aspects active
- yoga_match: Same yogas active
- tithi_match: Same lunar day
- dustana_match: Similar dustana house placements
- dominant_planet_match: Same dominant planets
*/

-- ----------------------------------------------------------------------------
-- Verification Queries (Run these after migration to verify)
-- ----------------------------------------------------------------------------

-- Verify table was created:
-- SELECT table_name 
-- FROM information_schema.tables 
-- WHERE table_name = 'event_cosmic_correlations';

-- Verify columns:
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'event_cosmic_correlations'
-- ORDER BY ordinal_position;

-- Verify constraints:
-- SELECT conname, contype, pg_get_constraintdef(oid) as definition
-- FROM pg_constraint
-- WHERE conrelid = 'event_cosmic_correlations'::regclass;

-- Verify foreign keys:
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
--     AND tc.table_name = 'event_cosmic_correlations';

-- Verify indexes:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'event_cosmic_correlations'
-- ORDER BY indexname;

-- Verify RLS is enabled:
-- SELECT tablename, rowsecurity
-- FROM pg_tables
-- WHERE tablename = 'event_cosmic_correlations';

-- Verify trigger exists:
-- SELECT trigger_name, event_manipulation, action_statement
-- FROM information_schema.triggers
-- WHERE event_object_table = 'event_cosmic_correlations';

-- ----------------------------------------------------------------------------
-- Sample Queries for Correlation Analysis
-- ----------------------------------------------------------------------------

/*
-- Query 1: Find events with high correlation scores (> 0.7)
SELECT 
    e.id AS event_id,
    e.title,
    e.date AS event_date,
    cs.snapshot_time,
    ecc.correlation_score,
    ecc.total_matches,
    ecc.matching_factors
FROM event_cosmic_correlations ecc
JOIN events e ON ecc.event_id = e.id
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE ecc.correlation_score > 0.7
ORDER BY ecc.correlation_score DESC
LIMIT 20;

-- Query 2: Find all correlations for a specific event
SELECT 
    cs.snapshot_time,
    cs.lagna_rasi,
    ecc.correlation_score,
    ecc.total_matches,
    jsonb_array_length(ecc.matching_factors) AS factor_count
FROM event_cosmic_correlations ecc
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE ecc.event_id = 1  -- Replace with actual event_id
ORDER BY ecc.correlation_score DESC;

-- Query 3: Find events correlated with a specific snapshot
SELECT 
    e.id,
    e.title,
    e.date,
    e.category,
    ecc.correlation_score,
    ecc.matching_factors
FROM event_cosmic_correlations ecc
JOIN events e ON ecc.event_id = e.id
WHERE ecc.snapshot_id = 1  -- Replace with actual snapshot_id
ORDER BY ecc.correlation_score DESC;

-- Query 4: Count correlations by factor type
SELECT 
    factor->>'type' AS factor_type,
    COUNT(*) AS occurrence_count,
    AVG((factor->>'score')::REAL) AS avg_score
FROM event_cosmic_correlations,
     jsonb_array_elements(matching_factors) AS factor
GROUP BY factor->>'type'
ORDER BY occurrence_count DESC;

-- Query 5: Top matching events for a specific snapshot with factor breakdown
SELECT 
    e.title,
    e.category,
    ecc.correlation_score,
    ecc.total_matches,
    jsonb_pretty(ecc.matching_factors) AS factors
FROM event_cosmic_correlations ecc
JOIN events e ON ecc.event_id = e.id
WHERE ecc.snapshot_id = 1  -- Replace with actual snapshot_id
  AND ecc.correlation_score > 0.5
ORDER BY ecc.correlation_score DESC
LIMIT 10;

-- Query 6: Find snapshots with multiple high-correlation events
SELECT 
    cs.snapshot_time,
    cs.lagna_rasi,
    COUNT(*) AS event_count,
    AVG(ecc.correlation_score) AS avg_correlation,
    MAX(ecc.correlation_score) AS max_correlation
FROM event_cosmic_correlations ecc
JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE ecc.correlation_score > 0.6
GROUP BY cs.id, cs.snapshot_time, cs.lagna_rasi
HAVING COUNT(*) >= 3
ORDER BY event_count DESC, avg_correlation DESC;
*/

-- ============================================================================
-- End of Migration 009
-- ============================================================================

COMMIT;

