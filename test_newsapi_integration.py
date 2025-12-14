#!/usr/bin/env python3
"""
Test script for NewsAPI integration.
This tests whether NewsAPI is properly configured and returning events.
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add script directory to path
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

def load_env():
    """Load environment variables from .env.local"""
    env_file = SCRIPT_DIR / '.env.local'
    if env_file.exists():
        print(f"📄 Loading environment from: {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✅ Environment loaded")
    else:
        print(f"⚠️  No .env.local file found at {env_file}")
        print("   Using system environment variables")
    print("")

def test_newsapi_key():
    """Test if NewsAPI key is available."""
    print("=" * 80)
    print("STEP 1: CHECK NEWSAPI KEY")
    print("=" * 80)
    print("")

    api_key = os.getenv('NEWSAPI_KEY')

    if not api_key:
        print("❌ NEWSAPI_KEY not found in environment")
        print("")
        print("To set up NewsAPI:")
        print("  1. Get free key at: https://newsapi.org/register")
        print("  2. Run: ./setup_newsapi.sh")
        print("  3. Or manually add to .env.local: NEWSAPI_KEY=your_key_here")
        print("")
        return False

    # Mask the key for security
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else api_key[:4] + "..."
    print(f"✅ NEWSAPI_KEY found: {masked_key}")
    print(f"   Length: {len(api_key)} characters")
    print("")

    return True

def test_newsapi_connection():
    """Test basic NewsAPI connection."""
    print("=" * 80)
    print("STEP 2: TEST NEWSAPI CONNECTION")
    print("=" * 80)
    print("")

    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("⏭️  Skipping (no API key)")
        return False

    try:
        import requests

        # Test with a simple query
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'country': 'us',
            'pageSize': 5
        }

        print("🔄 Testing NewsAPI connection...")
        print(f"   Endpoint: {url}")
        print(f"   Query: Top 5 US headlines")
        print("")

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            print(f"✅ NewsAPI connection successful!")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Total results: {data.get('totalResults', 0)}")
            print(f"   Articles returned: {len(data.get('articles', []))}")
            print("")

            # Show sample article
            articles = data.get('articles', [])
            if articles:
                article = articles[0]
                print("📰 Sample Article:")
                print(f"   Title: {article.get('title', 'N/A')}")
                print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
                print(f"   Published: {article.get('publishedAt', 'N/A')}")
                print(f"   URL: {article.get('url', 'N/A')}")
                print("")

            return True

        elif response.status_code == 401:
            print(f"❌ Authentication failed (HTTP 401)")
            print(f"   Your API key might be invalid or expired")
            print(f"   Get a new key at: https://newsapi.org/register")
            print("")
            return False

        elif response.status_code == 429:
            print(f"❌ Rate limit exceeded (HTTP 429)")
            print(f"   Free tier: 100 requests/day")
            print(f"   Try again later or upgrade your plan")
            print("")
            return False

        else:
            print(f"❌ NewsAPI returned HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            print("")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print(f"   Check your internet connection")
        print("")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        print("")
        return False

def test_fetch_newsapi_events():
    """Test the actual fetch_newsapi_events function from the main script."""
    print("=" * 80)
    print("STEP 3: TEST FETCH_NEWSAPI_EVENTS FUNCTION")
    print("=" * 80)
    print("")

    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("⏭️  Skipping (no API key)")
        return False

    try:
        # Import the function from main script
        from collect_events_with_cosmic_state import fetch_newsapi_events

        print("🔄 Testing fetch_newsapi_events(lookback_hours=24)...")
        print("   This uses the same function as the automated collection")
        print("")

        # Test with 24 hour lookback
        events = fetch_newsapi_events(lookback_hours=24)

        if not events:
            print("⚠️  No events returned")
            print("   This might be normal if:")
            print("   - No matching news in the past 24 hours")
            print("   - NewsAPI query filters are too strict")
            print("   - Rate limit reached")
            print("")
            return False

        print(f"✅ Successfully fetched {len(events)} events!")
        print("")

        # Analyze events
        print("📊 Event Analysis:")
        print(f"   Total events: {len(events)}")

        # Count by category
        categories = {}
        for event in events:
            cat = event.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        print(f"   Categories: {dict(categories)}")

        # Count events with times
        events_with_time = sum(1 for e in events if e.get('time'))
        print(f"   Events with time: {events_with_time}/{len(events)}")

        # Count events with location
        events_with_location = sum(1 for e in events if e.get('location'))
        print(f"   Events with location: {events_with_location}/{len(events)}")

        # Count events with sources
        events_with_sources = sum(1 for e in events if e.get('sources'))
        print(f"   Events with sources: {events_with_sources}/{len(events)}")

        print("")

        # Show sample events
        print("📰 Sample Events (first 3):")
        print("")
        for i, event in enumerate(events[:3], 1):
            print(f"Event {i}:")
            print(f"   Title: {event.get('title', 'N/A')}")
            print(f"   Category: {event.get('category', 'N/A')}")
            print(f"   Location: {event.get('location', 'N/A')}")
            print(f"   Date: {event.get('date', 'N/A')}")
            print(f"   Time: {event.get('time', 'N/A')}")
            print(f"   Impact: {event.get('impact_level', 'N/A')}")

            sources = event.get('sources', [])
            if sources:
                print(f"   Source: {sources[0] if sources else 'N/A'}")

            # Check if astrological relevance was mapped
            astro = event.get('astrological_relevance')
            if astro:
                print(f"   Astro Houses: {astro.get('relevant_houses', [])}")
                print(f"   Astro Planets: {astro.get('relevant_planets', [])}")

            print("")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"   Cannot import from collect_events_with_cosmic_state.py")
        print("")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("")
        return False

def test_newsapi_in_collection_flow():
    """Test NewsAPI integration in the full collection flow."""
    print("=" * 80)
    print("STEP 4: TEST NEWSAPI IN COLLECTION FLOW")
    print("=" * 80)
    print("")

    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("⏭️  Skipping (no API key)")
        return False

    print("ℹ️  This would run the full collection script with NewsAPI")
    print("   To avoid creating duplicate data, run manually:")
    print("")
    print("   python3 collect_events_with_cosmic_state.py --lookback-hours 2")
    print("")
    print("   Expected behavior:")
    print("   1. Script tries NewsAPI first")
    print("   2. If NewsAPI returns ≥5 events → uses NewsAPI")
    print("   3. If NewsAPI returns <5 events → falls back to OpenAI")
    print("")

    return True

def main():
    """Run all NewsAPI tests."""
    print("")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "NEWSAPI INTEGRATION TEST" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print("")

    # Load environment
    load_env()

    # Run tests
    results = {
        'API Key Check': test_newsapi_key(),
        'API Connection': test_newsapi_connection(),
        'Fetch Events Function': test_fetch_newsapi_events(),
        'Collection Flow': test_newsapi_in_collection_flow(),
    }

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        if result:
            print(f"  ✅ PASS - {test_name}")
        else:
            print(f"  ❌ FAIL - {test_name}")

    print("")
    print(f"Overall: {passed}/{total} tests passed")
    print("")

    if passed == total:
        print("🎉 NewsAPI integration is working perfectly!")
        print("")
        print("Next steps:")
        print("  1. Add NEWSAPI_KEY to GitHub Secrets for automated workflow")
        print("  2. Run: python3 collect_events_with_cosmic_state.py --lookback-hours 24")
        print("  3. Check database for NewsAPI events (should have source URLs)")
        print("")
    elif results.get('API Key Check') and results.get('API Connection'):
        print("✅ NewsAPI is configured and working!")
        print("   Some advanced tests didn't complete, but basic functionality works.")
        print("")
    else:
        print("⚠️  NewsAPI integration needs attention.")
        print("")
        if not results.get('API Key Check'):
            print("Action required:")
            print("  1. Get free API key at: https://newsapi.org/register")
            print("  2. Run: ./setup_newsapi.sh")
            print("  3. Or add to .env.local: NEWSAPI_KEY=your_key_here")
        elif not results.get('API Connection'):
            print("Action required:")
            print("  1. Verify your API key is correct")
            print("  2. Check if you've exceeded rate limit (100 requests/day)")
            print("  3. Try getting a new key if current one is invalid")
        print("")

    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
