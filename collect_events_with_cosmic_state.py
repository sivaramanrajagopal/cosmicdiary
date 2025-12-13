#!/usr/bin/env python3
"""
Enhanced Event Collection Script with Cosmic State Correlation

This script runs every 2 hours to:
1. Capture current cosmic state (Lagna, planets, aspects) at reference location
2. Detect world events via OpenAI
3. Calculate individual event charts
4. Correlate events with cosmic snapshot
5. Store all data in database

Author: Cosmic Diary System
Date: 2025-12-12
"""

import os
import sys
import json
from datetime import datetime, timezone, date, time, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
SCRIPT_DIR = Path(__file__).parent.resolve()
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

# Database and API clients
from supabase import create_client, Client
from openai import OpenAI

# Geocoding for location lookup
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    GEOCODING_AVAILABLE = True
except ImportError:
    GEOCODING_AVAILABLE = False
    print("⚠️  geopy not available - will skip geocoding")

# Our astrological calculation modules
from astro_calculations import calculate_complete_chart
from aspect_calculator import calculate_all_aspects
from correlation_analyzer import (
    correlate_event_with_snapshot,
    extract_retrograde_planets,
    extract_planet_houses,
    extract_planet_rasis
)

# Import enhanced prompt system (same as import_automated_events.py)
sys.path.append(str(SCRIPT_DIR))
try:
    from prompts.event_detection_prompt import (
        SYSTEM_PROMPT,
        generate_user_prompt,
        validate_event_response,
        calculate_research_score,
        get_time_window,
        auto_map_event_to_astrology
    )
    PROMPT_SYSTEM_AVAILABLE = True
    print("✓ Prompt system imported successfully")
except ImportError as e:
    print(f"⚠️  WARNING: Could not import prompt system: {e}")
    print(f"⚠️  Script directory: {SCRIPT_DIR}")
    print(f"⚠️  Checking if prompts/event_detection_prompt.py exists...")
    prompts_path = SCRIPT_DIR / 'prompts' / 'event_detection_prompt.py'
    print(f"⚠️  Prompts file path: {prompts_path}")
    print(f"⚠️  File exists: {prompts_path.exists()}")
    PROMPT_SYSTEM_AVAILABLE = False
    # Raise the error so deployment fails visibly
    raise ImportError(f"Prompt system is required but could not be imported: {e}")

# Configuration
REFERENCE_LOCATION = {
    "name": "Delhi, India",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
}

