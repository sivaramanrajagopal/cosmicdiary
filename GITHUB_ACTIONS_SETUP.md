# 🔧 GitHub Actions Configuration Guide

## Overview

This guide will help you configure GitHub Actions for automated event collection and cosmic state capture.

**Current Workflow**: Event Collection with Cosmic State - Runs every 2 hours

---

## 📋 Prerequisites

1. ✅ GitHub repository (`sivaramanrajagopal/cosmicdiary`)
2. ✅ GitHub account with admin access to the repository
3. ✅ All required services set up:
   - Supabase project
   - Railway backend
   - OpenAI API key
   - Email credentials (optional)

---

## 🔐 Step 1: Configure GitHub Secrets

Go to: **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions** → **Secrets**

### Required Secrets:

Click **"New repository secret"** for each:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `OPENAI_API_KEY` | `sk-...` | OpenAI API key for event detection |
| `SUPABASE_URL` | `https://xxx.supabase.co` | Your Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJ...` | Supabase service role key (NOT anon key) |
| `FLASK_API_URL` | `https://cosmicdiary-production.up.railway.app` | Railway backend URL |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP server for email notifications |
| `SMTP_PORT` | `587` | SMTP port (usually 587 for Gmail) |
| `EMAIL_USER` | `your-email@gmail.com` | Email address for sending notifications |
| `EMAIL_PASSWORD` | `your-app-password` | Gmail app password (NOT regular password) |
| `RECIPIENT_EMAIL` | `recipient@example.com` | Email address to receive notifications |

### 📝 How to Get Each Secret:

#### 1. OpenAI API Key
- Go to: https://platform.openai.com/api-keys
- Create new API key
- Copy the key (starts with `sk-`)

#### 2. Supabase URL & Service Role Key
- Go to: Supabase Dashboard → Project Settings → API
- **URL**: Copy "Project URL"
- **Service Role Key**: Copy "service_role" key (⚠️ Keep this secret!)
  - This is different from the anon key
  - Has full access to your database

#### 3. Railway Backend URL
- Go to: Railway Dashboard → Your Service → Settings → Networking
- Copy the **Public Domain** URL
- Example: `https://cosmicdiary-production.up.railway.app`

#### 4. Email Credentials (Gmail)
- **Email User**: Your Gmail address
- **App Password** (NOT your regular password):
  1. Go to: https://myaccount.google.com/apppasswords
  2. Select "Mail" and "Other (Custom name)"
  3. Name it "GitHub Actions"
  4. Copy the 16-character password
  5. Use this as `EMAIL_PASSWORD`

---

## 🎛️ Step 2: Configure GitHub Variables (Optional)

Go to: **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions** → **Variables**

Click **"New repository variable"**:

| Variable Name | Value | Purpose |
|---------------|-------|---------|
| `ENABLE_EMAIL_NOTIFICATIONS` | `true` | Enable/disable email notifications |

