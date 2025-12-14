# 🔍 GitHub Actions Zero Data - Debugging Guide

**Issue**: GitHub Actions workflow shows zeros for all statistics despite proper code setup.

**Last Updated**: December 14, 2025

---

## ✅ Code Verification (Already Done)

The code is **correctly configured**:
- ✅ Python script outputs proper format (`EVENTS_DETECTED=N`)
- ✅ Workflow parses logs correctly with grep/sed
- ✅ Output format test passed (`test_github_actions_output.py`)

**This means the issue is likely in GitHub Actions execution, not the code.**

---

## 🎯 Most Likely Causes

### 1. Script Errors Before Output (90% probability)

**Problem**: Script crashes or exits before reaching the output section.

**How to check**:
1. Go to GitHub → Actions → Latest workflow run
2. Click on "Run cosmic state collection with event correlation" step
3. Look for errors **before** the statistics section

**Common errors to look for**:
```
❌ ERROR: OpenAI client not initialized
❌ ERROR: Prompt system not available
❌ ERROR: OPENAI_API_KEY environment variable not set
❌ ERROR: Supabase connection failed
```

### 2. Missing Environment Variables (80% probability)

**Problem**: Required secrets not set in GitHub repository.

**How to check**:
1. Go to Repository Settings → Secrets and variables → Actions
2. Verify these secrets exist:
   - `OPENAI_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `NEWSAPI_KEY` (optional)

**How to fix**:
- Add missing secrets in GitHub Settings
- Make sure there are no extra spaces in secret values
- Verify API keys are active and not expired

### 3. Script Legitimately Detects Zero Events (20% probability)

**Problem**: OpenAI returns 0 events for the time window.

**How to check**:
Look for this in the logs:
```
⚠️  No events detected. Exiting.
   This is normal if:
   - No significant events occurred in the time window
   - OpenAI returned 0 events (check logs above)
```

---

## 🔍 Step-by-Step Debugging Process

### Step 1: Check GitHub Actions Logs

1. **Go to**: GitHub → Your Repository → Actions tab
2. **Click on**: Latest "Event Collection" workflow run
3. **Expand**: "Run cosmic state collection with event correlation" step
4. **Look for**: Any error messages or warnings

**What to look for**:
```bash
# GOOD SIGNS (script ran successfully):
✓ STEP 1 completed. Snapshot ID: 123
✓ STEP 2 completed. Events detected: 15
✓ Events Stored: 15

# BAD SIGNS (script failed):
❌ ERROR: ...
Traceback (most recent call last):
```

### Step 2: Download Log Artifact

GitHub Actions automatically uploads logs as artifacts.

1. **Go to**: Workflow run page (bottom of page)
2. **Look for**: "Artifacts" section
3. **Download**: `event-collection-logs-XXXXX.zip`
4. **Extract and open**: `collection_output.log`

**Search for**:
```bash
# Search for these patterns in the log:
grep "EVENTS_DETECTED=" collection_output.log
grep "ERROR" collection_output.log
grep "❌" collection_output.log
```

### Step 3: Verify Environment Variables

**Run this in GitHub Actions** (one-time debug):

Add a temporary step to your workflow:

```yaml
- name: Debug Environment Variables
  run: |
    echo "Checking environment variables..."
    echo "OPENAI_API_KEY is set: $([[ -n "$OPENAI_API_KEY" ]] && echo "YES" || echo "NO")"
    echo "SUPABASE_URL is set: $([[ -n "$SUPABASE_URL" ]] && echo "YES" || echo "NO")"
    echo "SUPABASE_SERVICE_ROLE_KEY is set: $([[ -n "$SUPABASE_SERVICE_ROLE_KEY" ]] && echo "YES" || echo "NO")"
    echo "NEWSAPI_KEY is set: $([[ -n "$NEWSAPI_KEY" ]] && echo "YES" || echo "NO")"
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
    NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
```

**Expected output**:
```
OPENAI_API_KEY is set: YES
SUPABASE_URL is set: YES
SUPABASE_SERVICE_ROLE_KEY is set: YES
NEWSAPI_KEY is set: YES (or NO if not configured)
```

### Step 4: Test Locally First

Before debugging GitHub Actions, verify the script works locally:

```bash
# Set environment variables
export OPENAI_API_KEY="your_key_here"
export SUPABASE_URL="your_url_here"
export SUPABASE_SERVICE_ROLE_KEY="your_key_here"
export NEWSAPI_KEY="your_key_here"  # Optional

# Run the script with verbose output
python3 collect_events_with_cosmic_state.py --lookback-hours 12 2>&1 | tee test_output.log

# Check for GitHub Actions output
grep "EVENTS_DETECTED=" test_output.log
```

**Expected output**:
```
EVENTS_DETECTED=15
EVENTS_STORED=15
CORRELATIONS_CREATED=12
AVG_CORRELATION_SCORE=0.73
```

If this works locally but not in GitHub Actions → Environment variable issue.

### Step 5: Check GitHub Actions Permissions

**Verify**: Repository Settings → Actions → General → Workflow permissions

Should be:
- ✅ Read and write permissions (or at least read for this workflow)

---

## 🐛 Common Error Scenarios

### Scenario 1: OpenAI API Key Not Set

**Error message**:
```
❌ ERROR: OpenAI client not initialized.
   Possible reasons:
   - OPENAI_API_KEY environment variable not set
