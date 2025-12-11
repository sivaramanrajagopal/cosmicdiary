#!/bin/bash

# Fix Cosmic Diary Cron Jobs
# This script fixes environment variable loading and cleans up duplicate/broken jobs

echo "🔧 Fixing Cosmic Diary Cron Jobs"
echo "=================================="

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

echo "📁 Script directory: $SCRIPT_DIR"
echo "🐍 Python path: $PYTHON_PATH"
echo ""

# Check if .env.local exists
if [ ! -f "$SCRIPT_DIR/.env.local" ]; then
    echo "❌ Error: .env.local not found at $SCRIPT_DIR/.env.local"
    echo "   Please create this file with your environment variables"
    exit 1
fi

echo "✅ Found .env.local at $SCRIPT_DIR/.env.local"
echo ""

# Create temporary cron file
CRON_FILE=$(mktemp)

# Get current crontab
crontab -l 2>/dev/null > "$CRON_FILE" || true

# Remove ALL existing Cosmic Diary jobs
echo "🧹 Cleaning up existing cron jobs..."
sed -i.bak '/# Cosmic Diary/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/# Cosmic Diary/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/daily_planetary_job.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/daily_planetary_job.py/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/import_automated_events.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/import_automated_events.py/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/email_reports.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/email_reports.py/d' "$CRON_FILE" 2>/dev/null
sed -i.bak '/automated_event_recorder.py/d' "$CRON_FILE" 2>/dev/null || sed -i '' '/automated_event_recorder.py/d' "$CRON_FILE" 2>/dev/null

# Create a wrapper script that loads environment variables
WRAPPER_SCRIPT="$SCRIPT_DIR/run_with_env.sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Wrapper script to run Python scripts with environment variables loaded
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/.env.local" 2>/dev/null || true
exec "$@"
EOF

chmod +x "$WRAPPER_SCRIPT"
echo "✅ Created wrapper script: $WRAPPER_SCRIPT"

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Add cleaned up Cosmic Diary cron jobs with proper environment loading
cat >> "$CRON_FILE" << EOF

# Cosmic Diary - Automated Jobs (Fixed - $(date +%Y-%m-%d))
# Daily planetary calculations (Midnight IST / 6:30 PM previous day UTC)
# Uses wrapper script to load .env.local
0 0 * * * "$WRAPPER_SCRIPT" "$PYTHON_PATH" "$SCRIPT_DIR/daily_planetary_job.py" >> "$SCRIPT_DIR/logs/planetary.log" 2>&1

# Automated event collection (11:30 AM IST / 6:00 AM UTC)
0 6 * * * "$WRAPPER_SCRIPT" "$PYTHON_PATH" "$SCRIPT_DIR/import_automated_events.py" >> "$SCRIPT_DIR/logs/event_collection.log" 2>&1

# Automated event collection (11:30 PM IST / 6:00 PM UTC)
30 18 * * * "$WRAPPER_SCRIPT" "$PYTHON_PATH" "$SCRIPT_DIR/import_automated_events.py" >> "$SCRIPT_DIR/logs/event_collection.log" 2>&1

# Daily email summary (11:00 PM IST / 5:30 PM UTC)
30 17 * * * "$WRAPPER_SCRIPT" "$PYTHON_PATH" "$SCRIPT_DIR/email_reports.py" daily >> "$SCRIPT_DIR/logs/email_reports.log" 2>&1

# Weekly email analysis (Sunday 6:00 PM IST / Sunday 12:30 PM UTC)
30 12 * * 0 "$WRAPPER_SCRIPT" "$PYTHON_PATH" "$SCRIPT_DIR/email_reports.py" weekly >> "$SCRIPT_DIR/logs/email_reports.log" 2>&1
EOF

# Install the new crontab
crontab "$CRON_FILE"

# Clean up
rm -f "$CRON_FILE" "${CRON_FILE}.bak"

echo ""
echo "✅ Cron jobs fixed and installed successfully!"
echo ""
echo "📋 Installed jobs:"
echo "   - Daily planetary calculations (Midnight IST / 00:00)"
echo "   - Event collection (6:00 AM UTC / 11:30 AM IST)"
echo "   - Event collection (6:30 PM UTC / 11:30 PM IST)"
echo "   - Daily email summary (5:30 PM UTC / 11:00 PM IST)"
echo "   - Weekly email analysis (Sunday 12:30 PM UTC / 6:00 PM IST)"
echo ""
echo "📝 Logs location: $SCRIPT_DIR/logs/"
echo ""
echo "🔍 To verify cron jobs:"
echo "   crontab -l | grep -A 1 'Cosmic Diary'"
echo ""
echo "🧪 To test manually:"
echo "   $WRAPPER_SCRIPT $PYTHON_PATH $SCRIPT_DIR/daily_planetary_job.py"

