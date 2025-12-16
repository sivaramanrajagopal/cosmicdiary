# Enhanced Email Notifications System

## Overview

The Cosmic Diary application now includes an enhanced email notification system that sends beautiful, informative email summaries with mini dashboards of recent events.

## Features

### 1. **2-Hour Event Collection Summary**
- Triggered automatically every 2 hours via GitHub Actions
- Shows events collected in the last 2 hours
- Displays mini dashboard with statistics and event cards

### 2. **Daily Summary Email**
- Sent once per day at 11:30 PM UTC (configurable)
- Comprehensive summary of all events from the last 24 hours
- Perfect for end-of-day review

### 3. **Mini Dashboard in Email**

Each email includes:

#### Statistics Grid
- **Events Detected**: Number of events found by collection system
- **Events Stored**: Number successfully saved to database
- **Correlations**: Planetary correlations created
- **Avg Score**: Average correlation strength

#### Event Cards
Up to 10 most recent events with:
- Color-coded impact levels (Critical, High, Medium, Low)
- Category emojis (🌪️ Natural Disaster, ⚔️ War, 💰 Economic, etc.)
- Event details: Date, Location, Category
- Description preview (first 150 characters)
- Border colors matching impact level

#### Visual Design
- Purple gradient header with Cosmic Diary branding
- Dark theme consistent with web app
- Responsive HTML email layout
- Plain text fallback for compatibility
- Links to dashboard and events page

## Email Types

### Success Email
Sent when event collection completes successfully:
- ✅ SUCCESS status badge (green)
- Full statistics
- Event cards for all collected events
- Links to view more on web app

### Failure Email
Sent when collection encounters errors:
- ❌ FAILED status badge (red)
- Error details displayed prominently
- Partial statistics (if any events were collected before failure)
- Helpful for debugging issues

### Daily Summary
Comprehensive end-of-day report:
- 🌟 Daily Summary subject line
- Stats for entire 24-hour period
- All events from the day organized by impact
- Perfect for reflection and pattern recognition

## Configuration

### Required Environment Variables

#### For GitHub Actions:
Set these as repository secrets in GitHub:

```yaml
# Email Server Configuration
SMTP_SERVER: smtp.gmail.com          # Your SMTP server
SMTP_PORT: 587                       # SMTP port (usually 587 for TLS)
EMAIL_USER: your-email@gmail.com     # Sender email address
EMAIL_PASSWORD: your-app-password    # Email password or app-specific password
RECIPIENT_EMAIL: recipient@email.com # Email address to receive notifications

# Supabase Configuration (for fetching event data)
SUPABASE_URL: https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY: your-service-role-key
```

#### Enable Notifications:
Set this as a repository variable (not secret):

```yaml
ENABLE_EMAIL_NOTIFICATIONS: 'true'
```

### Gmail Setup

If using Gmail:

1. **Enable 2-Factor Authentication** on your Google account
2. **Create App Password**:
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this as `EMAIL_PASSWORD` secret

3. **Configure Secrets**:
   ```
   EMAIL_USER: your-gmail@gmail.com
   EMAIL_PASSWORD: xxxx xxxx xxxx xxxx  (16-char app password)
   SMTP_SERVER: smtp.gmail.com
   SMTP_PORT: 587
   ```

## File Structure

### Python Scripts

#### `send_enhanced_summary.py`
Main email notification script with:
- HTML email template with mini dashboard
- Event fetching from Supabase
- Color-coded impact levels and categories
- Support for both 2-hour and daily summaries
- Error handling and fallbacks

#### `send_collection_summary.py` (Legacy)
Old simple text-based email system (no longer used)

### GitHub Actions Workflows

#### `.github/workflows/event-collection.yml`
Every 2 hours event collection:
- Runs `collect_events_with_cosmic_state.py`
- Extracts statistics from script output
- Calls `send_enhanced_summary.py` with `COLLECTION_TYPE=2-hour`
- Sends success or failure notifications

#### `.github/workflows/daily-summary.yml`
Daily summary workflow:
- Runs once per day at 11:30 PM UTC
- Queries Supabase for last 24 hours of events
- Calls `send_enhanced_summary.py` with `COLLECTION_TYPE=daily`
- Independent from event collection (runs even if no collection happened)

