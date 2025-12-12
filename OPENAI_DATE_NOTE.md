# ⚠️ OpenAI Date Limitation Note

## Issue

OpenAI models have a **knowledge cutoff date**. If you request events for dates after this cutoff, OpenAI will return empty results because it has no information about future events.

## Solution

### Use Historical Dates

OpenAI works best with dates **before its knowledge cutoff**. Typical cutoffs:
- **GPT-4o-mini**: Usually up to April 2024 or later (check OpenAI docs for exact date)
- **GPT-4**: Similar knowledge cutoff

### Recommended Dates

For testing, use dates that are definitely in the past:
- **2024 dates**: Most reliable
- **Early 2025**: May work if within knowledge cutoff
- **December 2025**: Likely beyond cutoff - will return empty

### Example

```bash
# ✅ Good - Historical date
./run_event_job.sh 2024-12-10

# ✅ Good - Recent past (within cutoff)
./run_event_job.sh 2024-11-15

# ❌ May fail - Too recent/future
./run_event_job.sh 2025-12-11
```

## Workaround for Recent/Future Dates

If you need events for recent dates that are beyond OpenAI's knowledge cutoff:

1. **Use News APIs** instead of OpenAI
2. **Manually create events** via the UI (`/events/new`)
3. **Wait for OpenAI model update** with newer knowledge cutoff
4. **Use a different date** that's within the cutoff

## How to Check Knowledge Cutoff

The script now warns you if:
- Date is in the future (no real events possible)
- OpenAI returns empty response (likely beyond cutoff)
- Response is too short (indicates empty result)

## Quick Fix

Run with a historical date:
```bash
./run_event_job.sh 2024-12-10
```

This should work reliably and return actual events!

