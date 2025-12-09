#!/bin/bash

# Cosmic Diary Cron Job Setup Script
# This script sets up cron jobs for automated tasks

echo "🕐 Setting up Cosmic Diary Cron Jobs"
echo "======================================"

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

echo "📁 Script directory: $SCRIPT_DIR"
echo "🐍 Python path: $PYTHON_PATH"

# Create temporary cron file
CRON_FILE=$(mktemp)

# Get current crontab
crontab -l 2>/dev/null > "$CRON_FILE" || true

# Remove existing Cosmic Diary jobs if any
sed -i.bak '/# Cosmic Diary/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/# Cosmic Diary/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/daily_planetary_job.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/daily_planetary_job.py/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/import_automated_events.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/import_automated_events.py/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/email_reports.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/email_reports.py/d' "$CRON_FILE" 2>/dev/null

# Add Cosmic Diary cron jobs
cat >> "$CRON_FILE" << EOF

# Cosmic Diary - Automated Jobs
# Daily planetary calculations (6 AM IST / 12:30 AM UTC)
30 0 * * * cd "$SCRIPT_DIR" && "$PYTHON_PATH" "$SCRIPT_DIR/daily_planetary_job.py" >> "$SCRIPT_DIR/logs/planetary_job.log" 2>&1

# Automated event collection (11:30 AM IST / 6:00 AM UTC)
0 6 * * * cd "$SCRIPT_DIR" && "$PYTHON_PATH" "$SCRIPT_DIR/import_automated_events.py" >> "$SCRIPT_DIR/logs/event_collection.log" 2>&1

# Automated event collection (11:30 PM IST / 6:00 PM UTC)
30 18 * * * cd "$SCRIPT_DIR" && "$PYTHON_PATH" "$SCRIPT_DIR/import_automated_events.py" >> "$SCRIPT_DIR/logs/event_collection.log" 2>&1

# Daily email summary (11:00 PM IST / 5:30 PM UTC)
30 17 * * * cd "$SCRIPT_DIR" && "$PYTHON_PATH" "$SCRIPT_DIR/email_reports.py" daily >> "$SCRIPT_DIR/logs/email_reports.log" 2>&1

# Weekly email analysis (Sunday 6:00 PM IST / Sunday 12:30 PM UTC)
30 12 * * 0 cd "$SCRIPT_DIR" && "$PYTHON_PATH" "$SCRIPT_DIR/email_reports.py" weekly >> "$SCRIPT_DIR/logs/email_reports.log" 2>&1
EOF

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Install the new crontab
crontab "$CRON_FILE"

# Clean up
rm -f "$CRON_FILE" "${CRON_FILE}.bak"

echo "✅ Cron jobs installed successfully!"
echo ""
echo "📋 Installed jobs:"
echo "   - Daily planetary calculations (6:00 AM IST)"
echo "   - Event collection (11:30 AM IST)"
echo "   - Event collection (11:30 PM IST)"
echo "   - Daily email summary (11:00 PM IST)"
echo "   - Weekly email analysis (Sunday 6:00 PM IST)"
echo ""
echo "📝 Logs will be written to: $SCRIPT_DIR/logs/"
echo ""
echo "To view cron jobs: crontab -l"
echo "To remove cron jobs: crontab -e (then delete the Cosmic Diary entries)"
