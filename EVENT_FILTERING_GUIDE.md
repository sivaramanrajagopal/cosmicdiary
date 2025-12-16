# Event Quality Filtering System - Complete Guide

## Overview

The Cosmic Diary event collection system now includes a **multi-layer quality filtering system** to ensure only significant, research-worthy events are stored in your database. This prevents trivial news from cluttering your astrological analysis.

## Problem Solved

**Before filtering**: System was collecting too many trivial events (celebrity gossip, minor local news, routine announcements) because OpenAI prompts were made lenient to avoid getting zero events.

**After filtering**: System applies strict quality controls AFTER OpenAI detection but BEFORE database storage, ensuring only important events make it through.

## How It Works

### Multi-Layer Filtering Process

```
OpenAI/NewsAPI Detection
    ↓
[STEP 2b: Quality Filters]
    ├─ Impact Level Filter (medium/high/critical only)
    ├─ Category Filter (disable Entertainment, etc.)
    ├─ Impact Metrics Filter (deaths, affected, financial impact)
    ├─ Geographic Scope Filter (state/national/international)
    ├─ Keyword Blacklist (celebrity gossip, viral videos, etc.)
    ├─ Quality Score Filter (research score >= 40)
    ├─ Validation Rules (required fields, lengths)
    ├─ Time Window Filter (events not too old)
    └─ Deduplication (check against last 72 hours)
    ↓
Only High-Quality Events → Database
```

## Configuration File

All filtering rules are controlled by: **`config/event_filters.json`**

This allows you to adjust filtering without modifying Python code.

### Key Configuration Sections

#### 1. Filtering Mode

```json
{
  "filtering_mode": {
    "enabled": true,
    "mode": "strict"
  }
}
```

**Options:**
- `"strict"`: Only high-quality, significant events (recommended)
- `"balanced"`: Good quality, more lenient
- `"lenient"`: Allow more events through

#### 2. Impact Level Filter

```json
{
  "impact_level_filters": {
    "minimum_impact_level": "medium",
    "allowed_levels": ["medium", "high", "critical"]
  }
}
```

**Controls**: Minimum impact level required for storage

**Options**: `"low"`, `"medium"`, `"high"`, `"critical"`

**Example**: Set to `"high"` to only store high/critical impact events

####  3. Category Filters

```json
{
  "category_filters": {
    "enabled_categories": [
      "Natural Disasters",
      "Economic Events",
      "Political Events",
      "Health & Medical",
      "Technology & Innovation",
      "Wars & Conflicts",
      "Business & Commerce",
      "Employment & Labor"
    ],
    "disabled_categories": [
      "Entertainment & Sports"
    ]
  }
}
```

**Controls**: Which event categories to allow/block

**To disable a category**: Move it from `enabled_categories` to `disabled_categories`

**Note**: Critical impact events override disabled categories

#### 4. Impact Metrics Thresholds

```json
{
  "impact_metrics_thresholds": {
    "critical_level": {
      "deaths_min": 100,
      "injured_min": 500,
      "affected_min": 1000000,
      "financial_impact_usd_min": 1000000000
    },
    "high_level": {
      "deaths_min": 10,
      "injured_min": 50,
      "affected_min": 100000,
      "financial_impact_usd_min": 100000000
    },
    "medium_level": {
      "deaths_min": 1,
      "injured_min": 10,
      "affected_min": 10000,
      "financial_impact_usd_min": 10000000
    }
  }
}
```

**Controls**: Events must meet AT LEAST ONE threshold for their impact level

**Example**: A "high" impact event must have:
- 10+ deaths, OR
- 50+ injured, OR
- 100K+ affected, OR
- $100M+ financial impact

#### 5. Geographic Scope Filter

```json
{
  "geographic_filters": {
    "enabled": true,
    "minimum_geographic_scope": "state",
    "priority_countries": ["India", "United States", "China", ...],
    "priority_indian_states": ["Tamil Nadu", "Karnataka", ...]
  }
}
```

**Controls**: Minimum geographic scope required

**Options**: `"local"`, `"state"`, `"national"`, `"international"`

**Example**: Set to `"national"` to only store national/international events

#### 6. Keyword Blacklist

```json
{
  "keyword_filters": {
    "blacklist": {
      "enabled": true,
      "keywords": [
        "celebrity gossip",
        "social media trend",
        "viral video",
        "influencer",
        "box office collection",
        "minor traffic accident"
      ]
    }
  }
}
```

**Controls**: Events containing these keywords are filtered out (unless critical impact)

**To add more keywords**: Add to the `keywords` array

#### 7. Quality Scoring

```json
{
  "quality_scoring": {
    "enabled": true,
    "minimum_research_score": 40
  }
}
```

**Controls**: Minimum research quality score (0-100) required

**Score factors**:
- Impact level (0-40 points)
- Time accuracy (0-20 points)
- Location specificity (0-15 points)
- Astrological clarity (0-15 points)
- Measurable impact (0-10 points)

