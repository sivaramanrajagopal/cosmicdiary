# How to View Events in the UI

## 📍 Pages to View Events

### 1. **Analysis Page** (`/analysis`)
- **URL**: `https://cosmicdiary.vercel.app/analysis`
- **What it shows**:
  - Latest 20 events (sorted by `created_at DESC` - newest first)
  - Planetary analysis for each event
  - Significant planets, retrograde planets
  - Correlation details
  - Dominant Rasi and Nakshatra
- **How to access**: Click "Analysis" in the navigation menu

### 2. **Events Page** (`/events`)
- **URL**: `https://cosmicdiary.vercel.app/events`
- **What it shows**:
  - All events in a list
  - Title, category, location, date
  - Impact level badge
- **How to access**: Click "Events" in the navigation menu

### 3. **Individual Event Detail Page** (`/events/[id]`)
- **URL**: `https://cosmicdiary.vercel.app/events/53` (for event ID 53)
- **What it shows**:
  - Full event details
  - Astrological chart (North/South Indian chart)
  - Planetary positions table
  - House mappings
  - Planetary aspects
  - Chart data (Ascendant, house cusps, etc.)
  - Correlation scores
- **How to access**: Click on any event from the Events or Analysis page

## 🔍 Your Recent Events (IDs 53-57)

Based on your latest collection run, these events should be visible:

1. **Event 53**: "Major Political Unrest in Tamil Nadu Following New Education Policy Announcement"
   - Location: Chennai, Tamil Nadu, India
   - Correlation Score: 1.00 (24 matches)
   - View at: `/events/53`

2. **Event 54**: "Severe Earthquake Strikes Northern India, Multiple Casualties Reported"
   - Location: Himachal Pradesh, India
   - Correlation Score: 1.00 (23 matches)
   - View at: `/events/54`

3. **Event 55**: "India's Inflation Rate Surges to 9% Amid Economic Turmoil"
   - Location: New Delhi, India
   - Correlation Score: 1.00 (23 matches)
   - View at: `/events/55`

4. **Event 56**: "International Summit on Climate Change Convenes in Paris"
   - Location: Paris, France
   - Correlation Score: 0.60 (10 matches)
   - View at: `/events/56`

5. **Event 57**: "Severe Flooding in Maharashtra Displaces Thousands"
   - Location: Maharashtra, India
   - Correlation Score: 1.00 (24 matches)
   - View at: `/events/57`

## 📊 What Each Page Shows

### Analysis Page Details:
- **Overview Statistics**: Total events, planetary correlations, retrograde influence
- **Planetary Patterns**: Most active Rasis, Nakshatras
- **Category-Planetary Links**: Which planets are associated with which event categories
- **Retrograde Analysis**: Frequency of retrograde planets during events
- **Event Cards**: Each event shows:
  - Title, category, date, impact level
  - Dominant Rasi and Nakshatra
  - Significant planetary influences (top 3)
  - Retrograde planets
  - Planetary correlations
  - Click to view full details

### Events Page Details:
- Simple list view of all events
- Quick access to event details
- Filter by date (if implemented)

### Event Detail Page:
- Complete astrological chart visualization
- All planetary positions in a table
- House number mappings
- Planetary aspects to event house
- Correlation breakdown with cosmic snapshot

## 🔄 After Running Event Collection

After you run the event collection job:

1. **Wait a few seconds** for the job to complete
2. **Refresh the Analysis page** (`/analysis`)
3. **New events should appear at the top** (latest first)
4. **Click on any event** to see full astrological details

## 🐛 Troubleshooting

### Events not showing up?
1. Check if events were actually stored:
   ```sql
   SELECT id, title, created_at FROM events ORDER BY created_at DESC LIMIT 5;
   ```

2. Check if the frontend is connected to the right database:
   - Verify `NEXT_PUBLIC_SUPABASE_URL` in Vercel
   - Verify `NEXT_PUBLIC_SUPABASE_ANON_KEY` in Vercel

3. Clear browser cache and refresh

### Analysis not showing?
1. Check if planetary data exists:
   ```sql
   SELECT date FROM planetary_data WHERE date >= '2025-12-13' ORDER BY date DESC;
   ```

2. Check if correlations exist:
   ```sql
   SELECT event_id, correlation_score FROM event_cosmic_correlations 
   WHERE event_id IN (53, 54, 55, 56, 57);
   ```

3. The analysis page calculates correlations on-the-fly from planetary data
   - If planetary data is missing for a date, analysis won't show for that event

## 📱 Quick Links

- **Analysis**: `https://cosmicdiary.vercel.app/analysis`
- **Events**: `https://cosmicdiary.vercel.app/events`
- **Jobs (Run Collection)**: `https://cosmicdiary.vercel.app/jobs`
- **Event 53**: `https://cosmicdiary.vercel.app/events/53`
- **Event 54**: `https://cosmicdiary.vercel.app/events/54`
- **Event 55**: `https://cosmicdiary.vercel.app/events/55`
- **Event 56**: `https://cosmicdiary.vercel.app/events/56`
- **Event 57**: `https://cosmicdiary.vercel.app/events/57`

