"""
Daily Planetary Data Job
Calculates and stores planetary positions for today (or specified date)
Runs via cron: 0 6 * * * (6 AM daily)
"""

import os
import sys
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
import requests
from supabase import create_client, Client

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()

# Load .env files from script directory (works even when run from cron)
# Try .env.local first (takes precedence), then .env
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)  # Don't override if .env.local already loaded

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
# Support both SUPABASE_SERVICE_ROLE_KEY and SUPABASE_KEY for compatibility
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY', '')

# Flask API URL (if running separately)
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:8000')

def calculate_planetary_data_via_api(target_date: date) -> dict:
    """Fetch planetary data from Flask API"""
    try:
        url = f"{FLASK_API_URL}/api/planets/daily"
        params = {'date': target_date.isoformat()}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching from Flask API: {e}")
        return None


def store_planetary_data(supabase: Client, planetary_data: dict):
    """Store planetary data in Supabase"""
    try:
        # Check if data already exists for this date
        date_str = planetary_data['date']
        
        # Try to get existing record
        existing = supabase.table('planetary_data')\
            .select('id')\
            .eq('date', date_str)\
            .execute()
        
        data_to_store = {
            'date': date_str,
            'planetary_data': planetary_data['planetary_data']
        }
        
        if existing.data:
            # Update existing record
            result = supabase.table('planetary_data')\
                .update(data_to_store)\
                .eq('date', date_str)\
                .execute()
            print(f"✅ Updated planetary data for {date_str}")
        else:
            # Insert new record
            result = supabase.table('planetary_data')\
                .insert(data_to_store)\
                .execute()
            print(f"✅ Inserted planetary data for {date_str}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error storing planetary data: {e}")
        return False


def main():
    """Main function"""
    print(f"🌙 Starting Daily Planetary Job - {datetime.now().isoformat()}")
    
    # Initialize Supabase
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Determine target date (default to today)
    # Can be overridden with command line argument: python daily_planetary_job.py 2025-01-15
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"❌ Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = date.today()
    
    print(f"📅 Calculating planetary data for: {target_date.isoformat()}")
    
    # Fetch planetary data from Flask API
    planetary_data = calculate_planetary_data_via_api(target_date)
    
    if not planetary_data:
        print("❌ Failed to calculate planetary data")
        sys.exit(1)
    
    # Store in Supabase
    success = store_planetary_data(supabase, planetary_data)
    
    if success:
        print(f"✅ Successfully processed planetary data for {target_date.isoformat()}")
        sys.exit(0)
    else:
        print("❌ Failed to store planetary data")
        sys.exit(1)


if __name__ == '__main__':
    main()
