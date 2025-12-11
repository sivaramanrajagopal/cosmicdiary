# 🚀 On-Demand Jobs Guide

**Run jobs manually and receive email notifications**

---

## 📋 Available On-Demand Jobs

### 1. Planetary Job with Email Notification

Runs the daily planetary calculation job and sends email notification on completion.

---

## 🎯 Usage

### Basic Usage (Today's Date)

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
python3 run_planetary_job_with_notification.py
```

### With Specific Date

```bash
python3 run_planetary_job_with_notification.py 2025-12-15
```

---

## ✨ Features

- ✅ Runs planetary calculation job
- ✅ Captures all output and errors
- ✅ Sends HTML email notification
- ✅ Shows success/failure status
- ✅ Includes detailed execution log in email
- ✅ Works with any date (past, present, or future)

---

## 📧 Email Configuration

### Required Environment Variables

Add these to your `.env.local`:

```bash
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
RECIPIENT_EMAIL=recipient@example.com
```

### Gmail Setup

1. **Enable 2-Step Verification**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll down to "App passwords"
   - Generate a new app password for "Mail"
   - Use this password (not your regular Gmail password)

3. **Configure `.env.local`**
   ```bash
   EMAIL_USER=vrsivauk78@gmail.com
   EMAIL_PASSWORD=your-16-character-app-password
   RECIPIENT_EMAIL=vrsivauk78@gmail.com
   ```

---

## 📨 Email Notification Format

The email includes:

- **Status**: Success or Failed indicator
- **Target Date**: Date for which planetary data was calculated
- **Execution Time**: When the job ran
- **Details**: Complete output log from the job

### Email Example

```
Subject: 🌙 Cosmic Diary - Planetary Job Success

Body:
- ✅ SUCCESS status
- Target Date: 2025-12-11
- Execution Time: 2025-12-11 06:05:30 IST
- Complete job output log
```

---

## 🔧 Advanced Usage

### Run for Multiple Dates

Create a simple script:

```bash
#!/bin/bash
# run_multiple_dates.sh

for date in 2025-12-10 2025-12-11 2025-12-12; do
    echo "Processing $date..."
    python3 run_planetary_job_with_notification.py $date
    sleep 5  # Wait between runs
done
```

### Schedule as Cron Job

Add to crontab for daily automated runs:

```bash
# Run at 6:30 AM IST daily with email notification
30 6 * * * cd /path/to/CosmicDiary && python3 run_planetary_job_with_notification.py >> logs/on_demand.log 2>&1
```

---

## 📊 Output

### Console Output

```
🌙 Starting On-Demand Planetary Job with Email Notification
============================================================
📅 Target date: 2025-12-11
📧 Notification will be sent to: your-email@gmail.com

📊 Job Output:
------------------------------------------------------------
🌙 Starting Daily Planetary Job - 2025-12-11T06:05:30
📅 Calculating planetary data for: 2025-12-11
✅ Updated planetary data for 2025-12-11
✅ Successfully processed planetary data for 2025-12-11
------------------------------------------------------------

📧 Sending email notification...
✅ Email notification sent to your-email@gmail.com

✅ Job completed successfully!
✅ Email notification sent

============================================================
```

---

## 🐛 Troubleshooting

### Email Not Sending

1. **Check environment variables**
   ```bash
   # Verify they're loaded
   python3 -c "from dotenv import load_dotenv; import os; load_dotenv('.env.local'); print(os.getenv('EMAIL_USER'))"
   ```

2. **Test email connection**
   ```python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   server.quit()
   print("✅ Email connection successful")
   ```

3. **Check Gmail security settings**
   - Ensure "Less secure app access" is enabled (or use App Password)
   - Check for any security alerts in Gmail

### Job Fails

1. **Check Flask API is running**
   - Job needs Flask API at `http://localhost:8000`
   - Verify with: `curl http://localhost:8000/health`

2. **Check database connection**
   - Verify Supabase credentials in `.env.local`
   - Test with: `python3 test_supabase_connection.py`

3. **Check logs**
   - Review output in console
   - Check email notification for detailed error

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| Run for today | `python3 run_planetary_job_with_notification.py` |
| Run for specific date | `python3 run_planetary_job_with_notification.py 2025-12-15` |
| Check email config | `grep EMAIL .env.local` |
| Test email manually | See troubleshooting section |

---

## 📝 Notes

- Email notification is optional - job will run even if email fails
- Email includes full job output for debugging
- Supports any date (past/present/future)
- Works with existing cron jobs (won't conflict)

---

## 🔄 Integration with Existing Cron Jobs

This script is independent of your cron jobs:
- Cron jobs run automatically on schedule
- This script runs on-demand when you execute it
- Both can run simultaneously without conflicts
- Use this for:
  - Testing new dates
  - Backfilling missing data
  - Manual triggers when needed
  - Development and debugging

---

**Ready to use! Just run the script and check your email.** 📧✨

