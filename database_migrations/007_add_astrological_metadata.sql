-- ============================================================================
-- Migration 007: Add Astrological Metadata to Events Table
-- ============================================================================
-- 
-- Description:
--   Adds fields to the events table to store astrological relevance metadata,
--   impact metrics, research scores, and source URLs. These fields enhance
--   event collection for astrological research purposes.
--
-- Date Created: 2025-12-12
-- Author: Cosmic Diary Migration System
--
-- Fields Added:
--   - astrological_metadata: JSONB storing houses, planets, and reasoning
--   - impact_metrics: JSONB storing quantifiable impact data
--   - research_score: REAL (0-100) indicating research worthiness
--   - sources: JSONB array of source URLs
--
-- Impact:
--   - All new fields are nullable to maintain compatibility with existing data
--   - No data loss or breaking changes
--   - Enables research-focused event filtering and analysis
--
-- How to Apply:
--   1. Connect to your Supabase PostgreSQL database
--   2. Open the SQL Editor in Supabase Dashboard
--   3. Copy and paste this entire file
--   4. Execute the migration
--   5. Verify the changes in the Table Editor
--
-- Rollback (if needed):
--   See: database_migrations/007_add_astrological_metadata_rollback.sql
--
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Add Astrological Metadata Columns
-- ----------------------------------------------------------------------------

-- Add astrological_metadata column
ALTER TABLE events 
ADD COLUMN IF NOT EXISTS astrological_metadata JSONB;

COMMENT ON COLUMN events.astrological_metadata IS 
'Stores houses, planets, and reasoning for astrological relevance. Format: {"primary_houses": [1, 8], "primary_planets": ["Mars", "Saturn"], "keywords": ["keyword1", "keyword2"], "reasoning": "Brief explanation why this event is astrologically significant"}';

-- Add impact_metrics column
ALTER TABLE events 
ADD COLUMN IF NOT EXISTS impact_metrics JSONB;

COMMENT ON COLUMN events.impact_metrics IS 
'Quantifiable impact data. Format: {"deaths": 100, "injured": 500, "affected": 10000, "financial_impact_usd": 1000000, "geographic_scope": "national"}. All fields are optional.';

-- Add research_score column
ALTER TABLE events 
ADD COLUMN IF NOT EXISTS research_score REAL CHECK (research_score >= 0 AND research_score <= 100);

COMMENT ON COLUMN events.research_score IS 
'Research worthiness score (0-100). Higher = more valuable for astrological research. Calculated based on impact level, time accuracy, location specificity, astrological clarity, and measurable metrics.';

-- Add sources column
ALTER TABLE events 
ADD COLUMN IF NOT EXISTS sources JSONB DEFAULT '[]'::JSONB;

COMMENT ON COLUMN events.sources IS 
'Array of source URLs for event verification. Format: ["url1", "url2", ...]. Used for tracking where event information was obtained.';

-- ----------------------------------------------------------------------------
-- Create Indexes for Performance
-- ----------------------------------------------------------------------------

-- Index on research_score for querying high-value events
CREATE INDEX IF NOT EXISTS idx_events_research_score 
ON events(research_score DESC)
WHERE research_score IS NOT NULL;

COMMENT ON INDEX idx_events_research_score IS 
'Index on research_score (DESC) for efficient queries filtering high-value events. Partial index only includes rows where research_score is set. Useful for finding top research-worthy events.';

-- GIN index on astrological_metadata for efficient JSONB queries
CREATE INDEX IF NOT EXISTS idx_events_astro_metadata_gin 
ON events USING GIN(astrological_metadata)
WHERE astrological_metadata IS NOT NULL;

COMMENT ON INDEX idx_events_astro_metadata_gin IS 
'GIN index on astrological_metadata JSONB for efficient queries filtering by house numbers, planet names, or keywords. Partial index only includes rows where metadata exists.';

-- GIN index on impact_metrics for efficient JSONB queries
CREATE INDEX IF NOT EXISTS idx_events_impact_metrics_gin 
ON events USING GIN(impact_metrics)
WHERE impact_metrics IS NOT NULL;

COMMENT ON INDEX idx_events_impact_metrics_gin IS 
'GIN index on impact_metrics JSONB for efficient queries filtering by impact data (deaths, affected, financial impact, etc.). Partial index only includes rows where metrics exist.';

-- GIN index on sources array
CREATE INDEX IF NOT EXISTS idx_events_sources_gin 
ON events USING GIN(sources)
WHERE sources IS NOT NULL AND jsonb_array_length(sources) > 0;

COMMENT ON INDEX idx_events_sources_gin IS 
'GIN index on sources JSONB array for efficient queries filtering by source URLs. Partial index only includes rows with sources.';

-- ----------------------------------------------------------------------------
-- Example JSONB Structures (for reference)
-- ----------------------------------------------------------------------------

/*
Example astrological_metadata JSONB structure:
{
  "primary_houses": [4, 8, 12],
  "primary_planets": ["Mars", "Saturn", "Rahu"],
  "keywords": ["earthquake", "natural disaster", "sudden event"],
  "reasoning": "Earthquake relates to House 4 (land), House 8 (sudden events), and House 12 (losses). Mars and Saturn are malefic planets associated with natural disasters. Rahu indicates unexpected calamities."
}

Example impact_metrics JSONB structure:
{
  "deaths": 150,
  "injured": 500,
  "affected": 10000,
  "financial_impact_usd": 50000000,
  "geographic_scope": "national"
}

Example sources JSONB array:
["https://news.example.com/article1", "https://reuters.com/article2"]
*/

-- ----------------------------------------------------------------------------
-- Verification Queries (Run these after migration to verify)
-- ----------------------------------------------------------------------------

-- Verify columns were added:
-- SELECT column_name, data_type, is_nullable, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'events' 
--   AND column_name IN ('astrological_metadata', 'impact_metrics', 'research_score', 'sources');

-- Verify indexes were created:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'events'
--   AND indexname IN ('idx_events_research_score', 'idx_events_astro_metadata_gin', 'idx_events_impact_metrics_gin', 'idx_events_sources_gin');

-- Verify constraints:
-- SELECT conname, contype, pg_get_constraintdef(oid) as definition
-- FROM pg_constraint
-- WHERE conrelid = 'events'::regclass
--   AND conname LIKE '%research_score%';

-- ============================================================================
-- End of Migration 007
-- ============================================================================

COMMIT;

