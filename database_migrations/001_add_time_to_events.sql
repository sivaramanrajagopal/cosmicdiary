-- ============================================================================
-- Migration 001: Add Time Fields to Events Table
-- ============================================================================
-- 
-- Description:
--   Adds time-related fields to the events table to support precise 
--   astrological calculations. This enables calculation of accurate 
--   ascendant and house systems based on event time and location.
--
-- Date Created: 2025-12-11
-- Author: Cosmic Diary Migration System
--
-- Fields Added:
--   - event_time: The time when the event occurred
--   - timezone: Timezone string (e.g., 'Asia/Kolkata', 'America/New_York')
--   - has_accurate_time: Boolean flag indicating if exact time is known
--
-- Impact:
--   - All new fields are nullable to maintain compatibility with existing data
--   - No data loss or breaking changes
--   - Enables future features for accurate astrological chart calculations
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the migration
--   5. Verify the changes in the Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/001_add_time_to_events_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Add Time-Related Columns
-- ----------------------------------------------------------------------------

-- Add event_time column: Stores the time when the event occurred
ALTER TABLE events
ADD COLUMN IF NOT EXISTS event_time TIME;

COMMENT ON COLUMN events.event_time IS 
'Time when the event occurred (HH:MM:SS format). Nullable since many events only have date information. Used for accurate astrological calculations.';

-- Add timezone column: Stores the timezone for the event
ALTER TABLE events
ADD COLUMN IF NOT EXISTS timezone TEXT DEFAULT 'UTC';

COMMENT ON COLUMN events.timezone IS 
'Timezone string in IANA format (e.g., ''Asia/Kolkata'', ''America/New_York'', ''Europe/London''). Defaults to ''UTC'' for global events or when timezone is unknown. Essential for converting event_time to UTC for calculations.';

-- Add has_accurate_time column: Flag indicating time precision
ALTER TABLE events
ADD COLUMN IF NOT EXISTS has_accurate_time BOOLEAN DEFAULT false;

COMMENT ON COLUMN events.has_accurate_time IS 
'Boolean flag indicating whether the event_time is known precisely (true) or estimated/approximate (false). Important for astrological accuracy - exact times enable precise ascendant calculations.';

-- ----------------------------------------------------------------------------
-- Create Indexes for Performance
-- ----------------------------------------------------------------------------

-- Index on event_time for time-based queries
-- Useful for: Finding events at specific times, time range queries
CREATE INDEX IF NOT EXISTS idx_events_event_time 
ON events(event_time)
WHERE event_time IS NOT NULL;

COMMENT ON INDEX idx_events_event_time IS 
'Index on event_time for efficient time-based queries. Partial index only includes rows where event_time is not null.';

-- Index on timezone for timezone filtering
-- Useful for: Filtering events by timezone, regional analysis
CREATE INDEX IF NOT EXISTS idx_events_timezone 
ON events(timezone)
WHERE timezone IS NOT NULL;

COMMENT ON INDEX idx_events_timezone IS 
'Index on timezone for efficient timezone-based filtering and regional event queries. Partial index only includes rows where timezone is not null.';

-- Composite index on date and event_time for temporal queries
-- Useful for: Events on a specific date and time, chronological sorting
CREATE INDEX IF NOT EXISTS idx_events_date_time 
ON events(date, event_time)
WHERE event_time IS NOT NULL;

COMMENT ON INDEX idx_events_date_time IS 
'Composite index on date and event_time for efficient temporal queries and chronological sorting of events with known times.';

-- Index on has_accurate_time for filtering by time precision
-- Useful for: Finding events with precise vs estimated times
CREATE INDEX IF NOT EXISTS idx_events_has_accurate_time 
ON events(has_accurate_time);

COMMENT ON INDEX idx_events_has_accurate_time IS 
'Index on has_accurate_time for filtering events by time precision. Helps identify events suitable for precise astrological calculations.';

-- ----------------------------------------------------------------------------
-- Update Constraints (Optional - for data validation)
-- ----------------------------------------------------------------------------

-- Add check constraint to ensure timezone is valid IANA format (if desired)
-- Note: This is a basic check - full validation would require application-level checks
-- Uncomment if you want strict timezone validation:
-- ALTER TABLE events
-- ADD CONSTRAINT valid_timezone_format 
-- CHECK (timezone IS NULL OR timezone ~ '^[A-Za-z_]+/[A-Za-z_]+$');

-- ----------------------------------------------------------------------------
-- Migration Complete
-- ----------------------------------------------------------------------------

COMMIT;

-- ============================================================================
-- Verification Queries (Run these after migration to verify)
-- ============================================================================

-- Verify columns were added:
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'events'
--   AND column_name IN ('event_time', 'timezone', 'has_accurate_time')
-- ORDER BY ordinal_position;

-- Verify indexes were created:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'events'
--   AND indexname LIKE 'idx_events%time%'
-- ORDER BY indexname;

-- Check existing data (should all be NULL for new columns):
-- SELECT 
--   COUNT(*) as total_events,
--   COUNT(event_time) as events_with_time,
--   COUNT(timezone) as events_with_timezone,
--   COUNT(*) FILTER (WHERE has_accurate_time = true) as events_with_accurate_time
-- FROM events;

-- ============================================================================
-- End of Migration 001
-- ============================================================================

