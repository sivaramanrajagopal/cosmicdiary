# 🚀 On-Demand Jobs - Complete Summary

**Two powerful on-demand jobs with email notifications**

---

## 📋 Available Jobs

### 1. Planetary Data Job ✅

**Script**: `run_planetary_job_with_notification.py` or `./run_job.sh`

**What it does:**
- Calculates planetary positions for a date
- Stores in `planetary_data` table
- Sends email notification

**Usage:**
```bash
./run_job.sh                    # Today
./run_job.sh 2025-12-15         # Specific date
```

---

### 2. Event Collection Job ✅ **NEW**

**Script**: `run_event_collection_with_notification.py` or `./run_event_job.sh`

**What it does:**
- Fetches events using OpenAI
- Creates events in `events` table
- Triggers automatic analysis (house mapping, aspects, correlations)
- Sends email notification

**Usage:**
```bash
./run_event_job.sh              # Yesterday (default)
./run_event_job.sh 2025-12-10   # Specific date
```

---

## 🎯 Quick Comparison

| Feature | Planetary Job | Event Collection Job |
|---------|---------------|----------------------|
| **Updates** | `planetary_data` table | `events` table |
| **Data Source** | Swiss Ephemeris (Flask API) | OpenAI API |
| **Requires** | Flask API running | OpenAI API key |
| **Triggers Analysis** | No | Yes (automatic) |
| **Default Date** | Today | Yesterday |
| **Email** | ✅ Yes | ✅ Yes |

---

## 🔄 Complete Workflow

### Recommended Order:

1. **First**: Run Planetary Job
   ```bash
   ./run_job.sh 2025-12-10
   ```
   - Ensures planetary data exists for the date

2. **Then**: Run Event Collection Job
   ```bash
   ./run_event_job.sh 2025-12-10
   ```
   - Creates events
   - Analysis requires planetary data (from step 1)

3. **Result**: Complete data with analysis
   - Events stored
   - Planetary data available
   - House mappings calculated
   - Aspects determined
   - Correlations analyzed

---

## 📧 Email Notifications

Both jobs send beautiful HTML emails with:

- ✅ Status indicator (Success/Failed)
- 📅 Target date processed
- 📊 Summary statistics
- 📝 Complete execution logs
- 🔍 Detailed results

**Email Configuration:**
- Uses same email settings from `.env.local`
- Sent to `RECIPIENT_EMAIL` (defaults to `EMAIL_USER`)

---

## 🔧 Requirements

### For Planetary Job:
- ✅ Flask API running (`http://localhost:8000`)
- ✅ Supabase credentials
- ✅ Email credentials (optional)

### For Event Collection Job:
- ✅ OpenAI API key
- ✅ Supabase credentials
- ✅ Email credentials (optional)
- ✅ Next.js API running (for analysis trigger, optional)

---

## 📁 Files Created

```
CosmicDiary/
├── run_planetary_job_with_notification.py    # Planetary job script
├── run_job.sh                                 # Planetary job wrapper
├── run_event_collection_with_notification.py  # Event collection script
├── run_event_job.sh                           # Event collection wrapper
├── ON_DEMAND_JOBS_GUIDE.md                    # Planetary job guide
├── ON_DEMAND_EVENT_JOB_GUIDE.md               # Event job guide
└── ON_DEMAND_JOBS_SUMMARY.md                  # This file
```

---

## 🎓 Usage Examples

### Example 1: Calculate Planetary Data for Today
```bash
cd /Users/sivaramanrajagopal/CosmicDiary/CosmicDiary
./run_job.sh
```

### Example 2: Collect Events for Yesterday
```bash
./run_event_job.sh
```

### Example 3: Complete Setup for a Date
```bash
# Step 1: Get planetary data
./run_job.sh 2025-12-10

# Step 2: Collect events
./run_event_job.sh 2025-12-10

# Step 3: Check results
python3 check_db_status.py
```

### Example 4: Batch Processing Multiple Dates
```bash
#!/bin/bash
# Process last 7 days
for i in {0..6}; do
    date=$(date -v-${i}d +%Y-%m-%d)
    echo "Processing $date..."
    ./run_job.sh $date
    ./run_event_job.sh $date
    sleep 5  # Rate limiting
done
```

---

## ✅ Verification

### Check What Was Created:

```bash
# Check database status
python3 check_db_status.py

# Or query directly
# - Check planetary_data table
# - Check events table
# - Check event_house_mappings table
# - Check event_planetary_aspects table
```

---

## 🐛 Troubleshooting

### Planetary Job Issues

**Problem**: "Failed to calculate planetary data"
- ✅ Ensure Flask API is running
- ✅ Check `FLASK_API_URL` in `.env.local`

**Problem**: Email not sent
- ✅ Check email credentials in `.env.local`
- ✅ Verify Gmail app password (not regular password)

### Event Collection Job Issues

**Problem**: "No events fetched"
- ✅ Check `OPENAI_API_KEY` is set
- ✅ Verify API key is valid
- ✅ Check OpenAI account has credits

**Problem**: "Events created but no analysis"
- ✅ Analysis happens automatically when events accessed via API
- ✅ Visit event in UI: `http://localhost:3002/events/[id]`
- ✅ Or trigger manually: `POST /api/events/recalculate-correlations`

---

## 📚 Documentation

- **Planetary Job**: See `ON_DEMAND_JOBS_GUIDE.md`
- **Event Collection Job**: See `ON_DEMAND_EVENT_JOB_GUIDE.md`
- **Database Status**: Run `check_db_status.py`

---

## 🎯 Next Steps

1. ✅ **Test Planetary Job**
   ```bash
   ./run_job.sh
   ```

2. ✅ **Test Event Collection Job**
   ```bash
   ./run_event_job.sh
   ```

3. ✅ **Check Email Inbox**
   - You should receive notifications for both jobs

4. ✅ **Verify in Database**
   ```bash
   python3 check_db_status.py
   ```

5. ✅ **View in UI**
   - Visit `http://localhost:3002/events` to see created events
   - Visit `http://localhost:3002/planets` to see planetary data

---

## 💡 Tips

- **Run planetary job first** - Events need planetary data for analysis
- **Use past dates** - More likely to have real events
- **Check email** - Detailed logs are included
- **Monitor logs** - Check console output for real-time status
- **Batch processing** - Use scripts for multiple dates

---

**Both jobs are ready to use! Start with `./run_job.sh` or `./run_event_job.sh`** 🚀✨