# Initialize clients
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', os.getenv('SUPABASE_KEY', ''))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("⚠️  Warning: OPENAI_API_KEY not set. Event detection will be skipped.")
    sys.exit(0)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def print_header():
    """Print script header with run time."""
    run_time = datetime.now(timezone.utc)
    print("=" * 80)
    print("COSMIC DIARY - ENHANCED EVENT COLLECTION WITH COSMIC STATE CORRELATION")
    print(f"Run Time: {run_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print("")


def capture_cosmic_snapshot() -> Tuple[int, Dict[str, Any]]:
    """
    Capture current planetary state at reference location.
    
    Returns:
        Tuple of (snapshot_id, snapshot_chart_data)
        snapshot_id: Database ID of inserted snapshot
        snapshot_chart_data: Chart data dictionary for correlation
    
    Raises:
        Exception: If snapshot capture fails
    """
    print("STEP 1: CAPTURING COSMIC STATE")
    print("-" * 80)
    
    try:
        # Get current UTC time
        now_utc = datetime.now(timezone.utc)
        snapshot_time = now_utc.isoformat()
        
        # Format for chart calculation
        event_date = now_utc.date()
        event_time_obj = now_utc.time()
        
        print(f"📅 Snapshot Time: {snapshot_time}")
        print(f"📍 Reference Location: {REFERENCE_LOCATION['name']}")
        print(f"   Coordinates: ({REFERENCE_LOCATION['latitude']}, {REFERENCE_LOCATION['longitude']})")
        print(f"   Timezone: {REFERENCE_LOCATION['timezone']}")
        print("")
        
        # Calculate complete chart for reference location
        print("🔮 Calculating astrological chart...")
        chart_data = calculate_complete_chart(
            event_date=event_date,
            event_time=event_time_obj,
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        print("  ✓ Chart calculated successfully")
        
        # Calculate aspects
        print("⭐ Calculating planetary aspects...")
        planetary_positions = chart_data.get('planetary_positions', {})
        house_cusps = chart_data.get('house_cusps', [])
        active_aspects = calculate_all_aspects(planetary_positions, house_cusps)
        print(f"  ✓ Found {len(active_aspects)} active aspects")
        
        # Extract retrograde planets
        retrograde_planets = extract_retrograde_planets(chart_data)
        print(f"  ✓ Retrograde planets: {', '.join(retrograde_planets) if retrograde_planets else 'None'}")
        
        # Extract dominant planets (strength_score >= 0.7)
        dominant_planets = []
        planetary_strengths = chart_data.get('planetary_strengths', {})
        if isinstance(planetary_strengths, dict):
            for planet_name, strength_data in planetary_strengths.items():
                if isinstance(strength_data, dict):
                    strength_score = strength_data.get('strength_score', 0.0)
                    if strength_score >= 0.7:
                        dominant_planets.append({
                            "planet": planet_name,
                            "strength_score": strength_score,
                            "reasons": [
                                k for k, v in strength_data.items()
                                if k != 'strength_score' and v is True
                            ]
                        })
        
        # Sort by strength
        dominant_planets.sort(key=lambda x: x['strength_score'], reverse=True)
        print(f"  ✓ Dominant planets: {len(dominant_planets)} planets with strength >= 0.7")
        
        # Get Moon details
        moon_data = planetary_positions.get('Moon', {})
        moon_rasi = None
        moon_nakshatra = None
        
        if moon_data:
            moon_rasi_data = moon_data.get('rasi', {})
            if isinstance(moon_rasi_data, dict):
                moon_rasi = moon_rasi_data.get('name')
            
            moon_nakshatra_data = moon_data.get('nakshatra', {})
            if isinstance(moon_nakshatra_data, dict):
                moon_nakshatra = moon_nakshatra_data.get('name')
        
        # Prepare snapshot data for database
        snapshot_data = {
            "snapshot_time": snapshot_time,
            "reference_location": REFERENCE_LOCATION['name'],
            "reference_latitude": REFERENCE_LOCATION['latitude'],
            "reference_longitude": REFERENCE_LOCATION['longitude'],
            "reference_timezone": REFERENCE_LOCATION['timezone'],
            "lagna_degree": chart_data.get('ascendant_degree', 0.0),
            "lagna_rasi": chart_data.get('ascendant_rasi', ''),
            "lagna_rasi_number": chart_data.get('ascendant_rasi_number', 1),
            "lagna_nakshatra": chart_data.get('ascendant_nakshatra'),
            "lagna_lord": chart_data.get('ascendant_lord', ''),
            "house_cusps": chart_data.get('house_cusps', []),
            "planetary_positions": planetary_positions,
            "active_aspects": active_aspects,
            "retrograde_planets": retrograde_planets,
            "dominant_planets": dominant_planets if dominant_planets else None,
            "moon_rasi": moon_rasi,
            "moon_nakshatra": moon_nakshatra,
            "ayanamsa": chart_data.get('ayanamsa', 0.0)
        }
        
        # Insert into database
        print("💾 Storing cosmic snapshot in database...")
        result = supabase.table('cosmic_snapshots').insert(snapshot_data).execute()
        
        if not result.data or len(result.data) == 0:
            raise Exception("Failed to insert cosmic snapshot into database")
        
        snapshot_id = result.data[0]['id']
        print(f"  ✓ Snapshot stored with ID: {snapshot_id}")
        print("")
        
        # Print summary
        print("📊 Snapshot Summary:")
        print(f"   Lagna: {chart_data.get('ascendant_rasi')} ({chart_data.get('ascendant_degree', 0):.2f}°)")
        print(f"   Retrograde Planets: {len(retrograde_planets)}")
        if dominant_planets:
            top_3 = dominant_planets[:3]
            print(f"   Top Dominant Planets: {', '.join([p['planet'] for p in top_3])}")
        print(f"   Active Aspects: {len(active_aspects)}")
        print("")
        
        return snapshot_id, chart_data
    
    except Exception as e:
        print(f"  ✗ Error capturing cosmic snapshot: {e}")
        raise


def detect_events_openai(lookback_hours: int = None) -> List[Dict[str, Any]]:
    """
    Detect world events using OpenAI API.
    
    Args:
        lookback_hours: Number of hours to look back for events. 
                       None = use default (from env or 2 hours)
                       1 = on-demand manual run
                       2 = scheduled GitHub Actions
    
    Returns:
        List of validated event dictionaries
    
    Raises:
        Exception: If event detection fails
    """
    print("STEP 2: DETECTING EVENTS VIA OPENAI")
    print("-" * 80)
    
    if not PROMPT_SYSTEM_AVAILABLE:
        print("❌ ERROR: Prompt system not available. Cannot proceed with event detection.")
        raise RuntimeError("Prompt system is required but not available")
    
    if not openai_client:
        print("⚠️  OpenAI client not initialized. Skipping event detection.")
        return []
    
    try:
        # Get time window with specified lookback hours
        time_window = get_time_window(lookback_hours=lookback_hours)
        
        lookback_h = time_window.get('lookback_hours', 2)
        print(f"📅 Detecting events for time window:")
        print(f"   Lookback: {lookback_h} hour(s)")
        print(f"   Start: {time_window['start']} UTC")
        print(f"   End: {time_window['end']} UTC")
        print("")
        
        # Generate user prompt using the prompt system
        user_prompt = generate_user_prompt(time_window)
        
        print("🤖 Calling OpenAI API with enhanced astrological prompts...")
        print(f"📝 Using SYSTEM_PROMPT from prompts/event_detection_prompt.py")
        print(f"📝 User prompt length: {len(user_prompt)} characters")
        print(f"📝 SYSTEM_PROMPT length: {len(SYSTEM_PROMPT)} characters")
        
        try:
            # For JSON mode, we need to ensure the prompt asks for JSON
            # Update user prompt to explicitly request JSON format
            json_user_prompt = user_prompt + "\n\nIMPORTANT: Return ONLY valid JSON. Your response must be a JSON object with an 'events' array."
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json_user_prompt}
                ],
                temperature=0.7,
                max_tokens=3500,  # Match import_automated_events.py
                response_format={"type": "json_object"}  # Force JSON response format
            )
        except Exception as api_error:
            print(f"❌ ERROR: OpenAI API call failed: {api_error}")
            print(f"   Error type: {type(api_error).__name__}")
            import traceback
            traceback.print_exc()
            raise
        
        # Check if response has content
        if not response.choices or len(response.choices) == 0:
            print("❌ ERROR: OpenAI returned empty choices array")
            print("   Response structure:", response)
            return []
        
        content = response.choices[0].message.content
        
        if not content:
            print("❌ ERROR: OpenAI returned empty content")
            print("   Response choices:", response.choices)
            return []
        
        content = content.strip()
        
        # Debug: Log response details
        print(f"📥 OpenAI response received")
        print(f"   Content length: {len(content)} characters")
        print(f"   Preview (first 500 chars): {content[:500]}")
        
        # Check if content is empty after stripping
        if not content:
            print("❌ ERROR: Content is empty after stripping whitespace")
            return []
        
        # Parse JSON - handle markdown code blocks (same logic as import_automated_events.py)
        original_content = content
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        # Check again after removing markdown
        if not content:
            print("❌ ERROR: Content is empty after removing markdown code blocks")
            print(f"   Original content preview: {original_content[:200]}")
            return []
        
        try:
            events = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error at position {e.pos}: {e.msg}")
            print(f"📄 Content length: {len(content)}")
            print(f"📄 Content preview (first 1000 chars): {content[:1000]}")
            if e.pos and e.pos < len(content):
                print(f"📄 Content around error position {e.pos}:")
                start = max(0, e.pos - 200)
                end = min(len(content), e.pos + 200)
                print(f"   ...{content[start:e.pos]}>>>ERROR<<<{content[e.pos:end]}...")
            else:
                print(f"📄 Full content: {content}")
            
            # Try to extract JSON from the response if it's wrapped in text
            print("🔧 Attempting to extract JSON from response...")
            import re
            json_match = re.search(r'\{.*\[.*\]\.*\}', content, re.DOTALL)
            if json_match:
                try:
                    extracted_json = json_match.group(0)
                    events = json.loads(extracted_json)
                    print("✓ Successfully extracted JSON from response")
                except:
                    print("✗ Failed to extract valid JSON")
                    return []
            else:
                print("✗ No JSON pattern found in response")
                return []
        
        # Handle different response formats (same as import_automated_events.py)
        if not isinstance(events, list):
            # Sometimes OpenAI wraps in an object
            if isinstance(events, dict):
                # Check common wrapper keys
                if 'events' in events:
                    events = events['events']
                elif 'data' in events:
                    events = events['data']
                elif 'results' in events:
                    events = events['results']
                else:
                    # If it's a single event object, wrap it
                    # Check if it has event-like structure
                    if 'title' in events or 'date' in events:
                        events = [events]
                    else:
                        print(f"⚠️  WARNING: Unexpected response format. Keys: {list(events.keys())}")
                        events = []
            else:
                print(f"⚠️  WARNING: Events is not a list or dict, type: {type(events)}")
                events = []
        
        print(f"  ✓ Received {len(events)} events from OpenAI")
        
        if len(events) == 0:
            print("")
            print("⚠️  WARNING: OpenAI returned 0 events!")
            print("   Possible reasons:")
            print("   1. No significant events in the specified time window")
            print("   2. Prompt may be too restrictive for a short time window")
            print("   3. OpenAI API may have rate limiting or issues")
            print("   4. The time window might be too short")
            print("")
            print("🔧 SUGGESTIONS:")
            print("   - Check if there were actually events in the time window")
            print("   - Try increasing lookback_hours if this is a scheduled run")
            print("   - Check OpenAI API status and usage limits")
            print("")
            return []
        
        print("")
        
        # Log sample event structure for debugging
        if events:
            print("📋 Sample event structure from OpenAI:")
            print(json.dumps(events[0], indent=2)[:500] + "...")
            print("")
        
        # Validate and score events using prompt system validators
        print("-" * 80)
        print("STEP 2b: VALIDATING AND SCORING EVENTS")
        print("-" * 80)
        
        validated_events = []
        validation_stats = {
            'total': len(events),
            'valid': 0,
            'invalid': 0,
            'reasons': {}
        }
        
        for event in events:
            # Normalize category first (before validation)
            # Map OpenAI category variations to our standard categories
            category_mapping = {
                'natural disaster': 'Natural Disasters',
                'natural disasters': 'Natural Disasters',
                'economic event': 'Economic Events',
                'economic events': 'Economic Events',
                'economic': 'Economic Events',
                'political event': 'Political Events',
                'political events': 'Political Events',
                'political': 'Political Events',
                'health crisis': 'Health & Medical',
                'health & medical': 'Health & Medical',
                'health': 'Health & Medical',
                'medical': 'Health & Medical',
                'technology': 'Technology & Innovation',
                'tech': 'Technology & Innovation',
                'technology & innovation': 'Technology & Innovation',
                'business': 'Business & Commerce',
                'commerce': 'Business & Commerce',
                'business & commerce': 'Business & Commerce',
                'war': 'Wars & Conflicts',
                'conflict': 'Wars & Conflicts',
                'wars & conflicts': 'Wars & Conflicts',
                'employment': 'Employment & Labor',
                'labor': 'Employment & Labor',
                'employment & labor': 'Employment & Labor',
                'women & children': 'Women & Children',
                'entertainment': 'Entertainment & Sports',
                'sports': 'Entertainment & Sports',
                'entertainment & sports': 'Entertainment & Sports',
            }
            
            if event.get('category'):
                event_category_lower = event['category'].lower().strip()
                if event_category_lower in category_mapping:
                    event['category'] = category_mapping[event_category_lower]
                    print(f"  🔄 Normalized category: {event.get('category', 'Unknown')}")
            
            # First try strict validation
            is_valid, reason = validate_event_response(event, lenient=False)
            
            # If validation fails but has basic fields, try lenient validation
            if not is_valid and event.get('title') and event.get('date'):
                # Try lenient validation (allows missing astrological mapping)
                is_valid_lenient, reason_lenient = validate_event_response(event, lenient=True)
                
                if is_valid_lenient:
                    # Auto-map astrological relevance if missing
                    if not event.get('astrological_relevance') or \
                       not event.get('astrological_relevance', {}).get('primary_houses'):
                        print(f"  🔮 Auto-mapping astrological relevance for: {event.get('title', 'Unknown')[:50]}")
                        event['astrological_relevance'] = auto_map_event_to_astrology(event)
                    
                    # Calculate research score
                    event['research_score'] = calculate_research_score(event)
                    validated_events.append(event)
                    validation_stats['valid'] += 1
                    print(f"  ✓ Validated (lenient): {event.get('title', 'Unknown')[:50]}")
                    continue
            
            # Strict validation passed
            if is_valid:
                # Calculate research score using prompt system
                event['research_score'] = calculate_research_score(event)
                validated_events.append(event)
                validation_stats['valid'] += 1
                print(f"  ✓ Validated: {event.get('title', 'Unknown')[:50]} (Score: {event.get('research_score', 0):.1f})")
            else:
                validation_stats['invalid'] += 1
                if reason not in validation_stats['reasons']:
                    validation_stats['reasons'][reason] = 0
                validation_stats['reasons'][reason] += 1
                print(f"  ⚠️  Skipping event '{event.get('title', 'Unknown')[:60]}': {reason}")
                
                # Show more details for debugging
                print(f"      Category: {event.get('category', 'N/A')}")
                print(f"      Impact: {event.get('impact_level', 'N/A')}")
                print(f"      Has astro: {bool(event.get('astrological_relevance'))}")
        
        print(f"✓ Validated: {validation_stats['valid']}/{validation_stats['total']} events")
        if validation_stats['invalid'] > 0:
            print(f"✗ Invalid: {validation_stats['invalid']} events")
            if validation_stats['reasons']:
                print("  Reasons:")
                for reason, count in validation_stats['reasons'].items():
                    print(f"    - {reason}: {count}")
        print("")
        
        if not validated_events:
            print("⚠️  No valid events after validation")
            print("🔍 DEBUGGING: Checking what OpenAI returned...")
            if events:
                print(f"   - OpenAI returned {len(events)} events")
                print("   - Sample of rejected events:")
                rejected_count = 0
                for event in events[:3]:  # Show first 3 rejected events
                    print(f"     {rejected_count + 1}. Title: {event.get('title', 'N/A')[:60]}")
                    print(f"        Category: {event.get('category', 'N/A')}")
                    print(f"        Impact: {event.get('impact_level', 'N/A')}")
                    rejected_count += 1
            else:
                print("   - OpenAI returned 0 events (empty response)")
                print("   - Possible reasons:")
                print("     * No significant events in the time window")
                print("     * Prompt too restrictive for short time window")
                print("     * OpenAI API issue or rate limiting")
            return []
        
        # Sort by research score and take top 15
        validated_events.sort(key=lambda x: x.get('research_score', 0), reverse=True)
        selected_events = validated_events[:15]
        
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
        
        print("📊 Event Detection Summary:")
        print(f"   Events from OpenAI: {len(events)}")
        print(f"   Validated events: {len(validated_events)}")
        print(f"   Selected for processing: {len(selected_events)}")
        print(f"   Categories: {', '.join([f'{k}({v})' for k, v in categories.items()])}")
        print("")
        
        return selected_events
    
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parsing error: {e}")
        print(f"  📄 Raw response (first 500 chars): {content[:500] if 'content' in locals() else 'N/A'}")
        raise
    except Exception as e:
        print(f"  ✗ Error detecting events: {e}")
        import traceback
        traceback.print_exc()
        raise


