# Queries to View Stored Events in Supabase

## Quick Queries for Your Recent Collection

### 1. View All Recent Events (Latest First)
```sql
SELECT 
    id,
    title,
    date,
    category,
    location,
    impact_level,
    event_time,
    timezone,
    created_at
FROM events
WHERE date >= '2025-12-13'
ORDER BY created_at DESC;
```

### 2. View Events with Full Details
```sql
SELECT 
    e.id,
    e.title,
    e.date,
    e.event_time,
    e.timezone,
    e.category,
    e.location,
    e.latitude,
    e.longitude,
    e.impact_level,
    e.description,
    e.astrological_metadata,
    e.research_score,
    e.created_at
FROM events e
WHERE date >= '2025-12-13'
ORDER BY e.created_at DESC
LIMIT 20;
```

### 3. View Events with Chart Data
```sql
SELECT 
    e.id,
    e.title,
    e.date,
    e.location,
    ecd.ascendant_rasi,
    ecd.ascendant_rasi_number,
    ecd.ascendant_lord,
    ecd.house_system,
    ecd.ayanamsa,
    jsonb_object_keys(ecd.planetary_positions) as planets_in_chart
FROM events e
LEFT JOIN event_chart_data ecd ON e.id = ecd.event_id
WHERE e.date >= '2025-12-13'
ORDER BY e.created_at DESC;
```

### 4. View Events with Correlation Scores
```sql
SELECT 
    e.id,
    e.title,
    e.date,
    e.location,
    ecc.correlation_score,
    ecc.total_matches,
    ecc.matching_factors,
    ecc.created_at as correlation_created_at
FROM events e
LEFT JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
WHERE e.date >= '2025-12-13'
ORDER BY ecc.correlation_score DESC, e.created_at DESC;
```

### 5. View All Correlation Details
```sql
SELECT 
    ecc.id,
    ecc.event_id,
    e.title as event_title,
    ecc.snapshot_id,
    ecc.correlation_score,
    ecc.total_matches,
    ecc.matching_factors,
    ecc.created_at
FROM event_cosmic_correlations ecc
JOIN events e ON ecc.event_id = e.id
WHERE e.date >= '2025-12-13'
ORDER BY ecc.correlation_score DESC;
```

### 6. View Your Specific Events (IDs 53-57)
```sql
SELECT 
    e.id,
    e.title,
    e.date,
    e.event_time,
    e.location,
    e.category,
    e.impact_level,
    ecd.ascendant_rasi,
    ecc.correlation_score,
    ecc.total_matches,
    e.created_at
FROM events e
LEFT JOIN event_chart_data ecd ON e.id = ecd.event_id
LEFT JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
WHERE e.id IN (53, 54, 55, 56, 57)
ORDER BY e.id;
```

### 7. View Cosmic Snapshots (to see which snapshot events were correlated with)
```sql
SELECT 
    cs.id,
    cs.snapshot_time,
    cs.lagna_rasi,
    cs.lagna_rasi_number,
    cs.reference_location->>'name' as reference_location,
    cs.created_at
FROM cosmic_snapshots cs
WHERE cs.snapshot_time >= '2025-12-12 19:55:33'::timestamptz
ORDER BY cs.created_at DESC
LIMIT 5;
```

### 8. Complete View: Events + Charts + Correlations + Snapshot
```sql
SELECT 
    e.id as event_id,
    e.title,
    e.date,
    e.event_time,
    e.location,
    e.category,
    e.impact_level,
    ecd.ascendant_rasi,
    ecd.ascendant_rasi_number,
    ecd.ascendant_lord,
    ecc.correlation_score,
    ecc.total_matches,
    ecc.matching_factors,
    cs.lagna_rasi as snapshot_lagna,
    e.created_at as event_created
FROM events e
LEFT JOIN event_chart_data ecd ON e.id = ecd.event_id
LEFT JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id
LEFT JOIN cosmic_snapshots cs ON ecc.snapshot_id = cs.id
WHERE e.date >= '2025-12-13'
ORDER BY e.created_at DESC;
```

## Count Queries

### Count Total Events
```sql
SELECT COUNT(*) as total_events FROM events;
```

### Count Events by Date
```sql
SELECT date, COUNT(*) as event_count
FROM events
GROUP BY date
ORDER BY date DESC;
```

### Count Events with Correlations
```sql
SELECT 
    COUNT(DISTINCT e.id) as events_with_correlations
FROM events e
JOIN event_cosmic_correlations ecc ON e.id = ecc.event_id;
```

### Count Events with Chart Data
```sql
SELECT 
    COUNT(DISTINCT e.id) as events_with_charts
FROM events e
JOIN event_chart_data ecd ON e.id = ecd.event_id;
```

## How to Run These Queries

1. **In Supabase Dashboard:**
   - Go to your Supabase project
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"
   - Paste any of the queries above
   - Click "Run" or press `Cmd/Ctrl + Enter`

2. **Via psql (if you have access):**
   ```bash
   psql "postgresql://postgres:[YOUR-PASSWORD]@[YOUR-PROJECT].supabase.co:5432/postgres"
   ```
   Then paste the query.

