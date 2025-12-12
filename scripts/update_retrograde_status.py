#!/usr/bin/env python3
"""
Script to update retrograde status for Rahu and Ketu in existing planetary_data records.

This fixes retrograde status in the database:
- Rahu: Always retrograde (True)
- Ketu: Always retrograde (True)
- Sun: Never retrograde (False)
- Moon: Never retrograde (False)
- Other planets: Keep existing status (based on speed)

Usage:
    python3 scripts/update_retrograde_status.py [--date YYYY-MM-DD] [--all]
"""

import os
import sys
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

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

def fix_retrograde_status(planetary_data_dict: dict) -> dict:
    """Fix retrograde status according to Vedic astrology rules"""
    if not planetary_data_dict or 'planets' not in planetary_data_dict.get('planetary_data', {}):
        return planetary_data_dict
    
    planets = planetary_data_dict['planetary_data']['planets']
    
    for planet in planets:
        planet_name = planet.get('name', '')
        
        # Vedic astrology rules:
        if planet_name == 'Rahu':
            planet['is_retrograde'] = True  # Always retrograde
        elif planet_name == 'Ketu':
            planet['is_retrograde'] = True  # Always retrograde
        elif planet_name == 'Sun':
            planet['is_retrograde'] = False  # Never retrograde
        elif planet_name == 'Moon':
            planet['is_retrograde'] = False  # Never retrograde
        # Other planets keep their existing status (already calculated from speed)
    
    return planetary_data_dict

def update_planetary_data_record(supabase: Client, record_id: int, fixed_data: dict) -> bool:
    """Update a single planetary_data record"""
    try:
        result = supabase.table('planetary_data').update({
            'planetary_data': fixed_data['planetary_data']
        }).eq('id', record_id).execute()
        
        return result.data is not None and len(result.data) > 0
    except Exception as e:
        print(f"  ❌ Error updating record {record_id}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update retrograde status in planetary_data records')
    parser.add_argument('--date', type=str, help='Update specific date (YYYY-MM-DD)')
    parser.add_argument('--all', action='store_true', help='Update all records in database')
    args = parser.parse_args()
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local")
        sys.exit(1)
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Fetch records to update
    if args.date:
        print(f"🔍 Fetching planetary data for date: {args.date}")
        query = supabase.table('planetary_data').select('*').eq('date', args.date)
        records = query.execute().data or []
    elif args.all:
        print("🔍 Fetching all planetary data records...")
        records = supabase.table('planetary_data').select('*').execute().data or []
    else:
        print("❌ Error: Either --date YYYY-MM-DD or --all flag required")
        print("Usage: python3 scripts/update_retrograde_status.py --date 2025-12-12")
        print("   or: python3 scripts/update_retrograde_status.py --all")
        sys.exit(1)
    
    if not records:
        print("⚠️  No records found to update")
        return
    
    print(f"📊 Found {len(records)} record(s) to update\n")
    
    updated_count = 0
    error_count = 0
    
    for record in records:
        record_id = record['id']
        date = record['date']
        planetary_data = record['planetary_data']
        
        print(f"[{updated_count + error_count + 1}/{len(records)}] Updating {date} (ID: {record_id})...")
        
        # Fix retrograde status
        fixed_data = {
            'planetary_data': planetary_data
        }
        fixed_data = fix_retrograde_status(fixed_data)
        
        # Check if changes were made
        original_planets = {p['name']: p.get('is_retrograde') for p in planetary_data.get('planets', [])}
        fixed_planets = {p['name']: p.get('is_retrograde') for p in fixed_data['planetary_data'].get('planets', [])}
        
        changes = []
        for planet_name in ['Rahu', 'Ketu', 'Sun', 'Moon']:
            if planet_name in original_planets and planet_name in fixed_planets:
                if original_planets[planet_name] != fixed_planets[planet_name]:
                    changes.append(f"{planet_name}: {original_planets[planet_name]} → {fixed_planets[planet_name]}")
        
        if changes:
            print(f"  📝 Changes: {', '.join(changes)}")
            if update_planetary_data_record(supabase, record_id, fixed_data):
                updated_count += 1
                print(f"  ✅ Updated successfully")
            else:
                error_count += 1
                print(f"  ❌ Failed to update")
        else:
            print(f"  ℹ️  No changes needed")
        
        print("")
    
    print("=" * 60)
    print(f"✅ Update complete: {updated_count} updated, {error_count} errors")
    print("=" * 60)

if __name__ == '__main__':
    main()

