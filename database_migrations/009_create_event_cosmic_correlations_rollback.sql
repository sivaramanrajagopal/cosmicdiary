-- ============================================================================
-- Migration 009 Rollback: Drop Event-Cosmic Correlations Table
-- ============================================================================
-- 
-- Description:
--   Rollback script for Migration 009. Drops the event_cosmic_correlations
--   table, its trigger function, and all associated indexes, policies, and
--   constraints.
--
-- WARNING: This will permanently delete all correlation data!
--   Make sure to backup data before running this rollback.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the rollback
--   5. Verify the table has been dropped
--
-- ============================================================================

BEGIN;

-- Drop RLS policies first
DROP POLICY IF EXISTS "Allow all operations on event_cosmic_correlations" ON event_cosmic_correlations;

-- Drop triggers
DROP TRIGGER IF EXISTS trigger_update_correlation_total_matches ON event_cosmic_correlations;

-- Drop trigger function
DROP FUNCTION IF EXISTS update_correlation_total_matches() CASCADE;

-- Drop indexes (will be automatically dropped with table, but explicit for clarity)
DROP INDEX IF EXISTS idx_correlations_event;
DROP INDEX IF EXISTS idx_correlations_snapshot;
DROP INDEX IF EXISTS idx_correlations_score;
DROP INDEX IF EXISTS idx_correlations_event_score;
DROP INDEX IF EXISTS idx_correlations_factors_gin;

-- Drop the table (this will cascade to all dependent objects)
DROP TABLE IF EXISTS event_cosmic_correlations CASCADE;

COMMIT;

-- ============================================================================
-- End of Rollback
-- ============================================================================

