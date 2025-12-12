-- ============================================================================
-- Rollback Migration 003: Remove Columns from event_house_mappings
-- ============================================================================
-- 
-- Description:
--   Removes the actual_house_number and calculation_method columns
--   added in migration 003.
--
-- WARNING: This will permanently delete all ascendant-based house data!
--          Make sure to backup your data before running this rollback.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Drop Indexes First
-- ----------------------------------------------------------------------------

DROP INDEX IF EXISTS idx_house_mappings_composite;
DROP INDEX IF EXISTS idx_house_mappings_method;
DROP INDEX IF EXISTS idx_house_mappings_actual_house;

-- ----------------------------------------------------------------------------
-- Remove Columns
-- ----------------------------------------------------------------------------

ALTER TABLE event_house_mappings
DROP COLUMN IF EXISTS calculation_method;

ALTER TABLE event_house_mappings
DROP COLUMN IF EXISTS actual_house_number;

COMMIT;

-- ============================================================================
-- Rollback Complete
-- ============================================================================

