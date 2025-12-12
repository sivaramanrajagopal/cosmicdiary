-- ============================================================================
-- Migration 003: Update event_house_mappings Table
-- ============================================================================
-- 
-- Description:
--   Adds columns to event_house_mappings table to support both
--   Kalapurushan (fixed sign-based) and ascendant-based house systems.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- Changes:
--   - Add actual_house_number: House number from ascendant-based calculation
--   - Add calculation_method: Indicates which method was used
--
-- Impact:
--   - All new fields are nullable to maintain compatibility with existing data
--   - Existing records will have calculation_method = 'kalapurushan'
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the migration
--   5. Verify the changes in the Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/003_update_house_mappings_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Add New Columns
-- ----------------------------------------------------------------------------

-- Add actual_house_number column: House number from ascendant-based calculation
ALTER TABLE event_house_mappings
ADD COLUMN IF NOT EXISTS actual_house_number INT CHECK (actual_house_number BETWEEN 1 AND 12);

COMMENT ON COLUMN event_house_mappings.actual_house_number IS 
'House number calculated using ascendant-based house system (1-12). 
This is the actual house where the event occurred based on event time and location.
NULL if ascendant-based calculation not yet performed.';

-- Add calculation_method column: Indicates which calculation method was used
ALTER TABLE event_house_mappings
ADD COLUMN IF NOT EXISTS calculation_method TEXT 
CHECK (calculation_method IN ('kalapurushan', 'ascendant-based'))
DEFAULT 'kalapurushan';

COMMENT ON COLUMN event_house_mappings.calculation_method IS 
'Method used for house calculation:
- ''kalapurushan'': Fixed sign-based (Aries=1, Taurus=2, etc.) - default for existing records
- ''ascendant-based'': Actual ascendant-based house system using event time and location';

-- ----------------------------------------------------------------------------
-- Update Existing Records
-- ----------------------------------------------------------------------------

-- Set calculation_method for existing records (default to kalapurushan)
UPDATE event_house_mappings
SET calculation_method = 'kalapurushan'
WHERE calculation_method IS NULL;

-- ----------------------------------------------------------------------------
-- Create Indexes
-- ----------------------------------------------------------------------------

-- Index on actual_house_number for filtering by ascendant-based houses
CREATE INDEX IF NOT EXISTS idx_house_mappings_actual_house 
ON event_house_mappings(actual_house_number)
WHERE actual_house_number IS NOT NULL;

COMMENT ON INDEX idx_house_mappings_actual_house IS 
'Index on actual_house_number for efficient queries on ascendant-based house assignments. 
Partial index only includes rows where actual_house_number is set.';

-- Index on calculation_method for filtering by method
CREATE INDEX IF NOT EXISTS idx_house_mappings_method 
ON event_house_mappings(calculation_method);

COMMENT ON INDEX idx_house_mappings_method IS 
'Index on calculation_method for filtering events by calculation method used.';

-- Composite index on both house numbers for comparison queries
CREATE INDEX IF NOT EXISTS idx_house_mappings_composite 
ON event_house_mappings(house_number, actual_house_number)
WHERE actual_house_number IS NOT NULL;

COMMENT ON INDEX idx_house_mappings_composite IS 
'Composite index on house_number (kalapurushan) and actual_house_number (ascendant-based) 
for comparing house assignments between the two methods.';

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
-- WHERE table_name = 'event_house_mappings'
--   AND column_name IN ('actual_house_number', 'calculation_method')
-- ORDER BY ordinal_position;

-- Check existing data (should all be 'kalapurushan'):
-- SELECT calculation_method, COUNT(*) as count
-- FROM event_house_mappings
-- GROUP BY calculation_method;

-- Check for records with actual_house_number:
-- SELECT 
--   COUNT(*) as total,
--   COUNT(actual_house_number) as with_actual_house,
--   COUNT(*) FILTER (WHERE calculation_method = 'ascendant-based') as ascendant_based
-- FROM event_house_mappings;

-- ============================================================================
-- End of Migration 003
-- ============================================================================