**Example**: Set to `60` for even stricter quality control

#### 8. Deduplication

```json
{
  "deduplication": {
    "enabled": true,
    "similarity_threshold": 0.85,
    "check_within_hours": 48
  }
}
```

**Controls**: Prevents storing duplicate events

**similarity_threshold**: Title similarity ratio (0.0-1.0)
- `0.85` = 85% similar titles are considered duplicates
- Lower = stricter (more duplicates caught)
- Higher = lenient (fewer duplicates caught)

**check_within_hours**: Time window to check for duplicates

#### 9. Special Rules

```json
{
  "special_rules": {
    "always_allow_critical": true,
    "always_allow_natural_disasters": true,
    "always_allow_wars_conflicts": true,
    "always_allow_economic_crises": true
  }
}
```

**Controls**: Categories that bypass most filters due to astrological significance

## Common Configuration Scenarios

### Scenario 1: Very Strict (Only Major Events)

```json
{
  "filtering_mode": {"mode": "strict"},
  "impact_level_filters": {
    "minimum_impact_level": "high",
    "allowed_levels": ["high", "critical"]
  },
  "quality_scoring": {"minimum_research_score": 60},
  "geographic_filters": {"minimum_geographic_scope": "national"}
}
```

**Result**: Only national/international high/critical impact events

### Scenario 2: Balanced (Good Quality)

```json
{
  "filtering_mode": {"mode": "balanced"},
  "impact_level_filters": {
    "minimum_impact_level": "medium",
    "allowed_levels": ["medium", "high", "critical"]
  },
  "quality_scoring": {"minimum_research_score": 40},
  "geographic_filters": {"minimum_geographic_scope": "state"}
}
```

**Result**: State-level+ medium/high/critical events (default)

### Scenario 3: Focus on Indian Events Only

```json
{
  "geographic_filters": {
    "enabled": true,
    "priority_countries": ["India"],
    "priority_indian_states": ["Tamil Nadu", "Karnataka", "Maharashtra"],
    "minimum_geographic_scope": "state"
  }
}
```

**Result**: State-level+ events from prioritized Indian states

### Scenario 4: No Entertainment, Strict Business

```json
{
  "category_filters": {
    "disabled_categories": [
      "Entertainment & Sports"
    ]
  },
  "impact_metrics_thresholds": {
    "high_level": {
      "financial_impact_usd_min": 500000000
    }
  }
}
```

**Result**: No entertainment, business events must have $500M+ impact

## Monitoring Filter Performance

### During Collection Run

When the collection script runs, you'll see filtering statistics:

```
Starting STEP 2b: Applying Quality Filters...
📋 Fetched 25 recent events for deduplication check
================================================================================
APPLYING EVENT QUALITY FILTERS
================================================================================
Input: 12 events from OpenAI
Mode: STRICT

  ✗ Rejected 1/12: Celebrity spotted at coffee shop
    Reason: Impact level 'low' below threshold
  ✗ Rejected 2/12: Minor traffic accident in suburb
    Reason: Geographic scope too narrow
  ✗ Rejected 3/12: New movie trailer released
    Reason: Category 'Entertainment & Sports' is disabled

================================================================================
FILTERING RESULTS
================================================================================
✓ Accepted: 9 events
✗ Rejected: 3 events

📊 Rejection Breakdown:
   - Impact level 'low' below threshold: 1
   - Geographic scope too narrow: 1
   - Category 'Entertainment & Sports' is disabled: 1
================================================================================

✓ STEP 2b completed.
   Before filtering: 12 events
   After filtering: 9 events
   Filtered out: 3 events
```

### Key Metrics to Monitor

1. **Acceptance Rate**: (Accepted / Total) × 100%
   - Too high (>90%): Filters may be too lenient
   - Too low (<30%): Filters may be too strict

2. **Rejection Reasons**: Which filters are catching the most events

3. **Events Stored**: Are you getting enough quality events per run?

## Troubleshooting

### Problem: Too Few Events Getting Through

**Symptoms**: Most runs result in 0-2 events stored

**Solutions**:

1. **Reduce minimum impact level**:
   ```json
   "minimum_impact_level": "low"
   ```

2. **Increase allowed categories**:
   ```json
   "disabled_categories": []
   ```

3. **Lower quality score threshold**:
   ```json
   "minimum_research_score": 30
   ```

4. **Broaden geographic scope**:
   ```json
   "minimum_geographic_scope": "local"
   ```

5. **Switch to balanced mode**:
   ```json
   "mode": "balanced"
   ```

### Problem: Still Getting Trivial Events

**Symptoms**: Low-quality events in database

**Solutions**:

1. **Increase minimum impact level**:
   ```json
   "minimum_impact_level": "high"
   ```

2. **Add more blacklist keywords**:
   ```json
   "keywords": [
     ...existing,
     "your-keyword-here"
   ]
   ```

