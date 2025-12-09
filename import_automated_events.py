"""
Automated Event Collection Script
Uses OpenAI API to collect significant world events
Runs via cron: 30 11 * * * and 30 23 * * * (11:30 AM and 11:30 PM IST)
"""

import os
import sys
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import requests
from openai import OpenAI
from supabase import create_client, Client
from typing import List, Dict, Optional

load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:8000')

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client"""
    if not OPENAI_API_KEY:
        print("⚠️ OpenAI API key not set. Skipping automated event collection.")
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


def fetch_recent_events_via_openai(client: OpenAI, target_date: date) -> List[Dict]:
    """Fetch significant world events using OpenAI"""
    try:
        # Construct prompt for OpenAI
        date_str = target_date.strftime('%B %d, %Y')
        prompt = f"""List 3-5 significant world events that occurred on {date_str}. 
For each event, provide:
1. A clear, factual title
2. A 2-3 sentence description
3. Category (e.g., Natural Disaster, Political, Economic, Technology, Health, Social, etc.)
4. Location (City, Country format)
5. Impact level (low, medium, or high)
6. Relevant tags (2-4 keywords)

Format as JSON array with this structure:
[
  {{
    "title": "Event Title",
    "description": "Detailed description...",
    "category": "Category Name",
    "location": "City, Country",
    "impact_level": "medium",
    "tags": ["tag1", "tag2"]
  }}
]

Only include real, significant events. Be factual and objective."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo" for cheaper option
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides factual information about world events. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        import json
        # Remove markdown code blocks if present
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        events = json.loads(content)
        return events if isinstance(events, list) else []
    
    except Exception as e:
        print(f"❌ Error fetching events from OpenAI: {e}")
        return []


def get_planetary_data_for_date(target_date: date) -> Optional[Dict]:
    """Fetch planetary data for a specific date"""
    try:
        url = f"{FLASK_API_URL}/api/planets/daily"
        params = {'date': target_date.isoformat()}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get('planetary_data', {}).get('planets', [])
    
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch planetary data: {e}")
        return None


def store_event(supabase: Client, event_data: Dict, target_date: date, planetary_data: Optional[List]):
    """Store event in Supabase"""
    try:
        event_record = {
            'date': target_date.isoformat(),
            'title': event_data.get('title', ''),
            'description': event_data.get('description', ''),
            'category': event_data.get('category', 'Other'),
            'location': event_data.get('location', ''),
            'latitude': event_data.get('latitude'),
            'longitude': event_data.get('longitude'),
            'impact_level': event_data.get('impact_level', 'medium'),
            'event_type': 'world',
            'tags': event_data.get('tags', [])
        }
        
        result = supabase.table('events').insert(event_record).execute()
        
        if result.data:
            print(f"✅ Stored event: {event_record['title']}")
            return True
        else:
            print(f"❌ Failed to store event: {event_record['title']}")
            return False
    
    except Exception as e:
        print(f"❌ Error storing event: {e}")
        return False


def main():
    """Main function"""
    print(f"🤖 Starting Automated Event Collection - {datetime.now().isoformat()}")
    
    # Validate configuration
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)
    
    if not OPENAI_API_KEY:
        print("⚠️ Warning: OPENAI_API_KEY not set. Cannot collect events.")
        sys.exit(0)  # Exit gracefully, not an error
    
    # Initialize clients
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    openai_client = get_openai_client()
    
    if not openai_client:
        sys.exit(0)
    
    # Determine target date (default to yesterday, as we're collecting events that happened)
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"❌ Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        # Default to yesterday (events that already happened)
        target_date = date.today() - timedelta(days=1)
    
    print(f"📅 Collecting events for: {target_date.isoformat()}")
    
    # Fetch events from OpenAI
    events = fetch_recent_events_via_openai(openai_client, target_date)
    
    if not events:
        print("⚠️ No events collected from OpenAI")
        sys.exit(0)
    
    print(f"📰 Found {len(events)} events")
    
    # Get planetary data for the date
    planetary_data = get_planetary_data_for_date(target_date)
    
    if not planetary_data:
        print("⚠️ Warning: No planetary data available for this date")
    
    # Store each event
    success_count = 0
    for event in events:
        if store_event(supabase, event, target_date, planetary_data):
            success_count += 1
    
    print(f"✅ Successfully stored {success_count}/{len(events)} events")
    
    if success_count > 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
