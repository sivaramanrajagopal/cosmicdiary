"""
Test Supabase Connection
Simple script to verify Supabase connection and database access
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '') or os.getenv('SUPABASE_KEY', '')

def test_connection():
    """Test Supabase connection"""
    print("🔌 Testing Supabase connection...")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set")
        return False
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test query - try to count events
        try:
            response = supabase.table('events').select('id', count='exact').limit(1).execute()
            print(f"✅ Connection successful!")
            print(f"📊 Events table accessible")
            
            # Try to count records
            count_response = supabase.table('events').select('*', count='exact').execute()
            event_count = count_response.count if hasattr(count_response, 'count') else 'unknown'
            print(f"📈 Total events in database: {event_count}")
        
        except Exception as e:
            print(f"⚠️ Warning: Could not query events table: {e}")
            print("   This might be normal if the table doesn't exist yet.")
            print("   Run database_schema.sql to create the tables.")
        
        # Test planetary_data table
        try:
            response = supabase.table('planetary_data').select('id', count='exact').limit(1).execute()
            print(f"✅ Planetary_data table accessible")
            
            count_response = supabase.table('planetary_data').select('*', count='exact').execute()
            pd_count = count_response.count if hasattr(count_response, 'count') else 'unknown'
            print(f"📈 Total planetary_data records: {pd_count}")
        
        except Exception as e:
            print(f"⚠️ Warning: Could not query planetary_data table: {e}")
            print("   This might be normal if the table doesn't exist yet.")
        
        return True
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == '__main__':
    success = test_connection()
    exit(0 if success else 1)
