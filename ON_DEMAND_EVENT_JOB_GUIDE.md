# 📅 On-Demand Event Collection & Analysis Job

**Collect events, create in database, trigger analysis, and send email notification**

---

## 🎯 What This Job Does

1. ✅ **Fetches Events** - Uses OpenAI to collect significant world events for a date
2. ✅ **Creates Events** - Stores events in the `events` table
3. ✅ **Triggers Analysis** - Automatically calculates:
   - House mappings (event → astrological house)
   - Planetary aspects (which planets aspect the event's house)
   - Planetary correlations (significant planet influences)
4. ✅ **Sends Email** - Notification with results and details

---

## 🚀 Quick Usage

### Run for Yesterday (Default - Most Recent Events)

```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
./run_event_job.sh
```

### Run for Specific Date

```bash
./run_event_job.sh 2025-12-10
```

Or use Python directly:

```bash
python3 run_event_collection_with_notification.py
python3 run_event_collection_with_notification.py 2025-12-15
```

---

## ✨ Features

- 🤖 **OpenAI Integration** - Fetches real, significant world events
- 💾 **Database Storage** - Creates events in Supabase
- 🔮 **Automatic Analysis** - Triggers house mapping, aspects, correlations
- 📧 **Email Notification** - Beautiful HTML email with results
- 📊 **Detailed Logging** - Complete execution details in email
- 🎯 **Error Handling** - Graceful failure handling with detailed reports

---

## 📋 Requirements

### Environment Variables

Ensure these are set in `.env.local`:

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-api-key

# Email (optional but recommended)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com

# Optional (defaults provided)
NEXTJS_API_URL=http://localhost:3002
FLASK_API_URL=http://localhost:8000
```

---

## 📊 What Gets Created

### Events Table
Each event includes:
- **Title** - Event name
- **Description** - Detailed description
- **Category** - Event category (Natural Disaster, Political, etc.)
- **Location** - City, Country
- **Impact Level** - low, medium, high, critical
- **Date** - Event date
- **Tags** - Relevant keywords

### Automatic Analysis (Triggered on Creation)

When an event is created via the Next.js API, it automatically triggers:

1. **House Mapping** (`event_house_mappings`)
   - Maps event to astrological house (1-12)
   - Based on event category and significations

2. **Planetary Aspects** (`event_planetary_aspects`)
   - Calculates which planets aspect the event's house
   - Includes aspect types and strengths

3. **Planetary Correlations** (`event_planetary_correlations`)
   - Identifies significant planets
   - Calculates correlation scores
   - Notes reasons for correlation

---

## 📧 Email Notification

The email includes:

### Header
- Status indicator (Success/Failed)
- Execution timestamp

### Summary
- Target date processed
- Number of events created
- Execution status

### Events List
- All created events with:
  - Title
  - Category
  - Impact level
  - Location

### Details
- Complete execution log
- Success/failure for each event
- Error messages if any

### Automatic Analysis Note
- Reminder that analysis will run automatically

---

## 🔄 Complete Flow

```
1. Fetch Events (OpenAI)
   └─ Collects 3-5 significant events for target date
   
2. Create Events (Supabase)
   └─ Stores each event in events table
   └─ Gets event ID back
   
3. Trigger Analysis (Automatic)
   └─ When event accessed via API, triggers:
      ├─ House mapping calculation
      ├─ Planetary aspects calculation
      └─ Planetary correlations calculation
   
4. Send Email
   └─ HTML notification with results
```

---

## 🎯 Example Output

### Console Output

```
📅 Starting On-Demand Event Collection & Analysis with Email Notification
======================================================================
📅 Target date: 2025-12-10
📧 Notification will be sent to: your-email@gmail.com

🤖 Fetching events from OpenAI...
✅ Fetched 4 events from OpenAI

💾 Creating events in database...
  [1/4] Creating: Major Earthquake Strikes California
  [2/4] Creating: Economic Policy Reform Announced
  [3/4] Creating: New Technology Breakthrough
  [4/4] Creating: International Summit Concludes

✅ Created 4/4 events in database

🔮 Analysis will be automatically triggered when events are accessed via API
   (House mapping, aspects, and correlations will be calculated)

📧 Sending email notification...
✅ Email notification sent to your-email@gmail.com

✅ Job completed successfully! Created 4 events.
✅ Email notification sent

======================================================================
```

### Email Content

- **Subject**: 📅 Cosmic Diary - Event Collection Success
- **Body**: HTML email with:
  - Status badge
  - Event count summary
  - List of all created events
  - Complete execution log
  - Automatic analysis reminder

---

## 🐛 Troubleshooting

### No Events Fetched

**Possible Causes:**
- OpenAI API key not set
- API rate limit exceeded
- No significant events for date (future dates)

**Solution:**
- Check `OPENAI_API_KEY` in `.env.local`
- Try a different date (past dates more likely to have events)

### Events Not Created

**Possible Causes:**
- Database connection issue
- Missing required fields
- Duplicate event (same title/date)

**Solution:**
- Check Supabase credentials
- Review error messages in email/console
- Verify database is accessible

### Analysis Not Triggered

**Note:** Analysis is automatically triggered when events are accessed via the Next.js API. To manually trigger:

1. Visit event in UI: `http://localhost:3002/events/[id]`
2. Or call API: `GET http://localhost:3002/api/events/[id]`
3. Or trigger recalculation: `POST http://localhost:3002/api/events/recalculate-correlations`

---

## 📝 Notes

### Date Selection

- **Default**: Yesterday (more likely to have real events)
- **Past Dates**: Recommended (historical events)
- **Future Dates**: Will generate speculative events
- **Today**: May have limited events

### Event Analysis Timing

Analysis (house mapping, aspects, correlations) happens:
- Automatically when event is accessed via Next.js API
- Can be manually triggered via `/api/events/recalculate-correlations`
- Requires planetary data to exist for event date

### Cost Considerations

- **OpenAI API**: ~$0.001-0.01 per run (depends on model and tokens)
- **Supabase**: Free tier includes plenty of storage
- **Email**: Free with Gmail (or your SMTP provider)

---

## 🔄 Integration with Other Jobs

### Standalone Use

```bash
# Run event collection
./run_event_job.sh 2025-12-10

# Run planetary data collection
./run_job.sh 2025-12-10
```

### Combined Workflow

1. **First**: Run planetary data job (ensures planetary positions exist)
2. **Then**: Run event collection job (creates events)
3. **Analysis**: Happens automatically when events are created

---

## ✅ Success Indicators

- Console shows "✅ Created X/Y events"
- Email received with event list
- Events visible in database
- Events appear in UI (`/events` page)
- Analysis data available after accessing events

---

**Ready to collect events! Run `./run_event_job.sh` to get started.** 🚀✨

