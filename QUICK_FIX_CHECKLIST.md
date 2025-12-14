# ✅ GitHub Actions Zero Data - Quick Fix Checklist

**Use this checklist to debug why GitHub Actions shows zeros.**

---

## 1️⃣ Verify GitHub Secrets (Start Here!)

**Go to**: Repository → Settings → Secrets and variables → Actions

Check these secrets exist:

- [ ] `OPENAI_API_KEY` - Starts with `sk-proj-`
- [ ] `SUPABASE_URL` - Ends with `.supabase.co`
- [ ] `SUPABASE_SERVICE_ROLE_KEY` - Long key (service role, not anon)
- [ ] `NEWSAPI_KEY` - Optional, for better event detection

**Missing secrets? Add them in GitHub Settings and re-run workflow.**

---

## 2️⃣ Check Latest Workflow Run

**Go to**: GitHub → Actions → Latest run

- [ ] Click "Run cosmic state collection with event correlation"
- [ ] Look for error messages (lines with `❌` or `ERROR`)
- [ ] Check if script reached the end (should say "completed successfully")

**Found errors?** See [GITHUB_ACTIONS_DEBUGGING_GUIDE.md](./GITHUB_ACTIONS_DEBUGGING_GUIDE.md)

---

## 3️⃣ Run Diagnostic Script

**Add this step to `.github/workflows/event-collection.yml`** (after line 31):

```yaml
- name: Run Diagnostics
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
    NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
  run: |
    python3 diagnose_github_actions.py
```

**Then**: Commit, push, and manually trigger workflow.

- [ ] All checks pass? → Script should work, check logs for actual errors
- [ ] Some checks fail? → Fix the failing components (usually secrets)

---

## 4️⃣ Download and Check Log Artifact

**Go to**: Workflow run page → Bottom → Artifacts section

- [ ] Download `event-collection-logs-XXXXX.zip`
- [ ] Extract and open `collection_output.log`
- [ ] Search for: `EVENTS_DETECTED=` (should show a number, not missing)
- [ ] Search for: `ERROR` (should show what went wrong)

---

## 5️⃣ Test Locally

**Run these commands** in your terminal:

```bash
# 1. Set environment variables
export OPENAI_API_KEY="your_key_here"
export SUPABASE_URL="your_url_here"
export SUPABASE_SERVICE_ROLE_KEY="your_key_here"

# 2. Run collection script
python3 collect_events_with_cosmic_state.py --lookback-hours 12 2>&1 | tee test.log

# 3. Check output
grep "EVENTS_DETECTED=" test.log
```

- [ ] Works locally? → GitHub Actions environment variable issue
- [ ] Fails locally? → Check error message, fix code/config

---

## 🎯 Common Issues & Fixes

### Issue: "OpenAI client not initialized"

**Fix**: Add `OPENAI_API_KEY` to GitHub Secrets
```
Repository → Settings → Secrets and variables → Actions → New secret
Name: OPENAI_API_KEY
Value: sk-proj-xxxxxxxxxxxxx
```

### Issue: "Supabase connection failed"

**Fix**: Verify you're using **service role key**, not anon key
```
Supabase Dashboard → Settings → API → service_role key (secret)
```

### Issue: "Prompt system not available"

**Fix**: Commit and push all files
```bash
git add prompts/event_detection_prompt.py
git commit -m "fix: Add prompt system file"
git push
```

### Issue: "No events detected" (legitimate)

**This is normal** if no significant events occurred in the 12-hour window.

**Options**:
- Increase lookback to 24 hours (in workflow file: `EVENT_LOOKBACK_HOURS: '24'`)
- Set up NewsAPI for real-time news (`./setup_newsapi.sh`)

---

## 📊 What Success Looks Like

When everything works, you should see:

```
📊 Parsed Statistics:
  Events Detected: 15      ← Not zero!
  Events Stored: 15
  Correlations Created: 12
  Avg Score: 0.73
```

---

## 🆘 Still Having Issues?

1. **Read**: [GITHUB_ACTIONS_DEBUGGING_GUIDE.md](./GITHUB_ACTIONS_DEBUGGING_GUIDE.md)
2. **Run**: `python3 diagnose_github_actions.py` (in GitHub Actions)
3. **Check**: Downloaded log artifact for detailed errors
4. **Test**: Run script locally to isolate the issue

---

**Most Common Fix**: Add missing secrets in GitHub repository settings. 90% of issues are due to missing `OPENAI_API_KEY` or `SUPABASE_SERVICE_ROLE_KEY`.