## Email Content Structure

### HTML Email

```html
<!DOCTYPE html>
<html>
  <head>
    <!-- Responsive styles, dark theme -->
  </head>
  <body>
    <!-- Purple gradient header with status -->
    <div class="header">
      <h1>🌟 Cosmic Diary</h1>
      <div class="status">✅ SUCCESS</div>
    </div>

    <!-- Statistics grid (4 boxes) -->
    <div class="stats">
      <div class="stat-grid">
        <div class="stat-box">Events Detected: 5</div>
        <div class="stat-box">Events Stored: 5</div>
        <div class="stat-box">Correlations: 12</div>
        <div class="stat-box">Avg Score: 72</div>
      </div>
    </div>

    <!-- Event cards section -->
    <div class="events-section">
      <h3>📋 Recently Collected Events (5)</h3>
      <!-- Color-coded event cards -->
      <div class="event-card">
        <h4>🌪️ Hurricane Milton hits Florida</h4>
        <span class="impact-badge">HIGH</span>
        <div>📅 2024-10-09 • 📍 Florida, USA • 🏷️ Natural Disaster</div>
        <p>Major hurricane causing widespread damage...</p>
      </div>
    </div>

    <!-- Footer with links -->
    <div class="footer">
      <a href="https://cosmicdiary.vercel.app/dashboard">📊 View Dashboard</a>
      <a href="https://cosmicdiary.vercel.app/events">📅 View All Events</a>
    </div>
  </body>
</html>
```

### Plain Text Fallback

```
Cosmic Diary - Event Collection Summary
==================================================

Status: ✅ SUCCESS
Collection Time: 2024-12-16 14:30:00 UTC

Statistics:
- Events Detected: 5
- Events Stored: 5
- Correlations Created: 12
- Avg Correlation Score: 72.00

Recent Events (5):

1. Hurricane Milton hits Florida
   Date: 2024-10-09
   Category: Natural Disaster | Impact: HIGH
   Location: Florida, USA
   Major hurricane causing widespread damage...

View Dashboard: https://cosmicdiary.vercel.app/dashboard
View Events: https://cosmicdiary.vercel.app/events
```

## Email Examples

### Subject Lines

**2-Hour Collection:**
```
🌟 Cosmic Diary: Event Collection Summary - 2024-12-16 14:30:00 UTC
```

**Daily Summary:**
```
🌟 Cosmic Diary: Daily Summary - December 16, 2024
```

**Failure:**
```
🌟 Cosmic Diary: Event Collection Failed - 2024-12-16 14:30:00 UTC
```

## Category Emojis

The system uses these emojis for visual categorization:

- 🌪️ Natural Disaster (Red border)
- ⚔️ War (Dark red border)
- 💰 Economic (Orange border)
- 🏛️ Political (Blue border)
- 💻 Technology (Purple border)
- 🏥 Health (Green border)
- 👤 Personal (Pink border)
- 📌 Other (Gray border)

## Impact Level Colors

