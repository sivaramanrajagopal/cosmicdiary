-- Cosmic Diary Supabase Schema
-- Run this in Supabase SQL Editor

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    location TEXT,
    latitude REAL,
    longitude REAL,
    impact_level TEXT CHECK(impact_level IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
    event_type TEXT CHECK(event_type IN ('world', 'personal')) DEFAULT 'world',
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planetary Data Table
-- Stores daily planetary positions for correlation analysis
CREATE TABLE IF NOT EXISTS planetary_data (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    planetary_data JSONB NOT NULL,
    -- Structure: { planets: [{ name, longitude, latitude, rasi: {number, name, lord}, nakshatra, is_retrograde, ... }] }
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Event-Planetary Correlations Table
-- Stores calculated planetary impact/relevance for each event
CREATE TABLE IF NOT EXISTS event_planetary_correlations (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    planet_name TEXT NOT NULL,
    planet_position JSONB,
    correlation_score REAL NOT NULL CHECK(correlation_score >= 0 AND correlation_score <= 1),
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, planet_name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_impact ON events(impact_level);
CREATE INDEX IF NOT EXISTS idx_planetary_data_date ON planetary_data(date);

-- GIN index for JSONB queries (for planetary data searches)
CREATE INDEX IF NOT EXISTS idx_planetary_data_gin ON planetary_data USING GIN (planetary_data);

-- Indexes for correlations
CREATE INDEX IF NOT EXISTS idx_correlations_event ON event_planetary_correlations(event_id);
CREATE INDEX IF NOT EXISTS idx_correlations_date ON event_planetary_correlations(date);
CREATE INDEX IF NOT EXISTS idx_correlations_planet ON event_planetary_correlations(planet_name);
CREATE INDEX IF NOT EXISTS idx_correlations_score ON event_planetary_correlations(correlation_score);

-- Row Level Security (RLS)
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE planetary_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_planetary_correlations ENABLE ROW LEVEL SECURITY;

-- Policies: Allow all operations (can restrict later if needed)
-- Drop existing policies if they exist, then create them
DROP POLICY IF EXISTS "Allow all operations on events" ON events;
CREATE POLICY "Allow all operations on events" ON events
    FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on planetary_data" ON planetary_data;
CREATE POLICY "Allow all operations on planetary_data" ON planetary_data
    FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on correlations" ON event_planetary_correlations;
CREATE POLICY "Allow all operations on correlations" ON event_planetary_correlations
    FOR ALL USING (true) WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to auto-update updated_at
-- Drop existing triggers if they exist
DROP TRIGGER IF EXISTS update_events_updated_at ON events;
DROP TRIGGER IF EXISTS update_planetary_data_updated_at ON planetary_data;
DROP TRIGGER IF EXISTS update_correlations_updated_at ON event_planetary_correlations;

CREATE TRIGGER update_events_updated_at
    BEFORE UPDATE ON events
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_planetary_data_updated_at
    BEFORE UPDATE ON planetary_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_correlations_updated_at
    BEFORE UPDATE ON event_planetary_correlations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Event House Mappings Table
-- Stores house mapping for each event (Kalapurushan method)
CREATE TABLE IF NOT EXISTS event_house_mappings (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    house_number INT NOT NULL CHECK (house_number BETWEEN 1 AND 12),
    rasi_name TEXT NOT NULL,
    house_significations TEXT[] DEFAULT '{}',
    mapping_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id)
);

-- Event Planetary Aspects Table
-- Stores planetary aspects to event houses (Drishti system)
CREATE TABLE IF NOT EXISTS event_planetary_aspects (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    house_number INT NOT NULL CHECK (house_number BETWEEN 1 AND 12),
    planet_name TEXT NOT NULL,
    aspect_type TEXT NOT NULL CHECK (aspect_type IN (
        'conjunction', 'drishti_3rd', 'drishti_4th', 'drishti_5th', 
        'drishti_7th', 'drishti_8th', 'drishti_9th', 'drishti_10th', 
        'drishti_11th', 'dustana'
    )),
    planet_longitude REAL NOT NULL,
    planet_rasi TEXT NOT NULL,
    aspect_strength TEXT CHECK (aspect_strength IN ('strong', 'moderate', 'weak')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, house_number, planet_name, aspect_type)
);

-- Indexes for house mappings
CREATE INDEX IF NOT EXISTS idx_house_mappings_event ON event_house_mappings(event_id);
CREATE INDEX IF NOT EXISTS idx_house_mappings_house ON event_house_mappings(house_number);
CREATE INDEX IF NOT EXISTS idx_house_mappings_rasi ON event_house_mappings(rasi_name);

-- Indexes for planetary aspects
CREATE INDEX IF NOT EXISTS idx_aspects_event ON event_planetary_aspects(event_id);
CREATE INDEX IF NOT EXISTS idx_aspects_house ON event_planetary_aspects(house_number);
CREATE INDEX IF NOT EXISTS idx_aspects_planet ON event_planetary_aspects(planet_name);
CREATE INDEX IF NOT EXISTS idx_aspects_type ON event_planetary_aspects(aspect_type);

-- RLS for new tables
ALTER TABLE event_house_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_planetary_aspects ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all operations on house_mappings" ON event_house_mappings;
CREATE POLICY "Allow all operations on house_mappings" ON event_house_mappings
    FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on aspects" ON event_planetary_aspects;
CREATE POLICY "Allow all operations on aspects" ON event_planetary_aspects
    FOR ALL USING (true) WITH CHECK (true);

-- Triggers for new tables
DROP TRIGGER IF EXISTS update_house_mappings_updated_at ON event_house_mappings;
CREATE TRIGGER update_house_mappings_updated_at
    BEFORE UPDATE ON event_house_mappings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_aspects_updated_at ON event_planetary_aspects;
CREATE TRIGGER update_aspects_updated_at
    BEFORE UPDATE ON event_planetary_aspects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to ensure planetary data exists for a date
CREATE OR REPLACE FUNCTION ensure_planetary_data(target_date DATE)
RETURNS VOID AS $$
BEGIN
    INSERT INTO planetary_data (date, planetary_data)
    VALUES (target_date, '{"planets": []}'::jsonb)
    ON CONFLICT (date) DO NOTHING;
END;
$$ LANGUAGE plpgsql;
