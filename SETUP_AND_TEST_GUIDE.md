# 🚀 Complete Setup & Testing Guide

**Follow these steps to:**
1. ✅ Test GitHub Actions workflow
2. ✅ Set up News API integration
3. ✅ Optimize configuration settings

---

## 📋 STEP 1: Configure Optimal Settings (✅ DONE!)

**Status**: ✅ Already completed automatically!

**What was changed**:
- ✅ Lookback window: 2 hours → **12 hours** (better results)
- ✅ Added NEWSAPI_KEY environment variable support
- ✅ Updated command to use 12-hour window

**File modified**: `.github/workflows/event-collection.yml`

**You can verify**:
```bash
grep "EVENT_LOOKBACK_HOURS" .github/workflows/event-collection.yml
# Should show: EVENT_LOOKBACK_HOURS: '12'
```

---

## 📋 STEP 2: Set Up News API Integration

### Option A: Automated Setup (Recommended - 2 minutes)

```bash
# Run the automated setup script
./setup_newsapi.sh
```

**The script will**:
1. Guide you to get a free API key
2. Add it to `.env.local`
3. Test the connection
4. Show you sample headlines

### Option B: Manual Setup (3 minutes)

**Step 2.1: Get API Key**
1. Go to https://newsapi.org/register
2. Fill out the form:
   - Name: Your name
   - Email: Your email
   - Password: Choose a password
3. Click "Submit"
4. Check your email for verification
5. Log in and find your API key

**Step 2.2: Add to .env.local**
```bash
# Add this line to .env.local
echo "NEWSAPI_KEY=your_api_key_here" >> .env.local
```

**Step 2.3: Test It**
```bash
python3 -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')
api_key = os.getenv('NEWSAPI_KEY')
print(f'API Key loaded: {api_key[:10]}...')

url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
response = requests.get(url)
data = response.json()

if data['status'] == 'ok':
    print(f'✅ SUCCESS! Found {len(data[\"articles\"])} articles')
else:
    print(f'❌ Error: {data.get(\"message\")}')"
```

### Verify News API Integration

```bash
# Test the full integration
python3 collect_events_with_cosmic_state.py --lookback-hours 2
```

**You should see**:
```
🔄 Attempting NewsAPI integration first...
📰 ATTEMPTING NEWSAPI INTEGRATION
🔑 NewsAPI key detected: abcd1234...
📡 Fetching news from NewsAPI...
✅ NewsAPI returned 20 articles
✅ Using 20 events from NewsAPI
```

---

## 📋 STEP 3: Test GitHub Actions Workflow

### 3A: Commit and Push Changes

First, commit all the changes:

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "feat: Fix event collection statistics parsing and add News API integration

- Fixed GitHub Actions to show actual event counts (not hardcoded zeros)
- Implemented News API integration for real-time events
- Changed lookback window from 2 to 12 hours for better results
- Added comprehensive debugging and error handling
- Created diagnostic tools and documentation"

# Push to GitHub
git push origin main
```

### 3B: Trigger GitHub Actions Manually

**Step 3B.1: Navigate to Actions**
1. Go to your GitHub repository
2. Click on the **"Actions"** tab at the top

**Step 3B.2: Select Workflow**
1. On the left sidebar, click:
   **"Event Collection with Cosmic State - Every 2 Hours"**

**Step 3B.3: Run Workflow**
1. Click the **"Run workflow"** dropdown button (on the right)
2. Keep branch as "main"
3. Click **"Run workflow"** button
4. Page will refresh - you'll see a new yellow dot appear

**Step 3B.4: Watch the Logs**
1. Click on the running workflow (yellow dot or "in progress")
2. Click on the job: **"Collect Events and Capture Cosmic State"**
3. Expand each step to see logs

**What to look for**:

✅ **In "Run cosmic state collection"**:
```
STEP 1: CAPTURING COSMIC STATE
✓ Snapshot stored with ID: XX

STEP 2: DETECTING EVENTS VIA OPENAI
(or if NewsAPI is set up:)
🔄 Attempting NewsAPI integration first...
✅ NewsAPI returned 20 articles
✅ Using 20 events from NewsAPI

✓ Events Detected: 20
✓ Events Stored: 20
```

✅ **In "Extract collection statistics"**:
```
📊 Parsed Statistics:
  Events Detected: 20       ← Should NOT be zero!
  Events Stored: 20         ← Should NOT be zero!
  Correlations Created: 18
  Avg Correlation Score: 0.75
```

✅ **In "Report Success Statistics"**:
```
📊 Collection Statistics:
  • Events Detected: 20
  • Events Stored: 20
  • Correlations Created: 18
  • Average Correlation Score: 0.75
