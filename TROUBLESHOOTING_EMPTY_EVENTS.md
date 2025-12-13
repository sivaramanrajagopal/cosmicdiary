# Troubleshooting: GitHub Actions Not Fetching Events

## Common Issues and Solutions

### Issue 1: OpenAI Returns 0 Events

**Symptoms:**
- GitHub Actions runs successfully
- Output shows: "✓ Received 0 events from OpenAI"
- No events stored in database

**Possible Causes:**

1. **No Significant Events in Time Window**
   - The 2-hour window might not have significant events
   - **Solution:** The prompt now includes fallback to Indian news

2. **Prompt Too Restrictive**
   - The prompt was too strict for short time windows
   - **Solution:** Updated prompt to be more lenient for 2-hour windows

3. **OpenAI API Issues**
   - Rate limiting
   - API errors
   - **Solution:** Check OpenAI API status and usage

**Debug Steps:**
1. Check GitHub Actions logs for:
   ```
   ✓ Received X events from OpenAI
   ```
2. Look for validation errors:
   ```
   ⚠️ Skipping event '...': Invalid category
   ```

---

### Issue 2: Events Rejected During Validation

**Symptoms:**
- OpenAI returns events (e.g., 5 events)
- But validation shows: "Validated: 0/5 events"
- All events are rejected

**Common Rejection Reasons:**

1. **Invalid Category**
   - Category doesn't match expected format
   - **Solution:** Category normalization has been improved

2. **Missing Astrological Mapping**
   - Event missing `astrological_relevance`
   - **Solution:** Auto-mapping is now enabled (lenient mode)

3. **Invalid Impact Level**
   - Must be: `low`, `medium`, `high`, or `critical`
   - **Solution:** Check OpenAI prompt specifies these values

4. **Description Length Issues**
   - Description too short (< 50 chars) or too long (> 800 chars)
   - **Solution:** Validation now allows 50-800 characters

**Debug Output:**
The script now shows detailed rejection reasons:
```
⚠️ Skipping event 'Event Title': Invalid category
   Category: Natural Disaster
   Impact: high
   Has astro: False
```

---

### Issue 3: Category Validation Failures

**Categories That Are Accepted:**
- Natural Disasters
- Economic Events
- Political Events
- Health & Medical
- Technology & Innovation
- Business & Commerce
- Wars & Conflicts
- Employment & Labor
- Women & Children
- Entertainment & Sports
- Social, Cultural, Sports, Environment, Education (also accepted)

**Category Normalization:**
The script now automatically normalizes:
- `natural disaster` → `Natural Disasters`
- `economic` → `Economic Events`
- `political` → `Political Events`
- `health` → `Health & Medical`
- `technology` → `Technology & Innovation`
- etc.

---

## Solutions Implemented

### 1. More Lenient Prompt for Short Windows

The prompt now:
- ✅ Adjusts significance thresholds for 2-hour windows
- ✅ Includes more regional/state-level events
- ✅ Always includes top Indian news
- ✅ Requests at least 5-10 events

### 2. Enhanced Validation with Auto-Mapping

- ✅ Lenient validation mode (allows missing astrological mapping)
- ✅ Auto-maps astrological relevance if missing
- ✅ Better category normalization
- ✅ More detailed error logging

### 3. Better Debugging Output

The script now logs:
- ✅ Number of events received from OpenAI
- ✅ Sample event structure
- ✅ Validation statistics
- ✅ Detailed rejection reasons
- ✅ Category normalization actions

---

## How to Debug GitHub Actions Runs

### Step 1: Check GitHub Actions Logs

1. Go to: `https://github.com/your-repo/actions`
2. Click on the latest workflow run
3. Click on "Collect Events and Capture Cosmic State" job
4. Expand "Run cosmic state collection with event correlation"

### Step 2: Look for These Lines

**Success Indicators:**
```
✓ Received 10 events from OpenAI
✓ Validated: 8/10 events
✓ Events Detected: 8
✓ Events Stored: 8
```

**Problem Indicators:**
```
✓ Received 0 events from OpenAI
⚠️ WARNING: OpenAI returned 0 events!
```

or

```
✓ Received 5 events from OpenAI
✓ Validated: 0/5 events
⚠️ No valid events after validation
```

### Step 3: Check Validation Stats

Look for:
```
✓ Validated: X/Y events
✗ Invalid: Z events
  Reasons:
    - Invalid category: N
    - Missing astrological mapping: M
```

---

## Manual Testing

### Test Locally:

```bash
# Test with 2-hour window (same as GitHub Actions)
python collect_events_with_cosmic_state.py --lookback-hours 2
```

### Check Output:
1. Does OpenAI return events?
2. Do events pass validation?
3. Are events stored in database?

---

## Quick Fixes

### If OpenAI Returns 0 Events:

1. **Check Time Window:**
   ```bash
   # The script will show:
   📅 Detecting events for time window:
      Lookback: 2 hour(s)
      Start: 2025-12-09 20:00:00 UTC
      End: 2025-12-09 22:00:00 UTC
   ```

2. **Try Longer Window:**
   ```bash
   # Test with 4 hours to see if events exist
   python collect_events_with_cosmic_state.py --lookback-hours 4
   ```

3. **Check OpenAI API:**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check OpenAI API status
   - Verify usage limits not exceeded

### If Events Are Rejected:

1. **Check Rejection Reasons:**
   - Look for: "⚠️ Skipping event: ..."
   - Common: Invalid category, missing fields

2. **Enable More Verbose Logging:**
   - The script already shows detailed reasons
   - Check category normalization logs

---

## Expected Behavior

**For 2-Hour Window (GitHub Actions):**
- ✅ Should return 5-15 events
- ✅ Should include Indian news if global news is scarce
- ✅ Should validate at least 3-5 events
- ✅ Should store at least 3-5 events

**If Less Than 3 Events:**
- Check if there were actually events in that time period
- The prompt is now more lenient to capture regional news
- Consider if the time window is too short

---

## Configuration

**GitHub Actions Workflow:**
```yaml
env:
  EVENT_LOOKBACK_HOURS: '2'
run: |
  python collect_events_with_cosmic_state.py --lookback-hours 2
```

**If Still Getting 0 Events:**
1. Try increasing to 4 hours temporarily:
   ```yaml
   EVENT_LOOKBACK_HOURS: '4'
   ```
2. Check if events appear
3. Then adjust back to 2 hours

---

## Next Steps

1. ✅ **Prompt Updated** - More lenient for short windows
2. ✅ **Validation Improved** - Auto-mapping enabled
3. ✅ **Debugging Enhanced** - Better error messages
4. ⏳ **Monitor Next Run** - Check GitHub Actions logs
5. ⏳ **Verify Events** - Check database for stored events

---

**Last Updated:** December 9, 2025

