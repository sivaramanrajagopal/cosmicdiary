#!/bin/bash
# Wrapper script to run Python scripts with environment variables loaded
# This ensures Python scripts can access .env.local even when run from cron
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Export environment variables from .env.local for bash environment
# This is a fallback - Python dotenv should handle it, but this ensures compatibility
if [ -f "$SCRIPT_DIR/.env.local" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env.local" | grep -v '^$' | xargs)
fi

# Execute the command with full path resolution
exec "$@"
