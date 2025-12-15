# Email Notifications Setup Guide

## Overview

The GitHub Actions workflow can send email summaries after each event collection run. This guide explains how to enable and configure email notifications.

## Current Status

✅ Email system is implemented and functional
⚠️ Email notifications are DISABLED by default
📧 Requires configuration in GitHub repository settings

## What You'll Receive

After each 2-hour event collection run, you'll get an email like this:

```
Subject: 🌟 Cosmic Diary: Event Collection Summary - 2025-12-15 12:30:00 UTC

Status: ✅ SUCCESS

Collection Time: 2025-12-15 12:30:00 UTC

Statistics:
- Events Detected: 5
- Events Stored: 5
- Correlations Created: 45  (includes planetary correlations)
- Avg Correlation Score: 72.50/100

This is an automated notification from Cosmic Diary event collection system.
```

## Setup Instructions

### Step 1: Get Email Credentials

#### For Gmail:
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication (required)
3. Go to https://myaccount.google.com/apppasswords
4. Create a new app password for "Cosmic Diary"
5. Copy the 16-character password (you'll need it for Step 2)

#### For Other Email Providers:
- **Outlook/Hotmail**: Use your regular password
- **Yahoo**: Create an app password at https://login.yahoo.com/account/security
- **Custom SMTP**: Get credentials from your email host

### Step 2: Add GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each of the following:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `SMTP_SERVER` | Your email provider's SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (usually 587) | `587` |
| `EMAIL_USER` | Your email address | `your.email@gmail.com` |
| `EMAIL_PASSWORD` | App password from Step 1 | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | Where to send summaries | `your.email@gmail.com` |

### Step 3: Enable Notifications

1. In GitHub, go to **Settings** → **Secrets and variables** → **Actions**
2. Click the **Variables** tab
3. Click **New repository variable**
4. Name: `ENABLE_EMAIL_NOTIFICATIONS`
5. Value: `true`
6. Click **Add variable**

### Step 4: Test It

1. Go to **Actions** → **Event Collection with Cosmic State - Every 2 Hours**
2. Click **Run workflow**
3. Select branch: `main`
4. Click **Run workflow**
5. Wait 5-10 minutes
6. Check your inbox for the summary email

## Email Providers

### Gmail
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```
- **Requires**: App password (see Step 1)
- **Security**: Enable 2FA first

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```
- **Requires**: Regular account password
- **Security**: May need to enable "less secure app access"

### Yahoo
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```
- **Requires**: App password
- **Security**: Enable 2FA first

### Custom SMTP
```
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587 (or 465 for SSL)
```
- **Requires**: Contact your email host for settings

## Troubleshooting

### "Email notification failed"

**Check these:**
1. All secrets are added correctly (no typos)
2. Email password is the **app password**, not your regular password (for Gmail/Yahoo)
3. SMTP_PORT is a number: `587` (not `"587"`)
4. Firewall allows outbound connections on port 587
5. Email provider hasn't flagged automated emails as spam

### "No email received"

**Try this:**
1. Check spam/junk folder
2. Verify `RECIPIENT_EMAIL` is correct
3. Test with manual workflow run (see Step 4)
4. Check GitHub Actions logs for errors

### "Authentication failed"

**For Gmail:**
- Make sure 2FA is enabled
- Use app password (16 characters), not regular password
- Don't include spaces in the app password

**For Other Providers:**
- Verify SMTP server and port are correct
- Check if "less secure app access" needs to be enabled

## Email Features

### Success Email Includes:
- ✅ Events detected count
- ✅ Events stored count
- ✅ Correlations created (includes planetary)
- ✅ Average correlation score
- ✅ Collection timestamp
- ✅ Pretty HTML formatting

### Failure Email Includes:
- ❌ Error message
- ❌ Stack trace (if available)
- ❌ Timestamp
- ❌ Helps diagnose issues quickly

## Disable Notifications

To turn off emails:
1. Go to **Settings** → **Secrets and variables** → **Actions** → **Variables**
2. Find `ENABLE_EMAIL_NOTIFICATIONS`
3. Click **...** → **Delete**

Or change the value to `false`.

## Schedule

Emails are sent:
- **Every 2 hours** (when workflow runs)
- **Times**: 00:30, 02:30, 04:30, 06:30, 08:30, 10:30, 12:30, 14:30, 16:30, 18:30, 20:30, 22:30 UTC
- **On manual runs** (via workflow_dispatch)

## Privacy & Security

- Email credentials are stored securely in GitHub Secrets
- Secrets are never exposed in logs or code
- Only authorized repository collaborators can view/edit secrets
- Emails are sent via encrypted TLS connection (port 587)
- No sensitive event data is included in emails (only statistics)

## Summary

1. ✅ Get app password from your email provider
2. ✅ Add 5 secrets to GitHub (SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL)
3. ✅ Add 1 variable to GitHub (ENABLE_EMAIL_NOTIFICATIONS = true)
4. ✅ Test with manual workflow run
5. ✅ Receive email summaries every 2 hours!

Need help? Check the troubleshooting section or review GitHub Actions logs.