```

**Fix**:
1. Go to Repository Settings → Secrets and variables → Actions
2. Add new secret: `OPENAI_API_KEY` = `sk-proj-...`
3. Re-run workflow

### Scenario 2: Supabase Connection Failed

**Error message**:
```
❌ ERROR: Supabase connection failed
```

**Fix**:
1. Verify `SUPABASE_URL` is correct (should end with `.supabase.co`)
2. Verify `SUPABASE_SERVICE_ROLE_KEY` is the **service role key**, not the anon key
3. Check Supabase dashboard for any service outages

### Scenario 3: Prompt System Not Available

**Error message**:
```
❌ ERROR: Prompt system not available. Cannot proceed with event detection.
   Check that prompts/event_detection_prompt.py exists and is importable
```

**Fix**:
1. Verify `prompts/event_detection_prompt.py` exists in your repository
2. Check if file was committed and pushed to GitHub
3. Run: `git status` and `git push` to ensure all files are synced

### Scenario 4: OpenAI Returns Zero Events

**Log shows**:
```
✓ STEP 1 completed. Snapshot ID: 123
🤖 Calling OpenAI API with enhanced astrological prompts...
📥 OpenAI response received
   Content length: 50 characters
⚠️  No events detected. Exiting.
```

**Fix**:
- This might be legitimate (no major events in 12-hour window)
- Try increasing lookback window to 24 hours:
  ```yaml
  EVENT_LOOKBACK_HOURS: '24'  # In workflow file
  ```
- Or set up NewsAPI for better event detection

### Scenario 5: Script Times Out

**Error message**:
```
Error: The operation was canceled.
```

**Fix**:
- Increase timeout in workflow:
  ```yaml
  timeout-minutes: 30  # Increase from 15 to 30
  ```

---

## 🧪 Quick Diagnostic Test

Run this command locally to test the **exact** workflow behavior:

```bash
# Simulate GitHub Actions execution
python3 collect_events_with_cosmic_state.py --lookback-hours 12 2>&1 | tee collection_output.log

# Parse statistics (same as workflow)
echo "Testing grep parsing..."
DETECTED=$(grep "EVENTS_DETECTED=" collection_output.log | tail -1 | sed 's/EVENTS_DETECTED=//')
STORED=$(grep "EVENTS_STORED=" collection_output.log | tail -1 | sed 's/EVENTS_STORED=//')
CORRELATIONS=$(grep "CORRELATIONS_CREATED=" collection_output.log | tail -1 | sed 's/CORRELATIONS_CREATED=//')
SCORE=$(grep "AVG_CORRELATION_SCORE=" collection_output.log | tail -1 | sed 's/AVG_CORRELATION_SCORE=//')

echo "Parsed statistics:"
echo "  Events Detected: $DETECTED"
echo "  Events Stored: $STORED"
echo "  Correlations: $CORRELATIONS"
echo "  Avg Score: $SCORE"
```

**Expected output** (if working):
```
Parsed statistics:
  Events Detected: 15
  Events Stored: 15
  Correlations: 12
  Avg Score: 0.73
```

**If you get empty values**, the grep parsing failed → Check log file manually.

---

## 📝 What to Report

If you still have issues after trying the above, provide:

1. **GitHub Actions log** (from "Run cosmic state collection" step)
2. **Downloaded log artifact** (`collection_output.log`)
3. **Environment variable check** results (YES/NO for each secret)
4. **Local test results** (does it work locally?)

---

## ✅ Quick Fix Checklist

- [ ] Verify GitHub Secrets are set (OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
- [ ] Check GitHub Actions logs for errors
- [ ] Download and inspect log artifact
- [ ] Test script locally with same environment variables
- [ ] Verify `prompts/event_detection_prompt.py` exists in repository
- [ ] Check if workflow has necessary permissions
- [ ] Try manual workflow trigger to see real-time logs

---

## 🎯 Most Likely Solutions (Try These First)

### Solution 1: Missing OPENAI_API_KEY

```bash
# In GitHub Repository Settings → Secrets and variables → Actions
# Add new secret:
Name: OPENAI_API_KEY
Value: sk-proj-xxxxxxxxxxxxxxxxxxxx
```

### Solution 2: Wrong Supabase Key Type

```bash
# Make sure you're using SERVICE ROLE KEY, not ANON KEY
# Service role key has admin permissions
# Find it in: Supabase Dashboard → Settings → API → service_role key
```

### Solution 3: Files Not Committed

```bash
# Make sure all files are pushed to GitHub
git add .
git commit -m "fix: Ensure all required files are committed"
git push
```

---

## 📚 Related Documentation

- **Workflow File**: `.github/workflows/event-collection.yml`
- **Collection Script**: `collect_events_with_cosmic_state.py`
- **Test Script**: `test_github_actions_output.py`
- **Setup Guide**: `SETUP_AND_TEST_GUIDE.md`

---

**Next Steps**: Follow the "Step-by-Step Debugging Process" above to identify the exact issue.