**Note**: Set to `false` to disable email notifications (emails won't be sent even if secrets are configured)

---

## 📂 Step 3: Verify Workflow File

The workflow file is located at:
```
.github/workflows/event-collection.yml
```

**Current Schedule**: Runs every 2 hours at :30 past the hour (e.g., 00:30, 02:30, 04:30)

**Manual Trigger**: You can also trigger manually from the Actions tab → "Run workflow"

---

## ✅ Step 4: Test the Workflow

### Option 1: Manual Trigger (Recommended for Testing)

1. Go to: **GitHub Repository** → **Actions** tab
2. Click on **"Event Collection with Cosmic State - Every 2 Hours"**
3. Click **"Run workflow"** button (top right)
4. Select branch: `main`
5. Click **"Run workflow"**

### Option 2: Wait for Scheduled Run

The workflow will automatically run:
- Every 2 hours at :30 past the hour
- First run: Next :30 minute mark (e.g., if it's 14:15, next run is 14:30)

### Check Workflow Status:

1. Go to: **Actions** tab
2. Click on the workflow run
3. Expand each step to see logs
4. ✅ Green checkmark = Success
5. ❌ Red X = Failure (check logs for errors)

---

## 🔍 Step 5: Verify Success

After a successful run, you should see:

### In GitHub Actions:
- ✅ All steps completed with green checkmarks
- No errors in logs

### In Supabase:
1. Check `events` table for new events
2. Check `cosmic_snapshots` table for new snapshots
3. Check `event_cosmic_correlations` table for correlations

### In Email (if enabled):
- Success notification email with statistics

---

## 🐛 Troubleshooting

### Issue: Workflow Fails with "Secret not found"

**Error**: `Secret 'OPENAI_API_KEY' is not set`

**Solution**:
1. Go to Settings → Secrets and variables → Actions → Secrets
2. Verify all required secrets are added
3. Check secret names match exactly (case-sensitive)
4. Try running workflow again

### Issue: Script Fails - "Module not found"

**Error**: `ModuleNotFoundError: No module named 'pyswisseph'`

**Solution**:
- The workflow installs dependencies automatically
- Check the "Install dependencies" step in logs
- If still failing, verify Python version matches (currently 3.10)

### Issue: Database Connection Error

**Error**: `Connection refused` or `Authentication failed`

**Solution**:
1. Verify `SUPABASE_URL` is correct (no trailing slash)
2. Verify `SUPABASE_SERVICE_ROLE_KEY` is the service role key (not anon key)
3. Check Supabase project is active (not paused)
4. Verify network access in Supabase settings

### Issue: OpenAI API Error

**Error**: `401 Unauthorized` or `Invalid API key`

**Solution**:
1. Verify `OPENAI_API_KEY` is correct
2. Check OpenAI account has credits/usage
3. Verify API key hasn't been revoked
4. Try creating a new API key

### Issue: Email Not Sending

**Error**: `SMTP authentication failed`

**Solution**:
1. Use **App Password** (not regular Gmail password)
2. Verify `EMAIL_USER` is correct Gmail address
3. Verify `EMAIL_PASSWORD` is the 16-character app password
4. Check `SMTP_SERVER` is `smtp.gmail.com`
5. Check `SMTP_PORT` is `587`
6. Verify `ENABLE_EMAIL_NOTIFICATIONS` variable is set to `true`

### Issue: Railway Backend Not Accessible

**Error**: `Connection refused` or `Timeout`

**Solution**:
1. Verify `FLASK_API_URL` is the public Railway URL
2. Test Railway URL directly: `curl https://cosmicdiary-production.up.railway.app/health`
3. Check Railway service is running (not sleeping)
4. Verify Railway service status in Railway dashboard

---

## 📊 Workflow Schedule

**Current Schedule**: Every 2 hours at :30 past the hour

**Cron Expression**: `30 */2 * * *`

**Examples**:
- 00:30 UTC
- 02:30 UTC
- 04:30 UTC
- 06:30 UTC
- ... and so on

**To Change Schedule**:
1. Edit `.github/workflows/event-collection.yml`
2. Modify the `cron` expression
3. Commit and push changes
4. GitHub Actions will use the new schedule

**Common Cron Examples**:
- Every hour: `0 * * * *`
- Every 2 hours: `0 */2 * * *`
- Every 4 hours: `0 */4 * * *`
- Daily at 6 AM: `0 6 * * *`
- Twice daily (6 AM and 6 PM): `0 6,18 * * *`

---

## 🔒 Security Best Practices

1. ✅ **Never commit secrets** to the repository
2. ✅ **Use GitHub Secrets** for all sensitive data
3. ✅ **Use Service Role Key** (not anon key) for GitHub Actions
4. ✅ **Regularly rotate** API keys and passwords
5. ✅ **Monitor workflow logs** for security issues
6. ✅ **Limit access** to repository settings

---

## 📝 Workflow Summary

**What the Workflow Does**:

1. ✅ Checks out code from repository
2. ✅ Sets up Python 3.10 environment
3. ✅ Installs dependencies (pyswisseph, supabase, openai, etc.)
4. ✅ Runs `collect_events_with_cosmic_state.py`:
   - Captures current cosmic state (planetary positions)
   - Detects events via OpenAI
   - Calculates event charts
   - Correlates events with cosmic state
   - Stores everything in Supabase
5. ✅ Extracts statistics
6. ✅ Sends email notifications (if enabled)
7. ✅ Uploads logs as artifacts
8. ✅ Creates GitHub issue on failure

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Expression Generator](https://crontab.guru/)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Railway Documentation](https://docs.railway.app/)
- [Supabase Documentation](https://supabase.com/docs)

---

## ✅ Configuration Checklist

- [ ] All required secrets added to GitHub
- [ ] `ENABLE_EMAIL_NOTIFICATIONS` variable set (optional)
- [ ] Workflow file exists at `.github/workflows/event-collection.yml`
- [ ] Tested workflow manually
- [ ] Verified workflow runs successfully
- [ ] Checked Supabase for new data
- [ ] Email notifications working (if enabled)
- [ ] Scheduled runs working correctly

---

**Last Updated**: 2025-12-12

**Need Help?** Check workflow logs in the Actions tab for detailed error messages.

