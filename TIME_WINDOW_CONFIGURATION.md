# Time Window Configuration Guide

## Overview

The event collection system supports configurable time windows for detecting events. This allows different lookback periods for on-demand manual runs versus scheduled automated runs.

---

## Configuration Modes

### 1. On-Demand Manual Runs (Default: 1 hour)

When a user manually triggers the event collection job via the UI or API, the system uses a **1-hour lookback window** to capture recent events.

**Frontend API Route:**
- `POST /api/jobs/run-event-collection`
- Accepts optional `lookback_hours` in request body
- Default: `1` hour

**Example Request:**
```json
POST /api/jobs/run-event-collection
{
  "lookback_hours": 1
}
```

**Flask Backend:**
- `POST /api/jobs/run-event-collection`
- Accepts `lookback_hours` parameter (validated: 1-24 hours)
- Passes to script as `--lookback-hours N`

**Script Execution:**
```bash
python collect_events_with_cosmic_state.py --lookback-hours 1
```

---

### 2. Scheduled GitHub Actions (Default: 2 hours)

When the automated GitHub Actions workflow runs every 2 hours, it uses a **2-hour lookback window** to capture events from the period since the last run.

**GitHub Actions Workflow:**
- File: `.github/workflows/event-collection.yml`
- Schedule: Every 2 hours (cron: `0 */2 * * *`)
- Environment variable: `EVENT_LOOKBACK_HOURS=2`
- Command: `python collect_events_with_cosmic_state.py --lookback-hours 2`

**Configuration:**
```yaml
env:
  EVENT_LOOKBACK_HOURS: '2'
run: |
  python collect_events_with_cosmic_state.py --lookback-hours 2
```

---

## How It Works

### 1. Command Line Arguments

The `collect_events_with_cosmic_state.py` script accepts a `--lookback-hours` parameter:

```bash
python collect_events_with_cosmic_state.py --lookback-hours N
```

Where `N` is the number of hours to look back (1-24).

**Implementation:**
```python
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lookback-hours', type=int, default=None)
    args = parser.parse_args()
    
    # Determine lookback hours
    lookback_hours = args.lookback_hours
    if lookback_hours is None:
        lookback_hours = int(os.getenv('EVENT_LOOKBACK_HOURS', '2'))
```

### 2. Time Window Calculation

The `get_time_window()` function calculates the time window:

```python
def get_time_window(lookback_hours: int = None):
    now = datetime.utcnow()
    if lookback_hours is None:
        lookback_hours = int(os.getenv('EVENT_LOOKBACK_HOURS', '2'))
    start_time = now - timedelta(hours=lookback_hours)
    return {
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC",
        "lookback_hours": lookback_hours
    }
```

### 3. OpenAI Prompt

The prompt system emphasizes the exact time window:

```python
def generate_user_prompt(time_window=None):
    lookback_hours = time_window.get('lookback_hours', 2)
    prompt = f"""Scan news sources for significant world events from {time_window['start']} to {time_window['end']} UTC (past {lookback_hours} hour(s)).

CRITICAL: Focus ONLY on events that occurred within this specific time window. Do not include events from earlier periods.
...
Analysis window: Past {lookback_hours} hour(s) (from {time_window['start']} to {time_window['end']} UTC)
Time window is CRITICAL - only include events from this exact period.
"""
```

---

## Default Behavior

### Priority Order (highest to lowest):

1. **Command line argument** (`--lookback-hours N`)
   - Takes highest priority
   - Used by both on-demand and scheduled runs

2. **Environment variable** (`EVENT_LOOKBACK_HOURS`)
   - Used if command line argument is not provided
   - Set in GitHub Actions workflow

3. **Hardcoded default** (`2` hours)
   - Used if neither command line arg nor env var is set
   - Fallback for backwards compatibility

---

## Usage Examples

### Example 1: On-Demand Run (1 hour)

**Via Frontend:**
```javascript
// Frontend automatically uses 1 hour default
fetch('/api/jobs/run-event-collection', {
  method: 'POST',
  body: JSON.stringify({ lookback_hours: 1 })
});
```

**Via Flask API:**
```bash
curl -X POST https://your-railway-url/api/jobs/run-event-collection \
  -H "Content-Type: application/json" \
  -d '{"lookback_hours": 1}'
```

**Direct Script:**
```bash
python collect_events_with_cosmic_state.py --lookback-hours 1
```

### Example 2: Scheduled Run (2 hours)

**GitHub Actions automatically uses:**
```yaml
env:
  EVENT_LOOKBACK_HOURS: '2'
run: |
  python collect_events_with_cosmic_state.py --lookback-hours 2
```

### Example 3: Custom Time Window (3 hours)

**For testing or special scenarios:**
```bash
python collect_events_with_cosmic_state.py --lookback-hours 3
```

Or via API:
```json
POST /api/jobs/run-event-collection
{
  "lookback_hours": 3
}
```

---

## Validation

### Backend Validation (Flask)

The Flask endpoint validates the `lookback_hours` parameter:

```python
lookback_hours = request_data.get('lookback_hours', 1)
try:
    lookback_hours = int(lookback_hours)
    if lookback_hours < 1 or lookback_hours > 24:
        return jsonify({
            'error': 'Invalid lookback_hours. Must be between 1 and 24.'
        }), 400
except (ValueError, TypeError):
    return jsonify({
        'error': 'Invalid lookback_hours format. Must be a number.'
    }), 400
```

**Constraints:**
- Minimum: 1 hour
- Maximum: 24 hours
- Must be an integer

---

## Testing

### Test On-Demand (1 hour):
```bash
# Trigger via Flask API
curl -X POST http://localhost:8000/api/jobs/run-event-collection \
  -H "Content-Type: application/json" \
  -d '{"lookback_hours": 1}'

# Or directly via script
python collect_events_with_cosmic_state.py --lookback-hours 1
```

### Test Scheduled (2 hours):
```bash
# Simulate GitHub Actions
export EVENT_LOOKBACK_HOURS=2
python collect_events_with_cosmic_state.py --lookback-hours 2
```

### Verify Time Window:
Check the script output for:
```
📅 Detecting events for time window:
   Lookback: 1 hour(s)
   Start: 2025-12-09 21:00:00 UTC
   End: 2025-12-09 22:00:00 UTC
```

---

## Troubleshooting

### Issue: Time window not respected

**Symptoms:**
- Events from wrong time periods are captured
- OpenAI returns events outside the window

**Solutions:**
1. Verify the prompt includes the time window clearly
2. Check script output logs for actual time window used
3. Verify `lookback_hours` parameter is passed correctly

### Issue: Default behavior not working

**Symptoms:**
- Script uses wrong default
- Environment variable not read

**Solutions:**
1. Check environment variable is set: `echo $EVENT_LOOKBACK_HOURS`
2. Verify command line argument is passed: `python script.py --lookback-hours 2`
3. Check script output for which value is used

---

## Summary

| Mode | Lookback Window | Trigger | Configuration |
|------|----------------|---------|---------------|
| On-Demand | 1 hour (default) | Manual via UI/API | Request body or CLI arg |
| Scheduled | 2 hours (default) | GitHub Actions (every 2h) | Env var + CLI arg |
| Custom | 1-24 hours | Any | CLI arg or request body |

**Key Points:**
- ✅ On-demand: 1 hour for recent events
- ✅ Scheduled: 2 hours to match job frequency
- ✅ Flexible: Configurable via CLI, env var, or API
- ✅ Validated: Backend validates 1-24 hour range
- ✅ Documented: Prompts clearly state time window

---

**Last Updated:** December 9, 2025

