# GitHub Event Collection Analysis

## Issues Identified

### 1. **Database Table Mismatch** ⚠️ CRITICAL

**Problem**: Events collected by GitHub Actions are NOT being analyzed properly in the Next.js app.

**Root Cause**:
- **Python Collection Script** (`collect_events_with_cosmic_state.py`) stores correlations in:
  - `event_cosmic_correlations` table

- **Next.js App** (`src/lib/database.ts`) reads correlations from:
  - `event_planetary_correlations` table

**Result**:
- Events ARE being stored ✓
- Correlations ARE being calculated ✓
- BUT Next.js app CAN'T find them ✗
- Filtering by planets won't work for automated events ✗

### 2. **Email Notifications Not Enabled**

**Status**: Email system is functional but disabled

**To Enable**:
1. Go to: Repository Settings → Secrets and variables → Actions → Variables
2. Add: `ENABLE_EMAIL_NOTIFICATIONS` = `true`

**Email Secrets Required**:
- `SMTP_SERVER` (e.g., smtp.gmail.com)
- `SMTP_PORT` (e.g., 587)
- `EMAIL_USER` (your email)
- `EMAIL_PASSWORD` (app password)
- `RECIPIENT_EMAIL` (where to send summaries)

### 3. **Current Workflow**

```
GitHub Actions (every 2 hours)
  ↓
collect_events_with_cosmic_state.py
  ↓
OpenAI detects events
  ↓
Events stored in 'events' table ✓
  ↓
Correlations stored in 'event_cosmic_correlations' ✗
  ↓
Next.js app reads from 'event_planetary_correlations'
  ↓
No correlations found ✗
```

## Solutions

### Solution 1: Modify Python Script (Recommended)

**Update** `collect_events_with_cosmic_state.py` to store correlations in BOTH tables:

```python
# Store in event_cosmic_correlations (for analysis)
supabase.table('event_cosmic_correlations').insert(correlation_db_data).execute()

# ALSO store in event_planetary_correlations (for Next.js app)
for planet_corr in extract_planet_correlations(correlation_data):
    supabase.table('event_planetary_correlations').insert({
        'event_id': event_id,
        'date': event_date,
        'planet_name': planet_corr['planet'],
        'correlation_score': planet_corr['score'],
        'reason': planet_corr['reason']
    }).execute()
```

### Solution 2: Modify Next.js App (Alternative)

**Update** `src/lib/database.ts` to read from BOTH tables:

```typescript
// Try event_planetary_correlations first
let correlations = await supabase.from('event_planetary_correlations')...

// If empty, try event_cosmic_correlations
if (!correlations || correlations.length === 0) {
  correlations = await supabase.from('event_cosmic_correlations')...
}
```

### Solution 3: Database Migration (Clean Slate)

**Copy** existing data from `event_cosmic_correlations` to `event_planetary_correlations`

## Verification Steps

After implementing the fix:

1. **Trigger Manual Run**:
   ```bash
   # Go to: Actions → Event Collection → Run workflow
   ```

2. **Check Database**:
   ```sql
   -- Should have records in both tables
   SELECT COUNT(*) FROM event_cosmic_correlations;
   SELECT COUNT(*) FROM event_planetary_correlations;
   ```

3. **Test in App**:
   - Go to `/events` page
   - Apply planet filter (e.g., Mars)
   - Automated events should appear ✓

4. **Check Email**:
   - After GitHub Actions run
   - Check inbox for summary email
   - Should show:
     - Events detected
     - Events stored
     - Correlations created
     - Average correlation score

## Email Summary Format

When enabled, you'll receive emails like:

```
🌟 Cosmic Diary: Event Collection Summary
Status: ✅ SUCCESS

Collection Time: 2025-12-15 12:30:00 UTC

Statistics:
- Events Detected: 5
- Events Stored: 5
- Correlations Created: 5
- Avg Correlation Score: 72.50/100
```

## Recommended Implementation Order

1. ✅ **Fix table mismatch** (Solution 1 - modify Python script)
2. ✅ **Enable email notifications** (set GitHub variable)
3. ✅ **Test manual run** (verify everything works)
4. ✅ **Monitor automated runs** (check every 2 hours)

## Current GitHub Actions Schedule

- **Frequency**: Every 2 hours
- **Times**: 00:30, 02:30, 04:30, 06:30, 08:30, 10:30, 12:30, 14:30, 16:30, 18:30, 20:30, 22:30 UTC
- **Lookback Window**: 12 hours (to avoid missing events)
- **Manual Trigger**: Available via workflow_dispatch

## Files to Modify

1. `collect_events_with_cosmic_state.py` (lines 1076-1077)
2. `.github/workflows/event-collection.yml` (add variable check)
3. GitHub Secrets/Variables (add email config)
