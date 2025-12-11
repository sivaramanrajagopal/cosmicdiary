#!/bin/bash
# Quick wrapper script to run on-demand planetary job with email notification

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Use wrapper to ensure environment variables are loaded
if [ -n "$1" ]; then
    # Run with specific date
    "$SCRIPT_DIR/run_with_env.sh" /usr/bin/python3 "$SCRIPT_DIR/run_planetary_job_with_notification.py" "$1"
else
    # Run for today
    "$SCRIPT_DIR/run_with_env.sh" /usr/bin/python3 "$SCRIPT_DIR/run_planetary_job_with_notification.py"
fi

