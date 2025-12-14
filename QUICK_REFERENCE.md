# Quick Reference Guide - Event Collection System

**Last Updated**: 2025-12-14

---

## 🚀 Quick Commands

### Test System Health
```bash
python3 test_event_collection_setup.py
```
This checks all components and confirms everything is configured correctly.

### Run Event Collection Locally
```bash
# With 2-hour window (may return few events due to OpenAI limitations)
python3 collect_events_with_cosmic_state.py --lookback-hours 2

# With 12-hour window (RECOMMENDED - better results)
python3 collect_events_with_cosmic_state.py --lookback-hours 12

# With 24-hour window (for historical analysis)
python3 collect_events_with_cosmic_state.py --lookback-hours 24
```

### Trigger GitHub Actions Manually
1. Go to GitHub → Actions tab
2. Select "Event Collection with Cosmic State - Every 2 Hours"
3. Click "Run workflow" → "Run workflow"
4. View logs to see actual event counts

---

## 📊 Expected Outputs

### ✅ Success Output
```
================================================================================
SUMMARY
================================================================================
✓ Events Detected: 10
✓ Events Stored: 10
✓ Correlations Created: 8
✓ Average Correlation Score: 0.75
✓ Highest Correlation Score: 0.95
✓ Lowest Correlation Score: 0.55
✓ Success Rate: 100.0%
================================================================================

✅ Event collection completed successfully!

::group::GitHub Actions Output
EVENTS_DETECTED=10
EVENTS_STORED=10
CORRELATIONS_CREATED=8
AVG_CORRELATION_SCORE=0.75
::endgroup::
```

### ⚠️ Zero Events Output
```
⚠️  No events detected. Exiting.
   This is normal if:
   - No significant events occurred in the time window
   - OpenAI returned 0 events (check logs above)
   - All events were filtered during validation

::group::GitHub Actions Output
EVENTS_DETECTED=0
EVENTS_STORED=0
CORRELATIONS_CREATED=0
AVG_CORRELATION_SCORE=0.00
::endgroup::
```

---

## 🔧 Troubleshooting

### Problem: Always Getting Zero Events

**Diagnosis**:
```bash
# Check if it's an OpenAI issue
python3 test_event_collection_setup.py
```

**Solutions**:
1. **Increase lookback window**: Use 12 hours instead of 2
   ```bash
   python3 collect_events_with_cosmic_state.py --lookback-hours 12
   ```

2. **Check OpenAI API**:
   - Verify API key is valid
   - Check usage limits at https://platform.openai.com/usage
   - OpenAI has NO real-time news access - it only knows events from training data

3. **Integrate News API** (recommended for production):
   - See `NEWS_API_INTEGRATION_GUIDE.md`
   - Get free NewsAPI key: https://newsapi.org/register

### Problem: Validation Failures

**Diagnosis**: Look for this in logs:
```
⚠️  NO VALID EVENTS AFTER VALIDATION
💡 Most Common Rejection Reasons:
   - Missing required field: description (5 events)
   - Invalid category: xyz (3 events)
```

**Solutions**:
- Events might have wrong category names
- Events might have missing fields
- Check validation logic in prompts/event_detection_prompt.py

### Problem: GitHub Actions Still Shows Zero

**Check**:
1. Workflow logs for "📊 Parsed Statistics"
2. If you see hardcoded zeros, the workflow file wasn't updated
3. Download `collection_output.log` artifact to inspect

**Fix**:
```bash
# Verify workflow file has the parsing logic
grep -A 10 "Extract collection statistics" .github/workflows/event-collection.yml
```

---

## ⚙️ Configuration

### Environment Variables

**Required** (in `.env.local` or GitHub Secrets):
```bash
OPENAI_API_KEY=sk-proj-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

**Optional**:
```bash
EVENT_LOOKBACK_HOURS=12  # Default: 2
NEWSAPI_KEY=xxx  # If using News API integration
```

### GitHub Actions Schedule

Current schedule: **Every 2 hours at :30 past the hour**
```yaml
# In .github/workflows/event-collection.yml
on:
  schedule:
    - cron: '30 */2 * * *'  # Every 2 hours