def store_event_with_chart(event: Dict[str, Any]) -> Tuple[Optional[int], Optional[Dict[str, Any]]]:
    """
    Store event in database and calculate its chart if time/location available.
    
    Args:
        event: Event dictionary with all required fields
    
    Returns:
        Tuple of (event_id, chart_data) if successful, (None, None) otherwise
    """
    try:
        # Extract astrological relevance if available (from prompt system)
        astro_relevance = event.get('astrological_relevance', {})
        astrological_metadata = None
        if astro_relevance:
            astrological_metadata = {
                'primary_houses': astro_relevance.get('primary_houses', []),
                'primary_planets': astro_relevance.get('primary_planets', []),
                'keywords': astro_relevance.get('keywords', []),
                'reasoning': astro_relevance.get('reasoning', '')
            }
        
        # Extract impact_metrics (from prompt system)
        impact_metrics = event.get('impact_metrics', {})
        
        # Extract sources (from prompt system)
        sources = event.get('sources', [])
        if not isinstance(sources, list):
            sources = []
        
        # Prepare event data for events table (matching import_automated_events.py structure)
        event_data = {
            "date": event.get('date'),
            "title": event.get('title'),
            "description": event.get('description', ''),
            "category": event.get('category', 'Other'),
            "location": event.get('location', ''),
            "latitude": event.get('latitude'),
            "longitude": event.get('longitude'),
            "impact_level": event.get('impact_level', 'medium'),
            "event_type": 'world',
            "tags": event.get('tags', []),
            # Enhanced time fields
            "event_time": event.get('time') if event.get('time') and event.get('time') != 'estimated' else None,
            "timezone": event.get('timezone', 'UTC'),
            "has_accurate_time": event.get('time') is not None and event.get('time') != 'estimated',
            # Enhanced astrological metadata fields (from prompt system)
            "astrological_metadata": astrological_metadata,
            "impact_metrics": impact_metrics if impact_metrics else None,
            "research_score": event.get('research_score'),
            "sources": sources
        }
        
        print(f"    📝 Attempting to store: {event_data.get('title', 'Unknown')}")
        print(f"       Date: {event_data.get('date')}, Location: {event_data.get('location')}")
        
        # Insert into events table
        result = supabase.table('events').insert(event_data).execute()
        
        if not result.data or len(result.data) == 0:
            print(f"    ✗ Database insert returned no data")
            if hasattr(result, 'error') and result.error:
                print(f"    ✗ Database error: {result.error}")
            return None, None
        
        event_id = result.data[0]['id']
        
        # Try to get coordinates if missing
        event_lat = event.get('latitude')
        event_lng = event.get('longitude')
        coordinates_updated = False
        
        if (event_lat is None or event_lng is None) and event.get('location'):
            print(f"    🔍 Geocoding location: {event.get('location')}")
            try:
                if GEOCODING_AVAILABLE:
                    geolocator = Nominatim(user_agent="cosmic-diary/1.0", timeout=10)
                    location_obj = geolocator.geocode(event.get('location'))
                    if location_obj:
                        event_lat = location_obj.latitude
                        event_lng = location_obj.longitude
                        print(f"    ✓ Geocoded: {event_lat:.4f}, {event_lng:.4f}")
                        coordinates_updated = True
                    else:
                        print(f"    ⚠️  Could not geocode location")
            except (GeocoderTimedOut, GeocoderServiceError, Exception) as e:
                print(f"    ⚠️  Geocoding error: {e}")
        
        # Use default coordinates for India if still missing and location mentions India
        if (event_lat is None or event_lng is None) and event.get('location', '').lower().find('india') != -1:
            print(f"    📍 Using default India coordinates (Delhi)")
            event_lat = 28.6139  # Delhi
            event_lng = 77.2090
            coordinates_updated = True
        
        # Update event in database with geocoded coordinates if we got them
        if coordinates_updated and event_lat is not None and event_lng is not None:
            try:
                update_result = supabase.table('events').update({
                    'latitude': event_lat,
                    'longitude': event_lng
                }).eq('id', event_id).execute()
                
                if update_result.data:
                    print(f"    ✓ Updated event with coordinates: {event_lat:.4f}, {event_lng:.4f}")
                else:
                    print(f"    ⚠️  Could not update event coordinates in database")
            except Exception as e:
                print(f"    ⚠️  Error updating event coordinates: {e}")
        
        # Calculate and store chart if time and coordinates available
        # Check for both 'time' (from OpenAI) and 'event_time' (already converted)
        event_time_str = event.get('event_time') or event.get('time')
        
        if (event_time_str and 
            event_lat is not None and 
            event_lng is not None):
            
            try:
                # Parse date and time
                event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
                time_parts = event_time_str.split(':')
                event_time_obj = time(
                    int(time_parts[0]),
                    int(time_parts[1]) if len(time_parts) > 1 else 0,
                    int(time_parts[2]) if len(time_parts) > 2 else 0
                )
                
                # Get timezone (default to UTC if not set)
                timezone_str = event.get('timezone') or 'UTC'
                
                # Calculate chart
                chart_data = calculate_complete_chart(
                    event_date=event_date,
                    event_time=event_time_obj,
                    latitude=event_lat,
                    longitude=event_lng,
                    timezone_str=timezone_str
                )
                
                # Prepare chart data for database
                chart_db_data = {
                    "event_id": event_id,
                    "ascendant_degree": chart_data.get('ascendant_degree', 0.0),
                    "ascendant_rasi": chart_data.get('ascendant_rasi', ''),
                    "ascendant_rasi_number": chart_data.get('ascendant_rasi_number', 1),
                    "ascendant_nakshatra": chart_data.get('ascendant_nakshatra'),
                    "ascendant_lord": chart_data.get('ascendant_lord', ''),
                    "house_cusps": chart_data.get('house_cusps', []),
                    "house_system": chart_data.get('house_system', 'Placidus'),
                    "julian_day": chart_data.get('julian_day', 0.0),
                    "sidereal_time": chart_data.get('sidereal_time'),
                    "ayanamsa": chart_data.get('ayanamsa', 0.0),
                    "planetary_positions": chart_data.get('planetary_positions', {}),
                    "planetary_strengths": chart_data.get('planetary_strengths')
                }
                
                # Insert into event_chart_data table
                chart_insert_result = supabase.table('event_chart_data').insert(chart_db_data).execute()
                if chart_insert_result.data and len(chart_insert_result.data) > 0:
                    print(f"    ✓ Chart data stored for event {event_id}")
                else:
                    print(f"    ⚠️  Chart data insert returned no data (may already exist)")
                
                return event_id, chart_data
            
            except Exception as e:
                print(f"    ⚠️  Could not calculate chart: {e}")
                return event_id, None
        
        return event_id, None
    
    except Exception as e:
        print(f"    ✗ Error storing event: {e}")
        return None, None


