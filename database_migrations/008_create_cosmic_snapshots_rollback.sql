-- ============================================================================
-- Migration 008 Rollback: Drop Cosmic Snapshots Table
-- ============================================================================
-- 
-- Description:
--   Rollback script for Migration 008. Drops the cosmic_snapshots table
--   and all associated indexes, policies, and constraints.
--
-- WARNING: This will permanently delete all cosmic snapshot data!
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
DROP POLICY IF EXISTS "Allow all operations on cosmic_snapshots" ON cosmic_snapshots;

-- Drop indexes (will be automatically dropped with table, but explicit for clarity)
DROP INDEX IF EXISTS idx_cosmic_snapshots_time;
DROP INDEX IF EXISTS idx_cosmic_snapshots_lagna;
DROP INDEX IF EXISTS idx_cosmic_snapshots_time_lagna;
DROP INDEX IF EXISTS idx_cosmic_snapshots_positions_gin;
DROP INDEX IF EXISTS idx_cosmic_snapshots_aspects_gin;
DROP INDEX IF EXISTS idx_cosmic_snapshots_retrograde;

-- Drop the table (this will cascade to all dependent objects)
DROP TABLE IF EXISTS cosmic_snapshots CASCADE;

COMMIT;

-- ============================================================================
-- End of Rollback
-- ============================================================================

