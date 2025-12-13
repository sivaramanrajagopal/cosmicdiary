# Fix Missing Coordinates for Existing Events

## Problem
Events were geocoded and charts were calculated, but coordinates weren't saved back to the `events` table. This causes the chart to not display on the event detail page.

## Solution

### For Future Events
✅ **Fixed**: The code now updates the events table with geocoded coordinates after geocoding.

### For Existing Events (IDs 53-57)

Run this SQL query in Supabase to update existing events with coordinates from their chart data:

```sql
-- Update events with coordinates based on chart data location
-- This uses the location name to geocode (or uses default India coordinates)

UPDATE events e
SET 
    latitude = CASE 
        WHEN e.location ILIKE '%New Delhi%' OR e.location ILIKE '%Delhi%' THEN 28.6139
        WHEN e.location ILIKE '%Chennai%' OR e.location ILIKE '%Tamil Nadu%' THEN 13.0837
        WHEN e.location ILIKE '%Himachal Pradesh%' THEN 31.9292
        WHEN e.location ILIKE '%Maharashtra%' THEN 18.9068
        WHEN e.location ILIKE '%Paris%' OR e.location ILIKE '%France%' THEN 48.8535
        WHEN e.location ILIKE '%India%' THEN 28.6139  -- Default to Delhi
        ELSE NULL
    END,
    longitude = CASE 
        WHEN e.location ILIKE '%New Delhi%' OR e.location ILIKE '%Delhi%' THEN 77.2090
        WHEN e.location ILIKE '%Chennai%' OR e.location ILIKE '%Tamil Nadu%' THEN 80.2702
        WHEN e.location ILIKE '%Himachal Pradesh%' THEN 77.1828
        WHEN e.location ILIKE '%Maharashtra%' THEN 75.6742
        WHEN e.location ILIKE '%Paris%' OR e.location ILIKE '%France%' THEN 2.3484
        WHEN e.location ILIKE '%India%' THEN 77.2090  -- Default to Delhi
        ELSE NULL
    END
WHERE e.id IN (53, 54, 55, 56, 57)
  AND (e.latitude IS NULL OR e.longitude IS NULL);
```

### Specific Update for Event 55 (Inflation Rate)

```sql
-- Update event 55 specifically
UPDATE events
SET 
    latitude = 28.6419,  -- New Delhi coordinates (from geocoding log)
    longitude = 77.2217
WHERE id = 55;
```

### Verify the Update

```sql
-- Check if coordinates are now set
SELECT 
    id,
    title,
    location,
    latitude,
    longitude,
    CASE 
        WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN '✓ Has coordinates'
        ELSE '✗ Missing coordinates'
    END as status
FROM events
WHERE id IN (53, 54, 55, 56, 57)
ORDER BY id;
```

## After Running the Update

1. **Refresh the event detail page** (`/events/55`)
2. **The chart should now display** automatically (since `event_chart_data` already exists)
3. **If chart still doesn't show**, check:
   - `event_chart_data` table has data for event_id = 55
   - `hasLocation` prop is now `true` (coordinates exist)

## Prevention

The code has been updated to automatically save geocoded coordinates back to the events table. Future events will have coordinates saved automatically.

