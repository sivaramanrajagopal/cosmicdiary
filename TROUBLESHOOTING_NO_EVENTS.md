# 🔍 Troubleshooting: No Events Detected

## Issue
GitHub Actions workflow runs successfully but reports:
- Events Detected: 0
- Events Stored: 0
- Correlations Created: 0

## Common Causes

### 1. ✅ OpenAI API Issues

**Check:**
- Is `OPENAI_API_KEY` set correctly in GitHub Secrets?
- Does the OpenAI API key have credits/usage available?
- Check workflow logs for OpenAI API errors

**Solution:**
```bash
# Test OpenAI API key locally
python -c "from openai import OpenAI; client = OpenAI(api_key='your-key'); print(client.models.list())"
```

### 2. ✅ Time Window Too Recent

**Issue:** OpenAI might not find events if the time window is too recent (e.g., looking for events in the last 2 hours might not find significant world events).

**Check:** The script looks for events in the past 2-3 hours. Significant world events might not occur in every 2-hour window.

**Solution:** This is **normal behavior**. Not every 2-hour window will have significant events. The script should still capture cosmic snapshots every 2 hours.

### 3. ✅ OpenAI Response Format Issues

**Issue:** OpenAI might return events but in an unexpected format, causing parsing to fail.

**Check Workflow Logs For:**
- JSON parsing errors
- "Invalid event format" messages
- OpenAI response structure issues

**Solution:** Check the workflow logs in GitHub Actions → Your Run → "Run cosmic state collection" step

### 4. ✅ Event Validation Too Strict

**Issue:** Events might be detected but filtered out due to strict validation criteria.

**Check:** Look for messages like:
- "Skipping invalid event"
- "Event validation failed"
- "Missing required fields"

**Solution:** Check validation logic in `collect_events_with_cosmic_state.py`

### 5. ✅ Cosmic Snapshot Still Working

**Good News:** Even if no events are detected, the cosmic snapshot should still be captured every 2 hours.

**Verify:**
1. Check Supabase `cosmic_snapshots` table
2. Look for new entries every 2 hours
3. Verify planetary positions are being stored

## Debugging Steps

### Step 1: Check Workflow Logs

1. Go to GitHub Actions → Your workflow run
2. Click on "Run cosmic state collection with event correlation"
3. Look for:
   - OpenAI API calls
   - Error messages
   - Event detection messages
   - JSON parsing issues

### Step 2: Check OpenAI Response

Look in logs for:
```
🤖 Calling OpenAI API with enhanced astrological prompts...
  ✓ Received X events from OpenAI
```

If you see "0 events", OpenAI might not be finding events for that time window.

### Step 3: Test Locally

Run the script locally to see detailed output:

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
python3 collect_events_with_cosmic_state.py
```

This will show:
- Detailed OpenAI prompts
- Raw OpenAI responses
- Event validation details
- All error messages

### Step 4: Check Supabase Data

1. Go to Supabase Dashboard
2. Check `cosmic_snapshots` table - should have entries every 2 hours
3. Check `events` table - may be empty if no events detected
4. Check `event_cosmic_correlations` table

## Expected Behavior

### Normal Scenarios:

1. **Cosmic Snapshot Captured, No Events:**
   - ✅ Cosmic snapshot created in database
   - ⚠️ 0 events detected (normal if no significant events in 2-hour window)
   - ✅ Script completes successfully

2. **Cosmic Snapshot + Events:**
   - ✅ Cosmic snapshot created
   - ✅ Events detected and stored
   - ✅ Correlations created

### This is NOT a Problem If:

- ✅ Cosmic snapshots are being created every 2 hours
- ✅ Workflow completes successfully (exit code 0)
- ✅ No error messages in logs
- ⚠️ Only "0 events detected" - this is normal for some time windows

### This IS a Problem If:

- ❌ No cosmic snapshots in database
- ❌ Workflow fails with errors
- ❌ OpenAI API errors in logs
- ❌ JSON parsing errors

## Quick Checks

### Check 1: Verify Secrets
```bash
# In GitHub: Settings → Secrets and variables → Actions
# Verify these exist:
- OPENAI_API_KEY
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- FLASK_API_URL
```

### Check 2: Verify Cosmic Snapshots
```sql
-- Run in Supabase SQL Editor
SELECT 
    id,
    snapshot_time,
    created_at,
    lagna_rasi,
    lagna_rasi_number
FROM cosmic_snapshots
ORDER BY created_at DESC
LIMIT 10;
```

If you see recent entries (every 2 hours), cosmic snapshots are working ✅

### Check 3: Test OpenAI Detection
```python
# Create test script: test_openai_detection.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Test with a simple prompt
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List 2 recent significant world events from the past 24 hours. Return as JSON array."}
    ]
)

print(response.choices[0].message.content)
```

## Next Steps

1. **If cosmic snapshots ARE being created:**
   - ✅ System is working correctly
   - Events are optional - not every window has significant events
   - Consider widening the time window if you want more events

2. **If cosmic snapshots are NOT being created:**
   - ❌ Check workflow logs for errors
   - ❌ Verify Supabase connection
   - ❌ Check FLASK_API_URL is correct

3. **If you want more events:**
   - Modify the OpenAI prompt to be less strict
   - Extend the time window (past 24 hours instead of 2-3 hours)
   - Lower the significance threshold

## Summary

**0 events detected is NOT necessarily an error** - it means:
- ✅ The script ran successfully
- ✅ OpenAI was called correctly
- ✅ No significant events found in the 2-hour window

**What matters:**
- ✅ Cosmic snapshots are captured every 2 hours
- ✅ Workflow completes without errors
- ✅ Data is stored in Supabase

Events will appear when significant world events occur!

