# Querying House Mappings and Planetary Aspects

## Query Examples for Supabase SQL Editor

### 1. Get All House Mappings with Event Details
```sql
SELECT 
  ehm.id,
  e.id as event_id,
  e.title as event_title,
  e.category,
  e.date as event_date,
  ehm.house_number,
  ehm.rasi_name,
  ehm.house_significations,
  ehm.mapping_reason,
  ehm.created_at
FROM event_house_mappings ehm
JOIN events e ON ehm.event_id = e.id
ORDER BY e.date DESC;
```

### 2. Get All Planetary Aspects for Events
```sql
SELECT 
  epa.id,
  e.id as event_id,
  e.title as event_title,
  e.category,
  e.date as event_date,
  epa.house_number,
  ehm.rasi_name as house_rasi,
  epa.planet_name,
  epa.aspect_type,
  epa.planet_rasi,
  epa.aspect_strength,
  epa.planet_longitude,
  epa.created_at
FROM event_planetary_aspects epa
JOIN events e ON epa.event_id = e.id
LEFT JOIN event_house_mappings ehm ON epa.event_id = ehm.event_id AND epa.house_number = ehm.house_number
ORDER BY e.date DESC, epa.aspect_strength DESC;
```

### 3. Get Complete Event Analysis (House + Aspects + Correlations)
```sql
SELECT 
  e.id as event_id,
  e.title,
  e.category,
  e.date,
  ehm.house_number,
  ehm.rasi_name as house_rasi,
  ehm.house_significations,
  COUNT(DISTINCT epa.id) as aspect_count,
  COUNT(DISTINCT epc.id) as correlation_count,
  STRING_AGG(DISTINCT epa.planet_name, ', ') as aspecting_planets,
  STRING_AGG(DISTINCT epa.aspect_type, ', ') as aspect_types
FROM events e
LEFT JOIN event_house_mappings ehm ON e.id = ehm.event_id
LEFT JOIN event_planetary_aspects epa ON e.id = epa.event_id
LEFT JOIN event_planetary_correlations epc ON e.id = epc.event_id
GROUP BY e.id, e.title, e.category, e.date, ehm.house_number, ehm.rasi_name, ehm.house_significations
ORDER BY e.date DESC;
```

### 4. Find Events with Specific House
```sql
SELECT 
  e.*,
  ehm.house_number,
  ehm.rasi_name,
  ehm.house_significations
FROM events e
JOIN event_house_mappings ehm ON e.id = ehm.event_id
WHERE ehm.house_number = 8  -- 8th house (transformation)
ORDER BY e.date DESC;
```

### 5. Find Events with Mars Aspects
```sql
SELECT 
  e.*,
  epa.aspect_type,
  epa.aspect_strength,
  ehm.house_number,
  ehm.rasi_name as event_house
FROM events e
JOIN event_planetary_aspects epa ON e.id = epa.event_id
JOIN event_house_mappings ehm ON e.id = ehm.event_id
WHERE epa.planet_name = 'Mars'
ORDER BY epa.aspect_strength DESC, e.date DESC;
```

### 6. Find Events with Dustana House Aspects (Rahu/Ketu)
```sql
SELECT 
  e.*,
  epa.planet_name,
  epa.aspect_type,
  ehm.house_number,
  ehm.rasi_name
FROM events e
JOIN event_planetary_aspects epa ON e.id = epa.event_id
JOIN event_house_mappings ehm ON e.id = ehm.event_id
WHERE epa.aspect_type = 'dustana'
  AND epa.planet_name IN ('Rahu', 'Ketu')
ORDER BY e.date DESC;
```

### 7. Count Aspects by Type
```sql
SELECT 
  aspect_type,
  COUNT(*) as count,
  STRING_AGG(DISTINCT planet_name, ', ') as planets
FROM event_planetary_aspects
GROUP BY aspect_type
ORDER BY count DESC;
```

### 8. House Distribution Analysis
```sql
SELECT 
  house_number,
  rasi_name,
  COUNT(*) as event_count,
  STRING_AGG(DISTINCT category, ', ') as categories
FROM event_house_mappings
GROUP BY house_number, rasi_name
ORDER BY house_number;
```

### 9. Events with Strong Planetary Aspects
```sql
SELECT 
  e.title,
  e.category,
  e.date,
  ehm.house_number,
  ehm.rasi_name,
  epa.planet_name,
  epa.aspect_type,
  epa.aspect_strength
FROM events e
JOIN event_house_mappings ehm ON e.id = ehm.event_id
JOIN event_planetary_aspects epa ON e.id = epa.event_id
WHERE epa.aspect_strength = 'strong'
ORDER BY e.date DESC;
```

### 10. Aspect Patterns by Event Category
```sql
SELECT 
  e.category,
  ehm.house_number,
  epa.planet_name,
  epa.aspect_type,
  COUNT(*) as occurrence_count
FROM events e
JOIN event_house_mappings ehm ON e.id = ehm.event_id
JOIN event_planetary_aspects epa ON e.id = epa.event_id
GROUP BY e.category, ehm.house_number, epa.planet_name, epa.aspect_type
ORDER BY occurrence_count DESC;
```

## Quick Checks

### Verify Data Exists
```sql
-- Check house mappings
SELECT COUNT(*) as total_mappings FROM event_house_mappings;

-- Check aspects
SELECT COUNT(*) as total_aspects FROM event_planetary_aspects;

-- Check both for an event
SELECT 
  (SELECT COUNT(*) FROM event_house_mappings WHERE event_id = 1) as mappings,
  (SELECT COUNT(*) FROM event_planetary_aspects WHERE event_id = 1) as aspects;
```

