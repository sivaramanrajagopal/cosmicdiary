#!/usr/bin/env python3
"""
Diagnostic script to test GitHub Actions environment.
Run this in GitHub Actions to diagnose why events are not being collected.
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check all required environment variables."""
    print("=" * 80)
    print("ENVIRONMENT VARIABLE CHECK")
    print("=" * 80)
    print("")

    required_vars = {
        'OPENAI_API_KEY': 'Required for event detection via OpenAI',
        'SUPABASE_URL': 'Required for database connection',
        'SUPABASE_SERVICE_ROLE_KEY': 'Required for database writes',
    }

    optional_vars = {
        'NEWSAPI_KEY': 'Optional - enables real-time news fetching',
        'EVENT_LOOKBACK_HOURS': 'Optional - defaults to 2 hours',
    }

    all_good = True

    print("Required Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show first 10 chars only for security
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {var}: SET ({masked})")
            print(f"      {description}")
        else:
            print(f"  ❌ {var}: NOT SET")
            print(f"      {description}")
            all_good = False

    print("")
    print("Optional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {var}: SET ({masked})")
        else:
            print(f"  ℹ️  {var}: NOT SET (using default)")
        print(f"      {description}")

    print("")
    return all_good

def check_files():
    """Check that required files exist."""
    print("=" * 80)
    print("FILE SYSTEM CHECK")
    print("=" * 80)
    print("")

    required_files = [
        'collect_events_with_cosmic_state.py',
        'prompts/event_detection_prompt.py',
        'correlation_analyzer.py',
        'astro_calculations.py',
    ]

    all_good = True

    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} NOT FOUND")
            all_good = False

    print("")
    return all_good

def check_python_packages():
    """Check that required Python packages are installed."""
    print("=" * 80)
    print("PYTHON PACKAGE CHECK")
    print("=" * 80)
    print("")

    packages = {
        'openai': 'OpenAI API client',
        'supabase': 'Supabase database client',
        'swisseph': 'Swiss Ephemeris for astrological calculations',
        'pytz': 'Timezone support',
        'requests': 'HTTP requests for NewsAPI',
    }

    all_good = True

    for package, description in packages.items():
        try:
            __import__(package)
            # Get version if possible
            try:
                mod = __import__(package)
                version = getattr(mod, '__version__', 'unknown')
                print(f"  ✅ {package} (v{version})")
            except:
                print(f"  ✅ {package}")
            print(f"      {description}")
        except ImportError:
            print(f"  ❌ {package} NOT INSTALLED")
            print(f"      {description}")
            all_good = False

    print("")
    return all_good

def test_openai_connection():
    """Test OpenAI API connection."""
    print("=" * 80)
    print("OPENAI API CONNECTION TEST")
    print("=" * 80)
    print("")

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("  ❌ OPENAI_API_KEY not set - skipping connection test")
        print("")
        return False

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        print("  🔄 Testing OpenAI API connection...")

        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API test successful' if you can read this."}],
            max_tokens=10
        )

        if response.choices and len(response.choices) > 0:
            print(f"  ✅ OpenAI API connection successful")
            print(f"      Response: {response.choices[0].message.content}")
            print("")
            return True
        else:
            print(f"  ❌ OpenAI API returned empty response")
            print("")
            return False

    except Exception as e:
        print(f"  ❌ OpenAI API connection failed: {e}")
        print(f"      Error type: {type(e).__name__}")
        print("")
        return False

def test_supabase_connection():
    """Test Supabase database connection."""
    print("=" * 80)
    print("SUPABASE CONNECTION TEST")
    print("=" * 80)
    print("")

    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not url or not key:
        print("  ❌ SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set")
        print("")
        return False

    try:
        from supabase import create_client

        print(f"  🔄 Connecting to: {url}")
        supabase = create_client(url, key)

        # Test query
        result = supabase.table('events').select('id').limit(1).execute()

        print(f"  ✅ Supabase connection successful")
        print(f"      Database is accessible")
        print("")
        return True

    except Exception as e:
        print(f"  ❌ Supabase connection failed: {e}")
        print(f"      Error type: {type(e).__name__}")
        print("")
        return False

def main():
    """Run all diagnostic checks."""
    print("")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "GITHUB ACTIONS DIAGNOSTIC TOOL" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    print("")
    print("This script checks your GitHub Actions environment for common issues.")
    print("")

    results = {
        'Environment Variables': check_environment(),
        'Required Files': check_files(),
        'Python Packages': check_python_packages(),
        'OpenAI API': test_openai_connection(),
        'Supabase Database': test_supabase_connection(),
    }

    # Summary
    print("=" * 80)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 80)
    print("")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {check}")

    print("")
    print(f"Overall: {passed}/{total} checks passed")
    print("")

    if passed == total:
        print("🎉 All checks passed! Your environment is properly configured.")
        print("")
        print("If you're still seeing zeros in GitHub Actions output:")
        print("  1. Check the workflow logs for actual errors during execution")
        print("  2. Verify the script runs to completion (look for 'completed successfully')")
        print("  3. Download the log artifact and search for 'EVENTS_DETECTED='")
        print("")
        sys.exit(0)
    else:
        print("⚠️  Some checks failed. Fix the issues above and try again.")
        print("")
        print("Common fixes:")
        print("  • Missing environment variables → Add them in GitHub Secrets")
        print("  • Missing files → Commit and push all required files")
        print("  • Missing packages → Check workflow 'Install dependencies' step")
        print("  • API connection failures → Verify API keys are correct and active")
        print("")
        sys.exit(1)

if __name__ == "__main__":
    main()