- **Critical**: Red (#dc2626)
- **High**: Orange (#f97316)
- **Medium**: Yellow (#fbbf24)
- **Low**: Green (#10b981)

## Testing

### Manual Test

To test the email system locally:

```bash
# Set environment variables in .env.local
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@email.com
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-key

# Set test statistics
export EVENTS_DETECTED=5
export EVENTS_STORED=5
export CORRELATIONS_CREATED=12
export AVG_CORRELATION_SCORE=72.5
export COLLECTION_TYPE=2-hour

# Run the script
python send_enhanced_summary.py
```

### Test via GitHub Actions

Trigger manually from GitHub:
1. Go to Actions tab
2. Select "Event Collection with Cosmic State - Every 2 Hours"
3. Click "Run workflow" → "Run workflow"
4. Check email inbox

Or for daily summary:
1. Go to Actions tab
2. Select "Daily Event Summary Email"
3. Click "Run workflow" → "Run workflow"
4. Check email inbox

## Troubleshooting

### Email Not Received

1. **Check GitHub Actions logs**:
   - Look for "✅ Enhanced summary email sent to..." in workflow logs
   - Check for error messages

2. **Verify environment variables**:
   - Ensure all required secrets are set
   - Verify `ENABLE_EMAIL_NOTIFICATIONS=true` is set as repository variable

3. **Check spam folder**:
   - First emails from new sender might be flagged as spam
   - Mark as "Not Spam" to whitelist

4. **SMTP Authentication**:
   - For Gmail, ensure you're using App Password (not regular password)
   - Verify 2FA is enabled on Google account

### Missing Event Cards

If statistics show events but cards are empty:

1. **Check Supabase connection**:
   - Verify `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are correct
   - Check Supabase logs for query errors

2. **Check time window**:
   - 2-hour summaries look back 2 hours from send time
   - Daily summaries look back 24 hours
   - Events must have `created_at` timestamp within window

### HTML Not Rendering

If email shows plain text instead of HTML:

1. **Email client compatibility**:
   - Most modern email clients support HTML
   - Some corporate email systems strip HTML

2. **Check email source**:
   - Email should have both `text/plain` and `text/html` parts
   - Client should automatically choose best format

## Workflow Schedule

### 2-Hour Collection
```yaml
cron: '30 */2 * * *'
```
Runs at: 00:30, 02:30, 04:30, 06:30, 08:30, 10:30, 12:30, 14:30, 16:30, 18:30, 20:30, 22:30 UTC

### Daily Summary
```yaml
cron: '30 23 * * *'
```
Runs at: 23:30 UTC (11:30 PM UTC) every day

**To adjust daily summary time**, edit `.github/workflows/daily-summary.yml`:
```yaml
# For 8 AM UTC:
cron: '0 8 * * *'

# For 6 PM UTC:
cron: '0 18 * * *'
```

## Benefits

1. **Stay Informed**: Get automatic updates about cosmic events
2. **Visual Dashboard**: See trends and patterns at a glance
3. **Error Monitoring**: Know immediately if collection fails
4. **Mobile Friendly**: Email renders beautifully on all devices
5. **Actionable Links**: Quick access to web dashboard from email
6. **Professional Design**: Clean, branded email matching app theme

## Next Steps

After configuring email notifications:

1. **Enable in GitHub**:
   - Set `ENABLE_EMAIL_NOTIFICATIONS=true` as repository variable
   - Add all required secrets

2. **Test manually**:
   - Trigger workflow manually to test email delivery
   - Verify HTML renders correctly in your email client

3. **Monitor**:
   - Check GitHub Actions logs for email send confirmations
   - Review daily summaries to track event collection patterns

4. **Customize** (optional):
   - Adjust daily summary time in workflow file
   - Modify email template in `send_enhanced_summary.py`
   - Update dashboard URLs if using custom domain

## Advanced Customization

### Change Email Template

Edit `send_enhanced_summary.py`:

```python
# Change colors
status_color = "#10b981"  # Success color
impact_colors = {
    'critical': '#dc2626',  # Customize impact colors
    'high': '#f97316',
    # ...
}

# Change number of events shown
for event in recent_events[:10]:  # Change 10 to desired number
    # ...

# Change email subject format
msg['Subject'] = f'Custom: {title}'
```

### Add More Statistics

Extend the statistics grid:

```python
html_body += f"""
<div class="stat-box">
    <span class="stat-value">{custom_metric}</span>
    <span class="stat-label">Custom Metric</span>
</div>
"""
```

### Filter Events in Email

Show only high-impact events:

```python
# In fetch_recent_events(), add filter:
response = supabase.table('events')\
    .select('...')\
    .gte('created_at', cutoff_time)\
    .in_('impact_level', ['high', 'critical'])\  # Filter
    .execute()
```

## Summary

The enhanced email notification system provides:
- ✅ Automatic 2-hour summaries with mini dashboard
- ✅ Daily comprehensive reports
- ✅ Beautiful HTML emails with event cards
- ✅ Color-coded impact levels and categories
- ✅ Error notifications for failed collections
- ✅ Mobile-responsive design
- ✅ Easy configuration via GitHub secrets
- ✅ Plain text fallback for compatibility

Stay connected to cosmic events with professional, informative email updates! 🌟