```

To change:
```yaml
# Every hour
- cron: '0 * * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Daily at midnight
- cron: '0 0 * * *'
```

---

## 📈 Performance Optimization

### For Better Event Collection

1. **Use longer lookback window**:
   - 2 hours = May return 0-5 events (OpenAI limitation)
   - 12 hours = Usually returns 8-15 events ✅
   - 24 hours = Usually returns 12-20 events ✅

2. **Integrate News API**:
   - Real-time events
   - More accurate
   - See `NEWS_API_INTEGRATION_GUIDE.md`

3. **Adjust validation rules**:
   - Make lenient mode default
   - Allow more categories
   - See `prompts/event_detection_prompt.py`

### For Faster Execution

1. **Reduce max events**:
   ```python
   # In detect_events_openai(), line 659
   selected_events = validated_events[:10]  # Instead of [:15]
   ```

2. **Skip correlations for testing**:
   ```bash
   # Just test event detection
   python3 -c "
   from collect_events_with_cosmic_state import detect_events_openai
   events = detect_events_openai(lookback_hours=12)
   print(f'Got {len(events)} events')
   "
   ```

---

## 📁 Important Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `collect_events_with_cosmic_state.py` | Main event collection script | Change core logic |
| `prompts/event_detection_prompt.py` | OpenAI prompts & validation | Adjust event criteria |
| `.github/workflows/event-collection.yml` | GitHub Actions workflow | Change schedule/config |
| `test_event_collection_setup.py` | Diagnostic tool | Never (just run it) |
| `FIXES_SUMMARY.md` | Complete documentation | Reference only |
| `NEWS_API_INTEGRATION_GUIDE.md` | News API setup guide | When adding News API |

---

## 🎯 Common Tasks

### Change Event Collection Schedule
Edit `.github/workflows/event-collection.yml` line 6:
```yaml
- cron: '30 */6 * * *'  # Every 6 hours instead of 2
```

### Add News API Integration
1. Get API key from https://newsapi.org/register
2. Add to `.env.local`: `NEWSAPI_KEY=your_key`
3. Follow guide in `NEWS_API_INTEGRATION_GUIDE.md`

### Adjust Event Validation
Edit `prompts/event_detection_prompt.py`:
- Line 391-498: `validate_event_response()` function
- Line 503-555: `calculate_research_score()` function

### Test OpenAI Prompts
```bash
python3 -c "
from prompts.event_detection_prompt import generate_user_prompt, get_time_window
tw = get_time_window(lookback_hours=12)
prompt = generate_user_prompt(tw)
print(prompt)
"
```

---

## 📞 Support Resources

- **Full Documentation**: `FIXES_SUMMARY.md`
- **News API Guide**: `NEWS_API_INTEGRATION_GUIDE.md`
- **Test Tool**: `python3 test_event_collection_setup.py`
- **GitHub Actions Logs**: Actions tab → Latest run → View logs
- **Download Logs**: Actions tab → Run → Artifacts → download `collection_output.log`

---

## ✅ Checklist for New Setup

- [ ] Run `python3 test_event_collection_setup.py` - all checks pass
- [ ] Test locally: `python3 collect_events_with_cosmic_state.py --lookback-hours 12`
- [ ] Verify GitHub Secrets are set (OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
- [ ] Trigger GitHub Actions manually and verify statistics show real numbers
- [ ] (Optional) Set up NewsAPI for real-time events
- [ ] Monitor first few automated runs

---

## 🆘 Still Having Issues?

1. **Check diagnostic output**:
   ```bash
   python3 test_event_collection_setup.py
   ```

2. **Check recent logs**:
   ```bash
   # View last 50 lines of test run
   python3 collect_events_with_cosmic_state.py --lookback-hours 12 2>&1 | tail -50
   ```

3. **Check GitHub Actions**:
   - Go to Actions → Latest workflow run
   - Look for "📊 Parsed Statistics"
   - Download `collection_output.log` artifact

4. **Common fixes**:
   - Use 12-hour window instead of 2
   - Verify OpenAI API key is valid
   - Check Supabase connection
   - Consider integrating News API

---

**Need more help?** Check `FIXES_SUMMARY.md` for detailed explanations.
