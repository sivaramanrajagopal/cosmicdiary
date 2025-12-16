# Event Filtering - Quick Reference

## 🎯 Quick Start

**Configuration File**: `config/event_filters.json`

**To adjust filtering**: Edit the JSON file, no code changes needed!

## ⚙️ Most Common Adjustments

### 1. Make Filtering More Strict

```json
{
  "impact_level_filters": {
    "minimum_impact_level": "high"
  },
  "quality_scoring": {
    "minimum_research_score": 60
  }
}
```

### 2. Make Filtering More Lenient

```json
{
  "impact_level_filters": {
    "minimum_impact_level": "low"
  },
  "quality_scoring": {
    "minimum_research_score": 30
  }
}
```

### 3. Disable a Category (e.g., Entertainment)

```json
{
  "category_filters": {
    "disabled_categories": [
      "Entertainment & Sports"
    ]
  }
}
```

### 4. Only National/International Events

```json
{
  "geographic_filters": {
    "minimum_geographic_scope": "national"
  }
}
```

### 5. Add Keyword to Blacklist

```json
{
  "keyword_filters": {
    "blacklist": {
      "keywords": [
        ...existing keywords,
        "your-new-keyword"
      ]
    }
  }
}
```

### 6. Temporarily Disable All Filtering

```json
{
  "filtering_mode": {
    "enabled": false
  }
}
```

## 📊 Filter Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| `strict` | High quality only | Astrological research |
| `balanced` | Good quality (default) | General use |
| `lenient` | More permissive | Testing, need more events |

## 🎚️ Impact Levels

| Level | Threshold Examples |
|-------|-------------------|
| `critical` | 100+ deaths OR $1B+ impact OR 1M+ affected |
| `high` | 10-100 deaths OR $100M-$1B impact OR 100K-1M affected |
| `medium` | 1-10 deaths OR $10M-$100M impact OR 10K-100K affected |
| `low` | Lower than medium (usually filtered out) |

## 🗂️ Geographic Scopes

| Scope | Description |
|-------|-------------|
| `local` | City/district level |
| `state` | State/province level (default minimum) |
| `national` | Country level |
| `international` | Multi-country |

## 🚫 Default Blacklisted Keywords

- celebrity gossip
- social media trend
- viral video
- influencer
- box office collection
- movie review
- fashion show
- beauty pageant
- sports match result
- minor traffic accident
- local protest
- routine inspection

## 🔍 Monitoring Filter Performance

Check GitHub Actions logs for:

```
FILTERING RESULTS
✓ Accepted: X events
✗ Rejected: Y events

📊 Rejection Breakdown:
   - Reason 1: count
   - Reason 2: count
```

**Ideal acceptance rate**: 50-80%
- Too high (>90%): Filters too lenient
- Too low (<30%): Filters too strict

## 🛠️ Troubleshooting

### Problem: Getting too few events

**Solution**: Lower thresholds
```json
{
  "impact_level_filters": {"minimum_impact_level": "low"},
  "quality_scoring": {"minimum_research_score": 30},
  "geographic_filters": {"minimum_geographic_scope": "local"}
}
```

### Problem: Still getting trivial events

**Solution**: Raise thresholds
```json
{
  "impact_level_filters": {"minimum_impact_level": "high"},
  "quality_scoring": {"minimum_research_score": 50},
  "category_filters": {"disabled_categories": ["Entertainment & Sports"]}
}
```

### Problem: Duplicates getting through

**Solution**: Tighten deduplication
```json
{
  "deduplication": {
    "similarity_threshold": 0.70,
    "check_within_hours": 168
  }
}
```

## 📍 File Locations

- **Config**: `config/event_filters.json`
- **Full Guide**: `EVENT_FILTERING_GUIDE.md`
- **Filter Code**: `event_quality_filter.py`
- **Collection Script**: `collect_events_with_cosmic_state.py`

## 🧪 Testing Your Changes

```bash
# Test the filter directly
python3 event_quality_filter.py

# Run collection with your settings
python3 collect_events_with_cosmic_state.py --lookback-hours 12
```

## 💡 Pro Tips

1. **Start strict, adjust later**: Easier to loosen than tighten
2. **Monitor for 2-3 runs**: See pattern before adjusting
3. **Update blacklist regularly**: Add keywords as you notice patterns
4. **Aim for 5-10 events per run**: Sweet spot for quality
5. **Critical events bypass filters**: Important events always get through

## 🎯 Recommended Settings

**For Research (High Quality)**:
- Mode: `strict`
- Impact: `high`
- Score: `60`
- Scope: `national`

**For General Use (Balanced)**:
- Mode: `balanced`
- Impact: `medium`
- Score: `40`
- Scope: `state`

**For Testing (More Events)**:
- Mode: `lenient`
- Impact: `low`
- Score: `30`
- Scope: `local`

---

For detailed information, see **EVENT_FILTERING_GUIDE.md**
