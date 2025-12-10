# Querying Planetary Data from Supabase

Your planetary data is stored correctly! Here are useful queries you can run in Supabase SQL Editor.

## ✅ Current Storage Structure

The data is stored in `planetary_data` table with this structure:
```json
{
  "planets": [
    {
      "name": "Sun",
      "longitude": 232.43,
      "latitude": 0,
      "is_retrograde": false,
      "nakshatra": 18,
      "rasi": {
        "name": "Scorpio",
        "number": 8,
        "lord": {
          "name": "Mars"
        }
      }
    }
  ]
}
```

## 📊 Useful Queries

### 1. Get all planetary data
```sql
SELECT * FROM planetary_data
ORDER BY date DESC;
```

### 2. Get planetary data for a specific date
```sql
SELECT * FROM planetary_data
WHERE date = '2025-12-10';
```

### 3. Get specific planet positions for a date
```sql
SELECT 
  date,
  planetary_data->'planets'->0 as sun_position,
  planetary_data->'planets'->1 as moon_position
FROM planetary_data
WHERE date = '2025-12-10';
```

### 4. Find all retrograde planets for a date
```sql
SELECT 
  date,
  jsonb_array_elements(planetary_data->'planets') as planet
FROM planetary_data
WHERE date = '2025-12-10'
  AND (jsonb_array_elements(planetary_data->'planets')->>'is_retrograde')::boolean = true;
```

### 5. Find planets in a specific Rasi
```sql
SELECT 
  date,
  jsonb_array_elements(planetary_data->'planets')->>'name' as planet_name,
  jsonb_array_elements(planetary_data->'planets')->'rasi'->>'name' as rasi_name
FROM planetary_data
WHERE date = '2025-12-10'
  AND jsonb_array_elements(planetary_data->'planets')->'rasi'->>'name' = 'Scorpio';
```

### 6. Count planets in each Rasi for a date
```sql
SELECT 
  planetary_data->'planets'->jsonb_array_elements->'rasi'->>'name' as rasi,
  COUNT(*) as planet_count
FROM planetary_data,
  jsonb_array_elements(planetary_data->'planets')
WHERE date = '2025-12-10'
GROUP BY rasi
ORDER BY planet_count DESC;
```

### 7. Get date range with planetary data
```sql
SELECT 
  date,
  jsonb_array_length(planetary_data->'planets') as planet_count
FROM planetary_data
WHERE date BETWEEN '2025-12-08' AND '2025-12-11'
ORDER BY date;
```

### 8. Find dates with retrograde planets
```sql
SELECT DISTINCT
  date,
  COUNT(*) FILTER (WHERE (planet->>'is_retrograde')::boolean = true) as retrograde_count
FROM planetary_data,
  jsonb_array_elements(planetary_data->'planets') as planet
GROUP BY date
HAVING COUNT(*) FILTER (WHERE (planet->>'is_retrograde')::boolean = true) > 0
ORDER BY date DESC;
```

### 9. Get Sun's position over time
```sql
SELECT 
  date,
  planetary_data->'planets'->0->>'name' as planet,
  planetary_data->'planets'->0->'rasi'->>'name' as rasi,
  (planetary_data->'planets'->0->>'longitude')::float as longitude
FROM planetary_data
WHERE planetary_data->'planets'->0->>'name' = 'Sun'
ORDER BY date DESC
LIMIT 10;
```

### 10. Validate data structure
```sql
-- Check if all records have 9 planets
SELECT 
  date,
  jsonb_array_length(planetary_data->'planets') as planet_count
FROM planetary_data
WHERE jsonb_array_length(planetary_data->'planets') != 9;
```

## 🔍 Data Validation

### Check for missing required fields
```sql
SELECT 
  date,
  planetary_data->'planets'->0->>'name' as has_name,
  planetary_data->'planets'->0->>'longitude' as has_longitude,
  planetary_data->'planets'->0->'rasi'->>'name' as has_rasi
FROM planetary_data
WHERE planetary_data->'planets'->0->>'name' IS NULL
   OR planetary_data->'planets'->0->>'longitude' IS NULL
   OR planetary_data->'planets'->0->'rasi'->>'name' IS NULL;
```

### Verify retrograde data
```sql
SELECT 
  date,
  jsonb_array_elements(planetary_data->'planets')->>'name' as planet,
  jsonb_array_elements(planetary_data->'planets')->>'is_retrograde' as is_retrograde
FROM planetary_data
WHERE date = '2025-12-10';
```

## 💡 Best Practices

1. **Use JSONB operators** (`->`, `->>`, `#>`, `#>>`) for efficient queries
2. **Index is already created** - GIN index on `planetary_data` for fast searches
3. **Date is indexed** - Fast date-based queries
4. **UNIQUE constraint** on date prevents duplicates

## 🚀 Performance Tips

- The GIN index on `planetary_data` makes JSONB queries fast
- Date index makes date-range queries efficient
- Use `jsonb_array_elements()` to expand arrays when needed
- Filter early in WHERE clause before expanding arrays

