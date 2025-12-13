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

# Our astrological calculation modules
from astro_calculations import calculate_complete_chart
from aspect_calculator import calculate_all_aspects
from correlation_analyzer import (
    correlate_event_with_snapshot,
    extract_retrograde_planets,
    extract_planet_houses,
    extract_planet_rasis
)

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


def detect_events_openai() -> List[Dict[str, Any]]:
    """
    Detect world events using OpenAI API.
    
    Returns:
        List of validated event dictionaries
    
    Raises:
        Exception: If event detection fails
    """
    print("STEP 2: DETECTING EVENTS VIA OPENAI")
    print("-" * 80)
    
    try:
        # Get today's date for event detection
        today = date.today()
        date_str = today.strftime('%B %d, %Y')
        
        print(f"📅 Detecting events for: {date_str}")
        print("")
        
        # Generate prompt with better context and historical event examples
        # Note: If the date is in the future relative to OpenAI's training data, we'll ask for recent past events
        prompt = f"""You are an expert at identifying significant world events with astrological research value. 

Please list 10-15 significant world events that occurred around {date_str}. If you cannot find events for this exact date, please provide events from the past 2-3 days or the most recent significant events you know about.

IMPORTANT: 
- Focus on events with clear time and location information
- Prioritize events that could have astrological significance (major political changes, natural disasters, economic shifts, social movements, conflicts, technological breakthroughs)
- Include both major headlines and regionally significant events

For each event, provide:
1. A clear, factual title (required)
2. A 2-3 sentence description (required)
3. Category: One of: Natural Disaster, Political, Economic, Technology, Health, Social, War, Cultural, Scientific, Environmental (required)
4. Location: City, Country format, e.g., "Paris, France" (required)
5. Impact level: low, medium, high, or critical (required)
6. Relevant tags: 2-4 keywords (required)
7. Date: The actual date the event occurred in YYYY-MM-DD format (required)
8. Time: If known, the time in HH:MM:SS format (optional, use "estimated" if not known)
9. Latitude/Longitude: Coordinates if you know them, otherwise omit (optional)

Format as a JSON array ONLY (no markdown, no explanation):
[
  {{
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "title": "Event Title",
    "description": "Detailed description of what happened...",
    "category": "Category Name",
    "location": "City, Country",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "impact_level": "medium",
    "tags": ["tag1", "tag2"]
  }}
]

Return ONLY valid JSON. If you cannot find any events, return an empty array: []"""
        
        # Call OpenAI API
        print("🤖 Calling OpenAI API...")
        print(f"📝 Prompt length: {len(prompt)} characters")
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a research assistant specializing in world events and news. You always respond with valid JSON arrays only. Never add explanations or markdown formatting outside the JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Increased for more events
        )
        
        content = response.choices[0].message.content.strip()
        
        # Debug: Log first 500 chars of response
        print(f"📥 OpenAI response preview (first 500 chars): {content[:500]}")
        
        # Parse JSON - handle markdown code blocks
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        # Try to find JSON array in the response
        # Sometimes OpenAI wraps it or adds text
        if not content.startswith('['):
            # Try to extract JSON array
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
                print(f"📋 Extracted JSON array from response")
        
        try:
            events = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error at position {e.pos}: {e.msg}")
            print(f"📄 Content around error: {content[max(0, e.pos-100):e.pos+100]}")
            raise
        if not isinstance(events, list):
            events = [events] if events else []
        
        print(f"  ✓ Received {len(events)} events from OpenAI")
        print("")
        
        # Debug: Print first event structure if available
        if events:
            print(f"  📋 Sample event structure:")
            print(f"     {json.dumps(events[0], indent=2)[:200]}...")
            print("")
        
        # Validate and filter events
        validated_events = []
        skipped_count = 0
        for event in events:
            # Basic validation
            if not event.get('title'):
                print(f"  ⚠️  Skipping event (no title): {event}")
                skipped_count += 1
                continue
            if not event.get('date'):
                print(f"  ⚠️  Skipping event '{event.get('title')}' (no date)")
                skipped_count += 1
                continue
            
            # Ensure required fields
            validated_event = {
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
                "event_time": event.get('time'),
                "timezone": None,  # Will be detected if coordinates available
                "has_accurate_time": bool(event.get('time')),
                "research_score": 0.8  # Default score
            }
            
            validated_events.append(validated_event)
        
        # Sort by research_score (if available)
        validated_events.sort(key=lambda x: x.get('research_score', 0), reverse=True)
        
        # Take top 15
        selected_events = validated_events[:15]
        
        print("📊 Event Detection Summary:")
        print(f"   Events from OpenAI: {len(events)}")
        print(f"   Skipped (invalid): {skipped_count}")
        print(f"   Validated events: {len(validated_events)}")
        print(f"   Selected for processing: {len(selected_events)}")
        
        # Category breakdown
        categories = {}
        for event in selected_events:
            cat = event.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
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
        # Prepare event data for events table
        event_data = {
            "date": event.get('date'),
            "title": event.get('title'),
            "description": event.get('description', ''),
            "category": event.get('category', 'Other'),
            "location": event.get('location', ''),
            "latitude": event.get('latitude'),
            "longitude": event.get('longitude'),
            "impact_level": event.get('impact_level', 'medium'),
            "event_type": event.get('event_type', 'world'),
            "tags": event.get('tags', []),
            "event_time": event.get('event_time'),
            "timezone": event.get('timezone'),
            "has_accurate_time": event.get('has_accurate_time', False)
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
        
        # Calculate and store chart if time and location available
        if (event.get('event_time') and 
            event.get('latitude') is not None and 
            event.get('longitude') is not None):
            
            try:
                # Parse date and time
                event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
                time_parts = event['event_time'].split(':')
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
                    latitude=event['latitude'],
                    longitude=event['longitude'],
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
                supabase.table('event_chart_data').insert(chart_db_data).execute()
                
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
        supabase.table('event_cosmic_correlations').insert(correlation_db_data).execute()
        
        return True
    
    except Exception as e:
        print(f"    ✗ Error correlating and storing: {e}")
        return False


def main():
    """Main execution flow."""
    print_header()
    
    snapshot_id = None
    snapshot_chart = None
    events_detected = []
    events_stored = 0
    correlations_created = 0
    correlation_scores = []
    
    try:
        # STEP 1: Capture Cosmic Snapshot
        snapshot_id, snapshot_chart = capture_cosmic_snapshot()
        
        # STEP 2: Detect Events
        events_detected = detect_events_openai()
        
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

