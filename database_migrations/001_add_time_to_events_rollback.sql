-- ============================================================================
-- Rollback Migration 001: Remove Time Fields from Events Table
-- ============================================================================
-- 
-- Description:
--   Removes the time-related fields added in migration 001.
--   Use this only if you need to undo the time fields addition.
--
-- WARNING: This will permanently delete all time-related data!
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
--   5. Verify the changes in the Table Editor
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Drop Indexes First (before dropping columns)
-- ----------------------------------------------------------------------------

DROP INDEX IF EXISTS idx_events_has_accurate_time;
DROP INDEX IF EXISTS idx_events_date_time;
DROP INDEX IF EXISTS idx_events_timezone;
DROP INDEX IF EXISTS idx_events_event_time;

-- ----------------------------------------------------------------------------
-- Remove Columns
-- ----------------------------------------------------------------------------

ALTER TABLE events
DROP COLUMN IF EXISTS has_accurate_time;

ALTER TABLE events
DROP COLUMN IF EXISTS timezone;

ALTER TABLE events
DROP COLUMN IF EXISTS event_time;

COMMIT;

-- ============================================================================
-- Rollback Complete
-- ============================================================================

