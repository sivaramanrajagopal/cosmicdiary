-- ============================================================================
-- Migration 007 Rollback: Remove Astrological Metadata from Events Table
-- ============================================================================
-- 
-- Description:
--   Rollback script for Migration 007. Removes the astrological metadata
--   columns and their indexes from the events table.
--
-- WARNING: This will permanently delete all astrological metadata!
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
--   5. Verify the columns have been removed
--
-- ============================================================================

BEGIN;

-- Drop indexes first
DROP INDEX IF EXISTS idx_events_research_score;
DROP INDEX IF EXISTS idx_events_astro_metadata_gin;
DROP INDEX IF EXISTS idx_events_impact_metrics_gin;
DROP INDEX IF EXISTS idx_events_sources_gin;

-- Drop columns
ALTER TABLE events 
DROP COLUMN IF EXISTS astrological_metadata,
DROP COLUMN IF EXISTS impact_metrics,
DROP COLUMN IF EXISTS research_score,
DROP COLUMN IF EXISTS sources;

COMMIT;

-- ============================================================================
-- End of Rollback
-- ============================================================================