3. **Raise quality score threshold**:
   ```json
   "minimum_research_score": 50
   ```

4. **Tighten impact metrics**:
   ```json
   "medium_level": {
     "affected_min": 50000  // Increase from 10000
   }
   ```

5. **Enable stricter deduplication**:
   ```json
   "similarity_threshold": 0.75  // Decrease from 0.85
   ```

### Problem: Duplicates Still Getting Through

**Symptoms**: Same event stored multiple times

**Solutions**:

1. **Lower similarity threshold**:
   ```json
   "similarity_threshold": 0.70
   ```

2. **Increase check window**:
   ```json
   "check_within_hours": 168  // 7 days instead of 48 hours
   ```

3. **Check database manually**:
   ```sql
   SELECT title, date, COUNT(*)
   FROM events
   GROUP BY title, date
   HAVING COUNT(*) > 1;
   ```

## Testing Your Configuration

### Option 1: Test Locally

```bash
# Run collection with your config
python collect_events_with_cosmic_state.py --lookback-hours 12

# Watch the filtering output
# Adjust config/event_filters.json
# Run again
```

### Option 2: Test Filter Module Directly

```bash
# Run the filter test
python event_quality_filter.py

# This tests with sample events and shows filtering behavior
```

### Option 3: Disable Filtering Temporarily

To compare results with/without filtering:

```json
{
  "filtering_mode": {
    "enabled": false  // Temporarily disable
  }
}
```

## Advanced Configuration

### Custom Impact Metrics for Specific Categories

While not directly supported in JSON, you can modify `event_quality_filter.py`:

```python
def _check_impact_metrics(self, event: Dict) -> bool:
    # Add custom logic here
    if event.get('category') == 'Technology & Innovation':
        # Require higher thresholds for tech events
        pass
```

### Priority Scoring

Events are automatically prioritized by:
1. Impact level (critical > high > medium > low)
2. Research quality score

Top events are kept when exceeding collection limits.

## File Locations

- **Configuration**: `config/event_filters.json`
- **Filter Logic**: `event_quality_filter.py`
- **Collection Script**: `collect_events_with_cosmic_state.py` (lines 1293-1342)
- **This Guide**: `EVENT_FILTERING_GUIDE.md`

## API Reference

### EventQualityFilter Class

```python
from event_quality_filter import EventQualityFilter, apply_event_filters

# Initialize with config
filter = EventQualityFilter(config=my_config)

# Apply filters
filtered_events, stats = filter.filter_events(
    events=detected_events,
    existing_events=recent_events_from_db
)

# Or use convenience function
filtered_events, stats = apply_event_filters(
    events=detected_events,
    existing_events=recent_events_from_db
)
```

### Filter Statistics

```python
stats = {
    'total': 12,
    'filtered': 9,
    'rejected': 3,
    'rejection_reasons': {
        'Impact level below threshold': 1,
        'Geographic scope too narrow': 1,
        'Category disabled': 1
    }
}
```

## Best Practices

1. **Start Strict, Then Adjust**: Begin with strict filters and loosen if needed
2. **Monitor Regularly**: Check filtering stats in GitHub Actions logs
3. **Update Blacklist**: Add keywords as you notice patterns in trivial events
4. **Balance Quality vs Quantity**: Aim for 5-10 high-quality events per run
5. **Test Changes**: Manually test config changes before committing
6. **Document Custom Rules**: If you add custom filters, document them

## Impact on Email Notifications

Filtered events affect your email summaries:
- **2-Hour Summaries**: Show only filtered events
- **Daily Summaries**: Aggregate filtered events from the day
- **Statistics**: "Events Stored" reflects post-filtering count

## Recommended Settings by Use Case

### For Astrological Research (Maximum Quality)

```json
{
  "mode": "strict",
  "minimum_impact_level": "high",
  "minimum_research_score": 60,
  "minimum_geographic_scope": "national"
}
```

### For News Tracking (Balanced Coverage)

```json
{
  "mode": "balanced",
  "minimum_impact_level": "medium",
  "minimum_research_score": 40,
  "minimum_geographic_scope": "state"
}
```

### For Personal Interest (More Events)

```json
{
  "mode": "lenient",
  "minimum_impact_level": "low",
  "minimum_research_score": 30,
  "minimum_geographic_scope": "local"
}
```

## Summary

The Event Quality Filtering System ensures your Cosmic Diary database contains only significant, research-worthy events. By adjusting `config/event_filters.json`, you have complete control over what gets stored.

**Key Benefits**:
- ✅ Filters out trivial/celebrity/gossip news
- ✅ Prevents duplicate events
- ✅ Ensures minimum significance thresholds
- ✅ Configurable without code changes
- ✅ Detailed filtering statistics
- ✅ Special rules for important categories

**Default Configuration**: Balanced mode with medium+ impact, state+ scope, and Entertainment disabled

For questions or issues, check the troubleshooting section or examine the filtering logs in your GitHub Actions runs.
