#!/usr/bin/env python3
"""
Script to delete old planetary data from database
This forces the system to recalculate using the fixed Flask API
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
SCRIPT_DIR = Path(__file__).parent.resolve()
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_planetary_data_for_date(date_str: str):
    """Delete planetary data for a specific date"""
    try:
        result = supabase.table('planetary_data').delete().eq('date', date_str).execute()
        print(f"✅ Deleted planetary data for {date_str}")
        return True
    except Exception as e:
        print(f"❌ Error deleting data for {date_str}: {e}")
        return False

def delete_all_recent_planetary_data():
    """Delete all planetary data from 2025-12-01 onwards"""
    from datetime import date, timedelta
    
    start_date = date(2025, 12, 1)
    today = date.today()
    
    current = start_date
    deleted_count = 0
    
    print(f"🗑️  Deleting planetary data from {start_date} to {today}...")
    print("   (This will force recalculation with fixed Ketu calculation)")
    print("")
    
    while current <= today:
        date_str = current.isoformat()
        if delete_planetary_data_for_date(date_str):
            deleted_count += 1
        current += timedelta(days=1)
    
    print(f"\n✅ Deleted {deleted_count} days of planetary data")
    print("   Next time you load /planets, it will fetch fresh data from Flask API")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Delete specific date
        date_str = sys.argv[1]
        delete_planetary_data_for_date(date_str)
    else:
        # Delete all recent data
        delete_all_recent_planetary_data()

