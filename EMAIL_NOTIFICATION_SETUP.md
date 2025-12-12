# 📧 Email Notification Setup Guide

Complete guide to set up email notifications for GitHub Actions event collection.

---

## Current Status

**❌ Email notifications are NOT currently enabled** in the GitHub Actions workflow.

However, the code has been added and can be enabled by:
1. Setting up email secrets in GitHub
2. Enabling the feature via repository variable

---

## Features

✅ **Success Email**: Sent after successful event collection  
✅ **Failure Email**: Sent if collection fails  
✅ **Summary Statistics**: Events detected, stored, correlations created  
✅ **Error Details**: Included in failure emails

---

## Step 1: Set Up Email Provider (Gmail Example)

### 1.1 Enable App Password for Gmail

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (required for app passwords)
3. Go to **App passwords**
4. Create new app password:
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter: **Cosmic Diary GitHub Actions**
5. **Copy the 16-character password** (you'll need this for GitHub secrets)

### 1.2 Email Configuration

- **SMTP Server**: `smtp.gmail.com`
- **SMTP Port**: `587` (TLS) or `465` (SSL)
- **Email**: Your Gmail address (e.g., `your-email@gmail.com`)
- **Password**: The 16-character app password (not your Gmail password)

---

## Step 2: Configure GitHub Secrets

### 2.1 Add Email Secrets

Go to your GitHub repository:
1. **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add the following secrets:

**Required Secrets:**

```
SMTP_SERVER
Value: smtp.gmail.com
```

```
SMTP_PORT
Value: 587
```

```
EMAIL_USER
Value: your-email@gmail.com
```

```
EMAIL_PASSWORD
Value: your-16-character-app-password
```

```
RECIPIENT_EMAIL
Value: recipient@example.com
(Can be same as EMAIL_USER if sending to yourself)
```

### 2.2 Enable Email Notifications

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"Variables"** tab
3. Click **"New repository variable"**
4. Add:

```
Name: ENABLE_EMAIL_NOTIFICATIONS
Value: true
```

---

## Step 3: Test Email Notification

### 3.1 Test Locally

```bash
cd /path/to/CosmicDiary/CosmicDiary

# Create .env.local with email configuration
cat > .env.local << EOF
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
EOF

# Test email script
python3 send_collection_summary.py
```

### 3.2 Test via GitHub Actions

1. Go to **Actions** tab in GitHub
2. Select **"Event Collection with Cosmic State"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Check workflow logs for email notification step
5. Check your email inbox

---

## Step 4: Verify Configuration

### 4.1 Check Secrets are Set

In GitHub repository:
- **Settings** → **Secrets and variables** → **Actions** → **Secrets**
- Verify all 5 email secrets are present

### 4.2 Check Variable is Set

- **Settings** → **Secrets and variables** → **Actions** → **Variables**
- Verify `ENABLE_EMAIL_NOTIFICATIONS` is set to `true`

### 4.3 Check Workflow File

Ensure `.github/workflows/event-collection.yml` includes:
- ✅ "Send Success Email Notification" step
- ✅ "Send Failure Email Notification" step

---

## Email Format

### Success Email Includes:

- ✅ Status: SUCCESS
- 📊 Collection time
- 📈 Statistics:
  - Events detected
  - Events stored
  - Correlations created
  - Average correlation score (if available)
- 🎨 HTML formatted email

### Failure Email Includes:

- ❌ Status: FAILED
- 📊 Collection time
- ❌ Error details
- 🔗 Link to workflow logs (via GitHub issue creation)

---

## Troubleshooting

### Issue: Emails Not Sending

**Check:**
1. ✅ `ENABLE_EMAIL_NOTIFICATIONS` variable is set to `true`
2. ✅ All email secrets are configured
3. ✅ Gmail app password is correct (16 characters)
4. ✅ 2-Step Verification is enabled in Google Account
5. ✅ Check workflow logs for email errors

### Issue: Gmail Blocks Login

**Solution:**
- Use App Password (not regular password)
- Ensure "Less secure app access" is not needed (use App Password instead)
- Check if Google is blocking sign-in attempts (check Gmail security)

### Issue: SMTP Connection Failed

**Solution:**
- Verify SMTP server: `smtp.gmail.com`
- Try port `587` (TLS) or `465` (SSL)
- Check firewall/network restrictions

### Issue: Email Sent but Not Received

**Check:**
- Spam/junk folder
- Email address is correct
- Check workflow logs to confirm email was sent

---

## Alternative Email Providers

### Outlook/Hotmail

```
SMTP_SERVER: smtp-mail.outlook.com
SMTP_PORT: 587
```

### Yahoo

```
SMTP_SERVER: smtp.mail.yahoo.com
SMTP_PORT: 587
```

### Custom SMTP Server

Use your organization's SMTP server settings.

---

## Disable Email Notifications

To disable email notifications:

1. Go to **Settings** → **Secrets and variables** → **Actions** → **Variables**
2. Edit `ENABLE_EMAIL_NOTIFICATIONS`
3. Set value to: `false`
4. Save

Or remove the variable entirely (defaults to disabled).

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit email passwords to git**
   - Always use GitHub Secrets

2. **Use App Passwords, not regular passwords**
   - Gmail App Passwords are safer
   - Can be revoked individually

3. **Limit recipient email access**
   - Only add trusted email addresses
   - Use separate email for automation if possible

4. **Monitor email usage**
   - Check sent emails regularly
   - Revoke app passwords if compromised

---

## Next Steps

1. ✅ Set up email secrets in GitHub
2. ✅ Enable `ENABLE_EMAIL_NOTIFICATIONS` variable
3. ✅ Test email notification locally
4. ✅ Trigger GitHub Actions workflow manually
5. ✅ Verify email is received
6. ✅ Monitor automated emails every 2 hours

---

**Last Updated**: 2025-12-12

