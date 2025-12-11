#!/usr/bin/env python3
"""Check what data was stored by the on-demand job"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
from datetime import date, datetime

# Load env
script_dir = Path(__file__).parent.resolve()
load_dotenv(script_dir / '.env.local')

supabase = create_client(
    os.getenv('SUPABASE_URL'), 
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)

print("=" * 60)
print("📊 Database Status Check")
print("=" * 60)

# Check planetary_data for today
today = date.today().isoformat()
print(f"\n1️⃣  Planetary Data for today ({today}):")
print("-" * 60)
result = supabase.table('planetary_data').select('date, id, created_at, updated_at').eq('date', today).execute()
if result.data:
    for row in result.data:
        print(f"   ✅ Date: {row['date']}")
        print(f"      ID: {row['id']}")
        print(f"      Created: {row['created_at']}")
        print(f"      Updated: {row['updated_at']}")
else:
    print(f"   ❌ No planetary data found for today")

# Check recent planetary data
print(f"\n2️⃣  Recent Planetary Data (last 5 days):")
print("-" * 60)
recent_planets = supabase.table('planetary_data').select('date, id, updated_at').order('date', desc=True).limit(5).execute()
if recent_planets.data:
    for row in recent_planets.data:
        print(f"   • {row['date']} (ID: {row['id']}, Updated: {row['updated_at'][:19]})")
else:
    print("   ❌ No planetary data found")

# Check events
print(f"\n3️⃣  Recent Events (last 5):")
print("-" * 60)
events = supabase.table('events').select('id, date, title, category, created_at').order('created_at', desc=True).limit(5).execute()
if events.data:
    for event in events.data:
        print(f"   • [{event['date']}] {event['title'][:50]}")
        print(f"     ID: {event['id']}, Category: {event['category']}")
        print(f"     Created: {event['created_at'][:19]}")
else:
    print("   ❌ No events found")

# Count summary
planetary_count = supabase.table('planetary_data').select('id', count='exact').execute()
events_count = supabase.table('events').select('id', count='exact').execute()

print(f"\n📈 Summary:")
print("-" * 60)
print(f"   Total Planetary Data Records: {planetary_count.count if hasattr(planetary_count, 'count') else 'N/A'}")
print(f"   Total Events: {events_count.count if hasattr(events_count, 'count') else 'N/A'}")

print("\n" + "=" * 60)
print("✅ Check complete!")
print("=" * 60)

