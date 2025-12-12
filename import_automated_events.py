"""
Automated Event Collection Script (Enhanced)
Uses OpenAI API with astrologically-relevant prompts to collect significant world events
Runs via cron: 30 11 * * * and 30 23 * * * (11:30 AM and 11:30 PM IST)
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import requests
from openai import OpenAI
from supabase import create_client, Client
from typing import List, Dict, Optional

# Import enhanced prompt system
sys.path.append(os.path.dirname(__file__))
from prompts.event_detection_prompt import (
    SYSTEM_PROMPT,
    generate_user_prompt,
    validate_event_response,
    calculate_research_score
)

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
    """Fetch significant world events using OpenAI with enhanced astrological prompts"""
    try:
        print(f"📝 Generating enhanced prompt for event detection...")
        
        # Use time window from prompt system
        from prompts.event_detection_prompt import get_time_window
        time_window = get_time_window()
        
        # Generate user prompt
        user_prompt = generate_user_prompt(time_window)
        
        print(f"🤖 Calling OpenAI API with enhanced astrological prompts...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3500  # Increased for detailed responses
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        events = json.loads(content)
        if not isinstance(events, list):
            # Sometimes OpenAI wraps in an object
            if isinstance(events, dict) and 'events' in events:
                events = events['events']
            else:
                events = [events] if events else []
        
        print(f"  ✓ Received {len(events)} events from OpenAI")
        return events
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"   Response content: {content[:500]}...")
        return []
    except Exception as e:
        print(f"❌ Error fetching events from OpenAI: {e}")
        import traceback
        traceback.print_exc()
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


def store_event(supabase: Client, event_data: Dict, target_date: date, planetary_data: Optional[List]) -> Optional[int]:
    """Store event in Supabase with enhanced astrological metadata"""
    try:
        # Extract astrological relevance if available
        astro_relevance = event_data.get('astrological_relevance', {})
        
        # Prepare event record
        event_record = {
            'date': event_data.get('date', target_date.isoformat()),
            'title': event_data.get('title', ''),
            'description': event_data.get('description', ''),
            'category': event_data.get('category', 'Other'),
            'location': event_data.get('location', ''),
            'latitude': event_data.get('latitude'),
            'longitude': event_data.get('longitude'),
            'impact_level': event_data.get('impact_level', 'medium'),
            'event_type': 'world',
            'tags': event_data.get('tags', []),
            # Enhanced fields
            'event_time': event_data.get('time') if event_data.get('time') != 'estimated' else None,
            'timezone': event_data.get('timezone', 'UTC'),
            'has_accurate_time': event_data.get('time') is not None and event_data.get('time') != 'estimated'
        }
        
        result = supabase.table('events').insert(event_record).execute()
        
        if result.data and len(result.data) > 0:
            event_id = result.data[0]['id']
            print(f"✅ Stored event: {event_record['title']} (ID: {event_id})")
            return event_id
        else:
            print(f"❌ Failed to store event: {event_record['title']}")
            return None
    
    except Exception as e:
        print(f"❌ Error storing event: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function with enhanced logging and validation"""
    print("="*80)
    print("ENHANCED AUTOMATED EVENT COLLECTION - ASTROLOGICAL RESEARCH FOCUS")
    print("="*80)
    print(f"Run Time: {datetime.now().isoformat()}")
    print()
    
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
    print()
    
    # Fetch events from OpenAI
    print("-"*80)
    print("STEP 1: FETCHING EVENTS FROM OPENAI")
    print("-"*80)
    events = fetch_recent_events_via_openai(openai_client, target_date)
    
    if not events:
        print("⚠️ No events collected from OpenAI")
        sys.exit(0)
    
    print(f"✓ Received {len(events)} events from OpenAI")
    print()
    
    # Validate and score events
    print("-"*80)
    print("STEP 2: VALIDATING AND SCORING EVENTS")
    print("-"*80)
    
    validated_events = []
    validation_stats = {
        'total': len(events),
        'valid': 0,
        'invalid': 0,
        'reasons': {}
    }
    
    for event in events:
        is_valid, reason = validate_event_response(event)
        if is_valid:
            # Calculate research score
            event['research_score'] = calculate_research_score(event)
            validated_events.append(event)
            validation_stats['valid'] += 1
        else:
            validation_stats['invalid'] += 1
            if reason not in validation_stats['reasons']:
                validation_stats['reasons'][reason] = 0
            validation_stats['reasons'][reason] += 1
    
    print(f"✓ Validated: {validation_stats['valid']}/{validation_stats['total']} events")
    if validation_stats['invalid'] > 0:
        print(f"✗ Invalid: {validation_stats['invalid']} events")
        if validation_stats['reasons']:
            print("  Reasons:")
            for reason, count in validation_stats['reasons'].items():
                print(f"    - {reason}: {count}")
    print()
    
    if not validated_events:
        print("⚠️ No valid events after validation")
        sys.exit(0)
    
    # Sort by research score and take top 15
    validated_events.sort(key=lambda x: x.get('research_score', 0), reverse=True)
    selected_events = validated_events[:15]
    
    print("-"*80)
    print("STEP 3: SELECTING TOP EVENTS BY RESEARCH SCORE")
    print("-"*80)
    print(f"✓ Selected top {len(selected_events)} events (sorted by research score)")
    
    # Calculate statistics
    if selected_events:
        scores = [e.get('research_score', 0) for e in selected_events]
        avg_score = sum(scores) / len(scores)
        print(f"✓ Average research score: {avg_score:.2f}/100")
        print(f"✓ Score range: {min(scores):.2f} - {max(scores):.2f}")
        
        # Category breakdown
        categories = {}
        for event in selected_events:
            cat = event.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"✓ Category breakdown:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {cat}: {count}")
        
        # Time accuracy statistics
        exact_time = sum(1 for e in selected_events if e.get('time') and e.get('time') != 'estimated')
        estimated_time = sum(1 for e in selected_events if e.get('time') == 'estimated')
        no_time = len(selected_events) - exact_time - estimated_time
        
        print(f"✓ Time accuracy:")
        print(f"    - Exact time: {exact_time}")
        print(f"    - Estimated time: {estimated_time}")
        print(f"    - No time: {no_time}")
    print()
    
    # Get planetary data for the date
    print("-"*80)
    print("STEP 4: STORING EVENTS")
    print("-"*80)
    planetary_data = get_planetary_data_for_date(target_date)
    
    if not planetary_data:
        print("⚠️ Warning: No planetary data available for this date")
    print()
    
    # Store each event
    success_count = 0
    event_ids = []
    
    for i, event in enumerate(selected_events, 1):
        print(f"[{i}/{len(selected_events)}] Storing: {event.get('title', 'Unknown')[:60]}...")
        print(f"    Research Score: {event.get('research_score', 0):.2f}/100")
        
        event_id = store_event(supabase, event, target_date, planetary_data)
        if event_id:
            success_count += 1
            event_ids.append(event_id)
        print()
    
    # Final summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✓ Events from OpenAI: {len(events)}")
    print(f"✓ Events validated: {validation_stats['valid']}")
    print(f"✓ Events selected: {len(selected_events)}")
    print(f"✓ Events stored: {success_count}")
    if selected_events:
        print(f"✓ Average research score: {avg_score:.2f}/100")
    print(f"✓ Success rate: {(success_count/len(selected_events)*100) if selected_events else 0:.1f}%")
    print("="*80)
    print()
    
    if success_count > 0:
        print(f"✅ Successfully stored {success_count} events")
        sys.exit(0)
    else:
        print(f"❌ Failed to store any events")
        sys.exit(1)


if __name__ == '__main__':
    main()
