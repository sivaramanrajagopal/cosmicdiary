-- Migration 010: Add sources column to events table
-- This stores URLs to news articles/sources where events were found

-- Add sources column as JSONB array
ALTER TABLE events
ADD COLUMN IF NOT EXISTS sources JSONB DEFAULT '[]'::jsonb;

-- Add comment
COMMENT ON COLUMN events.sources IS 'Array of source URLs/news sources where this event was found. Stored as JSONB array of strings. Example: ["https://example.com/news1", "https://example.com/news2"]';

-- Create GIN index for efficient JSONB searches
CREATE INDEX IF NOT EXISTS idx_events_sources_gin ON events USING GIN (sources);

-- Verify the column was added
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'sources'
    ) THEN
        RAISE NOTICE 'Column sources added successfully to events table';
    ELSE
        RAISE EXCEPTION 'Failed to add sources column';
    END IF;
END $$;