def correlate_and_store(
    event_id: int,
    event_chart: Dict[str, Any],
    snapshot_id: int,
    snapshot_chart: Dict[str, Any]
) -> bool:
    """
    Correlate event with snapshot and store results.
    
    Args:
        event_id: Database ID of the event
        event_chart: Event chart data dictionary
        snapshot_id: Database ID of the snapshot
        snapshot_chart: Snapshot chart data dictionary
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Correlate event with snapshot
        correlation_data = correlate_event_with_snapshot(
            event_chart=event_chart,
            snapshot_chart=snapshot_chart,
            snapshot_id=snapshot_id
        )
        
        # Prepare correlation data for database
        correlation_db_data = {
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "correlation_score": correlation_data.get('correlation_score', 0.0),
            "matching_factors": correlation_data.get('correlations', []),
            "total_matches": correlation_data.get('total_matches', 0)
        }
        
        # Insert into event_cosmic_correlations table
        correlation_insert_result = supabase.table('event_cosmic_correlations').insert(correlation_db_data).execute()
        
        if correlation_insert_result.data and len(correlation_insert_result.data) > 0:
            print(f"    ✓ Correlation stored (Score: {correlation_db_data['correlation_score']:.2f}, Matches: {correlation_db_data['total_matches']})")
            return True
        else:
            print(f"    ✗ Correlation insert returned no data")
            if hasattr(correlation_insert_result, 'error') and correlation_insert_result.error:
                print(f"    ✗ Database error: {correlation_insert_result.error}")
            return False
    
    except Exception as e:
        print(f"    ✗ Error correlating and storing: {e}")
        return False


def main():
    """
    Main execution flow.
    
    Command line arguments:
        --lookback-hours N: Number of hours to look back for events (default: 2)
                            Use 1 for on-demand manual runs
                            Use 2 for scheduled GitHub Actions
    """
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Collect events with cosmic state correlation')
    parser.add_argument(
        '--lookback-hours',
        type=int,
        default=None,
        help='Number of hours to look back for events (default: 2, or from EVENT_LOOKBACK_HOURS env var)'
    )
    args = parser.parse_args()
    
    # Determine lookback hours
    lookback_hours = args.lookback_hours
    if lookback_hours is None:
        # Check environment variable
        lookback_hours = int(os.getenv('EVENT_LOOKBACK_HOURS', '2'))
    
    print_header()
    print(f"🔍 Event Detection Mode: {lookback_hours} hour(s) lookback")
    print("")
    
    snapshot_id = None
    snapshot_chart = None
    events_detected = []
    events_stored = 0
    correlations_created = 0
    correlation_scores = []
    
    try:
        # STEP 1: Capture Cosmic Snapshot
        snapshot_id, snapshot_chart = capture_cosmic_snapshot()
        
        # STEP 2: Detect Events with specified lookback window
        events_detected = detect_events_openai(lookback_hours=lookback_hours)
        
        if not events_detected:
            print("⚠️  No events detected. Exiting.")
            return
        
        # STEP 3-4: Process Each Event
        print("STEP 3-4: PROCESSING EVENTS AND CORRELATIONS")
        print("-" * 80)
        
        for i, event in enumerate(events_detected, 1):
            print(f"[{i}/{len(events_detected)}] Processing: {event.get('title', 'Unknown')}")
            
            # Store event with chart
            result = store_event_with_chart(event)
            if result is None:
                print("  ✗ Failed to store event")
                continue
            
            event_id, event_chart = result
            events_stored += 1
            print(f"  ✓ Event stored (ID: {event_id})")
            
            # Correlate if chart was calculated
            if event_chart:
                success = correlate_and_store(
                    event_id=event_id,
                    event_chart=event_chart,
                    snapshot_id=snapshot_id,
                    snapshot_chart=snapshot_chart
                )
                
                if success:
                    correlations_created += 1
                    # Get correlation score for summary
                    correlation_result = correlate_event_with_snapshot(
                        event_chart=event_chart,
                        snapshot_chart=snapshot_chart,
                        snapshot_id=snapshot_id
                    )
                    correlation_scores.append(correlation_result.get('correlation_score', 0.0))
                    score = correlation_result.get('correlation_score', 0.0)
                    matches = correlation_result.get('total_matches', 0)
                    print(f"  ✓ Correlated (Score: {score:.2f}, Matches: {matches})")
            
            print("")
        
        # STEP 5: Summary
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"✓ Events Detected: {len(events_detected)}")
        print(f"✓ Events Stored: {events_stored}")
        print(f"✓ Correlations Created: {correlations_created}")
        if correlation_scores:
            avg_score = sum(correlation_scores) / len(correlation_scores)
            print(f"✓ Average Correlation Score: {avg_score:.2f}")
            print(f"✓ Highest Correlation Score: {max(correlation_scores):.2f}")
            print(f"✓ Lowest Correlation Score: {min(correlation_scores):.2f}")
        success_rate = (events_stored / len(events_detected) * 100) if events_detected else 0
        print(f"✓ Success Rate: {success_rate:.1f}%")
        print("=" * 80)
        print("")
        print("✅ Event collection completed successfully!")
        
    except Exception as e:
        print("")
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

