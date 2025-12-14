#!/usr/bin/env python3
"""
Diagnostic Script for Event Collection System
Tests all components to ensure everything is configured correctly
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
SCRIPT_DIR = Path(__file__).parent.resolve()
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

def print_header(text):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def check_env_var(var_name, required=True, mask=True):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value:
        display_value = f"{value[:10]}...{value[-4:]}" if mask and len(value) > 14 else value[:50]
        print(f"  ✅ {var_name}: {display_value}")
        return True
    else:
        status = "❌ REQUIRED" if required else "⚠️  OPTIONAL"
        print(f"  {status} {var_name}: Not set")
        return False if required else True

def check_openai():
    """Test OpenAI API connection"""
    print_header("TESTING OPENAI API")

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("  ❌ OPENAI_API_KEY not set")
        return False

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print(f"  ✅ OpenAI client initialized")

        # Test with a simple completion
        print(f"  🧪 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )

        if response.choices:
            print(f"  ✅ API call successful: {response.choices[0].message.content}")
            return True
        else:
            print(f"  ❌ API call failed: No response")
            return False

    except ImportError:
        print(f"  ❌ openai package not installed. Run: pip install openai")
        return False
    except Exception as e:
        print(f"  ❌ OpenAI API error: {e}")
        return False

def check_supabase():
    """Test Supabase connection"""
    print_header("TESTING SUPABASE DATABASE")

    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY')

    if not url or not key:
        print("  ❌ SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set")
        return False

    try:
        from supabase import create_client
        client = create_client(url, key)
        print(f"  ✅ Supabase client initialized")

        # Test connection by checking events table
        print(f"  🧪 Testing database query...")
        result = client.table('events').select('id').limit(1).execute()
        print(f"  ✅ Database connection successful")
        return True

    except ImportError:
        print(f"  ❌ supabase package not installed. Run: pip install supabase")
        return False
    except Exception as e:
        print(f"  ❌ Supabase error: {e}")
        return False

def check_python_packages():
    """Check if all required packages are installed"""
    print_header("CHECKING PYTHON PACKAGES")

    required_packages = {
        'openai': 'OpenAI API client',
        'supabase': 'Supabase database client',
        'dotenv': 'Environment variable loader',
        'swisseph': 'Swiss Ephemeris (pyswisseph)',
        'pytz': 'Timezone library',
        'timezonefinder': 'Timezone finder',
        'geopy': 'Geocoding library',
        'requests': 'HTTP library'
    }

    all_installed = True
    for package, description in required_packages.items():
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'swisseph':
                __import__('swisseph')
            else:
                __import__(package)
            print(f"  ✅ {package:20s} - {description}")
        except ImportError:
            print(f"  ❌ {package:20s} - NOT INSTALLED ({description})")
            all_installed = False

    return all_installed

def check_files():
    """Check if all required files exist"""
    print_header("CHECKING REQUIRED FILES")

    required_files = [
        'collect_events_with_cosmic_state.py',
        'astro_calculations.py',
        'aspect_calculator.py',
        'correlation_analyzer.py',
        'prompts/event_detection_prompt.py',
        'prompts/__init__.py'
    ]

    all_exist = True
    for file_path in required_files:
        full_path = SCRIPT_DIR / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - NOT FOUND")
            all_exist = False

    return all_exist

def check_prompt_import():
    """Test if prompt system can be imported"""
    print_header("TESTING PROMPT SYSTEM")

    try:
        sys.path.append(str(SCRIPT_DIR))
        from prompts.event_detection_prompt import (
            SYSTEM_PROMPT,
            generate_user_prompt,
            validate_event_response,
            calculate_research_score
        )
        print(f"  ✅ Prompt system imports successfully")
        print(f"  ✅ SYSTEM_PROMPT length: {len(SYSTEM_PROMPT)} characters")

        # Test generate_user_prompt
        from prompts.event_detection_prompt import get_time_window
        time_window = get_time_window(lookback_hours=2)
        user_prompt = generate_user_prompt(time_window)
        print(f"  ✅ User prompt generation works ({len(user_prompt)} characters)")

        return True
    except ImportError as e:
        print(f"  ❌ Failed to import prompt system: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing prompt system: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍" * 40)
    print("EVENT COLLECTION SYSTEM DIAGNOSTIC TEST")
    print("🔍" * 40)

    # Check environment variables
    print_header("CHECKING ENVIRONMENT VARIABLES")
    env_checks = {
        'OPENAI_API_KEY': check_env_var('OPENAI_API_KEY', required=True, mask=True),
        'SUPABASE_URL': check_env_var('SUPABASE_URL', required=True, mask=False),
        'SUPABASE_SERVICE_ROLE_KEY': check_env_var('SUPABASE_SERVICE_ROLE_KEY', required=True, mask=True),
        'EVENT_LOOKBACK_HOURS': check_env_var('EVENT_LOOKBACK_HOURS', required=False, mask=False),
    }

    # Run all checks
    checks = {
        'Python Packages': check_python_packages(),
        'Required Files': check_files(),
        'Prompt System': check_prompt_import(),
        'OpenAI API': check_openai(),
        'Supabase DB': check_supabase(),
    }

    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status:12s} - {check_name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! System is ready for event collection.")
        print("\nNext steps:")
        print("  1. Run: python collect_events_with_cosmic_state.py --lookback-hours 12")
        print("  2. Or trigger GitHub Actions manually")
        print("  3. Check FIXES_SUMMARY.md for detailed documentation")
    else:
        print("⚠️  SOME CHECKS FAILED! Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install missing packages: pip install openai supabase python-dotenv pyswisseph pytz timezonefinder geopy requests")
        print("  - Set environment variables in .env.local file")
        print("  - Check GitHub Secrets for OPENAI_API_KEY and SUPABASE credentials")
    print("=" * 80 + "\n")

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
