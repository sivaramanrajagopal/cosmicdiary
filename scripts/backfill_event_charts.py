#!/usr/bin/env python3
"""
Backfill chart data for existing events that have location and time.

This script:
1. Finds events that have latitude/longitude but no chart data
2. Calculates charts for those events using the Flask API
3. Stores chart data in the event_chart_data table
4. Updates house mappings with actual_house_number

Usage:
    python3 scripts/backfill_event_charts.py [--dry-run] [--limit N]
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
from typing import List, Dict, Optional

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.parent.resolve()

# Load .env files from script directory
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', os.getenv('SUPABASE_KEY', ''))
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:8000')

def get_events_needing_charts(supabase: Client, limit: Optional[int] = None) -> List[Dict]:
    """Get events that need chart calculation."""
    try:
        # Get events with location but no chart data
        query = supabase.table('events').select('*')
        
        # Filter for events with latitude and longitude
        response = query.execute()
        events = response.data if response.data else []
        
        events_needing_charts = []
        for event in events:
            if not (event.get('latitude') and event.get('longitude') and event.get('date')):
                continue
            
            # Check if chart data exists
            chart_response = supabase.table('event_chart_data').select('id').eq('event_id', event['id']).execute()
            if not chart_response.data:
                events_needing_charts.append(event)
                if limit and len(events_needing_charts) >= limit:
                    break
        
        return events_needing_charts
    except Exception as e:
        print(f"❌ Error fetching events: {e}")
        return []

def calculate_and_store_chart(supabase: Client, event: Dict, dry_run: bool = False) -> bool:
    """Calculate and store chart for an event."""
    try:
        chart_request = {
            'date': event['date'],
            'time': event.get('event_time', '12:00:00'),
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'timezone': event.get('timezone', 'UTC'),
        }
        
        print(f"  📊 Calculating chart for event {event['id']} ({event.get('title', 'Untitled')})...")
        print(f"     Date: {chart_request['date']}, Time: {chart_request['time']}")
        print(f"     Location: {chart_request['latitude']}, {chart_request['longitude']}")
        
        if dry_run:
            print(f"  [DRY RUN] Would calculate chart for event {event['id']}")
            return True
        
        response = requests.post(
            f'{FLASK_API_URL}/api/chart/calculate',
            json=chart_request,
            timeout=30
        )
        
        if not response.ok:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            print(f"     ❌ Failed: {error_data.get('error', 'Unknown error')}")
            return False
        
        chart_data = response.json()
        
        if not chart_data.get('success') or not chart_data.get('chart'):
            print(f"     ❌ Invalid response from Flask API")
            return False
        
        chart = chart_data['chart']
        
        # Store in database
        chart_record = {
            'event_id': event['id'],
            'ascendant_degree': chart['ascendant_degree'],
            'ascendant_rasi': chart['ascendant_rasi'],
            'ascendant_rasi_number': chart['ascendant_rasi_number'],
            'ascendant_nakshatra': chart.get('ascendant_nakshatra'),
            'ascendant_lord': chart['ascendant_lord'],
            'house_cusps': chart['house_cusps'],
            'house_system': chart['house_system'],
            'julian_day': chart['julian_day'],
            'sidereal_time': chart.get('sidereal_time'),
            'ayanamsa': chart['ayanamsa'],
            'planetary_positions': chart['planetary_positions'],
            'planetary_strengths': chart['planetary_strengths'],
        }
        
        result = supabase.table('event_chart_data').upsert(
            [chart_record],
            on_conflict='event_id'
        ).execute()
        
        if result.data:
            print(f"     ✅ Stored chart data (Ascendant: {chart['ascendant_rasi']} {chart['ascendant_degree']:.2f}°)")
            return True
        else:
            print(f"     ❌ Failed to store chart data")
            return False
            
    except requests.exceptions.Timeout:
        print(f"     ❌ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"     ❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Backfill chart data for existing events')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--limit', type=int, help='Limit the number of events to process')
    args = parser.parse_args()
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local")
        sys.exit(1)
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("🔍 Finding events that need chart calculations...")
    events = get_events_needing_charts(supabase, args.limit)
    
    if not events:
        print("✅ No events need chart calculations")
        return
    
    print(f"📊 Found {len(events)} event(s) needing chart calculations")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")
    
    print("")
    success_count = 0
    fail_count = 0
    
    for i, event in enumerate(events, 1):
        print(f"[{i}/{len(events)}] Processing event {event['id']}: {event.get('title', 'Untitled')}")
        
        if calculate_and_store_chart(supabase, event, args.dry_run):
            success_count += 1
        else:
            fail_count += 1
        
        print("")  # Empty line between events
    
    print("=" * 60)
    if args.dry_run:
        print(f"🔍 DRY RUN COMPLETE")
        print(f"   Would process: {len(events)} events")
    else:
        print(f"✅ Backfill complete: {success_count}/{len(events)} charts calculated successfully")
        if fail_count > 0:
            print(f"❌ Failed: {fail_count} events")
    print("=" * 60)

if __name__ == '__main__':
    main()

