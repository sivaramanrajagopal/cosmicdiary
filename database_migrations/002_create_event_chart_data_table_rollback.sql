-- ============================================================================
-- Rollback Migration 002: Drop Event Chart Data Table
-- ============================================================================
-- 
-- Description:
--   Removes the event_chart_data table created in migration 002.
--   Use this only if you need to undo the chart data table creation.
--
-- WARNING: This will permanently delete all chart data!
--          Make sure to backup your data before running this rollback.
--
-- Date Created: 2025-12-11
-- Author: Cosmic Diary Migration System
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the rollback
--   5. Verify the table was removed in Table Editor
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Drop Triggers First
-- ----------------------------------------------------------------------------

DROP TRIGGER IF EXISTS update_chart_data_updated_at ON event_chart_data;

-- ----------------------------------------------------------------------------
-- Drop Indexes
-- ----------------------------------------------------------------------------

DROP INDEX IF EXISTS idx_chart_data_ascendant_composite;
DROP INDEX IF EXISTS idx_chart_data_strengths_gin;
DROP INDEX IF EXISTS idx_chart_data_positions_gin;
DROP INDEX IF EXISTS idx_chart_data_cusps_gin;
DROP INDEX IF EXISTS idx_chart_data_ascendant_rasi;
DROP INDEX IF EXISTS idx_chart_data_event;

-- ----------------------------------------------------------------------------
-- Drop Policies
-- ----------------------------------------------------------------------------

DROP POLICY IF EXISTS "Allow all operations on chart_data" ON event_chart_data;

-- ----------------------------------------------------------------------------
-- Drop Table
-- ----------------------------------------------------------------------------

DROP TABLE IF EXISTS event_chart_data;

-- Note: update_updated_at_column() function is not dropped as it may be
-- used by other tables. If you want to drop it, uncomment:
-- DROP FUNCTION IF EXISTS update_updated_at_column();

COMMIT;

-- ============================================================================
-- Rollback Complete
-- ============================================================================