```

### 3C: Add NewsAPI Key to GitHub Secrets (If Using News API)

**Step 3C.1: Navigate to Secrets**
1. In your repository, click **"Settings"** tab
2. In left sidebar, click **"Secrets and variables"** → **"Actions"**

**Step 3C.2: Add New Secret**
1. Click **"New repository secret"** button
2. Name: `NEWSAPI_KEY`
3. Secret: Paste your NewsAPI key from `.env.local`
4. Click **"Add secret"**

**Step 3C.3: Re-run Workflow**
1. Go back to Actions tab
2. Run workflow again
3. This time it should use NewsAPI!

---

## 🎯 Expected Results

### Without News API (Using OpenAI)
```
ℹ️  NEWSAPI_KEY not set, using OpenAI
✓ Events Detected: 8-12
✓ Events Stored: 8-12
✓ Correlations Created: 6-10
```

### With News API (Real-time News)
```
🔄 Attempting NewsAPI integration first...
✅ Using 20 events from NewsAPI
✓ Events Detected: 20
✓ Events Stored: 20
✓ Correlations Created: 18
```

---

## 🧪 Testing Checklist

- [ ] **Configuration optimized** (12-hour lookback)
  ```bash
  grep "EVENT_LOOKBACK_HOURS: '12'" .github/workflows/event-collection.yml
  ```

- [ ] **News API set up locally**
  ```bash
  grep "NEWSAPI_KEY=" .env.local
  ```

- [ ] **News API tested locally**
  ```bash
  python3 collect_events_with_cosmic_state.py --lookback-hours 2
  # Should show: "🔄 Attempting NewsAPI integration first..."
  ```

- [ ] **Changes committed and pushed**
  ```bash
  git log -1 --oneline
  # Should show your commit message
  ```

- [ ] **GitHub Actions triggered manually**
  - [ ] Workflow ran successfully
  - [ ] Statistics show actual numbers (not zeros)
  - [ ] Events were stored in database

- [ ] **News API key added to GitHub Secrets** (optional but recommended)
  - Repository → Settings → Secrets → NEWSAPI_KEY exists

- [ ] **Verified in Supabase**
  - Check `events` table for new entries
  - Check `cosmic_snapshots` table
  - Check `event_cosmic_correlations` table

---

## 🐛 Troubleshooting

### Issue: "Still showing zero events in GitHub Actions"

**Check**:
1. Did you commit and push changes?
   ```bash
   git log -1 --oneline
   git push origin main
   ```

2. Is the workflow using the updated file?
   - Download `collection_output.log` artifact
   - Check if it says "EVENT_LOOKBACK_HOURS: '12'"

3. Check OpenAI API key is set in GitHub Secrets

### Issue: "NewsAPI not working locally"

**Check**:
```bash
# Verify key is in .env.local
grep NEWSAPI_KEY .env.local

# Test API key
python3 -c "
import os, requests
from dotenv import load_dotenv
load_dotenv('.env.local')
key = os.getenv('NEWSAPI_KEY')
print(f'Key: {key[:10]}...')
r = requests.get(f'https://newsapi.org/v2/top-headlines?country=in&apiKey={key}')
print(f'Status: {r.status_code}')
print(f'Articles: {len(r.json().get(\"articles\", []))}')"
```

### Issue: "GitHub Actions can't access NewsAPI"

**Check**:
1. Is `NEWSAPI_KEY` in GitHub Secrets?
   - Settings → Secrets and variables → Actions
   - Should see `NEWSAPI_KEY` listed

2. Does workflow reference it?
   ```yaml
   # In .github/workflows/event-collection.yml
   env:
     NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
   ```

---

## 📊 Performance Comparison

| Configuration | Events Expected | Quality | Speed |
|--------------|----------------|---------|-------|
| **Old (2hr, OpenAI)** | 0-5 | ❌ Low | ⚠️ Slow |
| **New (12hr, OpenAI)** | 8-15 | ✅ Good | ⚠️ Slow |
| **New (2hr, NewsAPI)** | 15-25 | ✅✅ Excellent | ✅ Fast |
| **New (12hr, NewsAPI)** | 20-40 | ✅✅ Excellent | ✅ Fast |

**Recommendation**: Use **NewsAPI with 2-12 hour window** for best results.

---

## 🎉 Success Criteria

You're done when:

1. ✅ Local test shows NewsAPI integration working
2. ✅ GitHub Actions shows actual event counts (not zeros)
3. ✅ Events are being stored in Supabase database
4. ✅ Statistics are displayed correctly in workflow logs

**Example successful output**:
```
📊 Parsed Statistics:
  Events Detected: 20
  Events Stored: 20
  Correlations Created: 18
  Avg Correlation Score: 0.72

✅ Event collection completed successfully!
```

---

## 🆘 Need Help?

1. **Run diagnostics**:
   ```bash
   python3 test_event_collection_setup.py
   ```

2. **Check recent changes**:
   ```bash
   git log --oneline -5
   git diff HEAD~1
   ```

3. **View documentation**:
   - `QUICK_REFERENCE.md` - Common commands
   - `FIXES_SUMMARY.md` - Technical details
   - `NEWS_API_INTEGRATION_GUIDE.md` - NewsAPI details

---

**Ready to start?**

**Quick Start**:
```bash
# 1. Set up NewsAPI (2 minutes)
./setup_newsapi.sh

# 2. Test locally (1 minute)
python3 collect_events_with_cosmic_state.py --lookback-hours 2

# 3. Commit and push (1 minute)
git add .
git commit -m "feat: Add News API integration and fix statistics"
git push

# 4. Test GitHub Actions (3 minutes)
# Go to GitHub → Actions → Run workflow
```

**Total time: ~7 minutes** 🚀
