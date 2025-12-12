#!/usr/bin/env python3
"""
On-Demand Event Collection & Analysis with Email Notification
- Collects events using OpenAI
- Creates events in database
- Triggers automatic analysis (house mapping, aspects, correlations)
- Sends email notification
"""

import os
import sys
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from openai import OpenAI
from supabase import create_client, Client
from typing import List, Dict, Optional

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()

# Load .env files from script directory
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '') or os.getenv('SUPABASE_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:8000')
NEXTJS_API_URL = os.getenv('NEXTJS_API_URL', 'http://localhost:3002')

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', EMAIL_USER)

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client"""
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)

def fetch_events_via_openai(client: OpenAI, target_date: date) -> List[Dict]:
    """Fetch significant world events using OpenAI"""
    try:
        date_str = target_date.strftime('%B %d, %Y')
        today = date.today()
        
        # Adjust prompt based on whether date is in past, present, or future
        today = date.today()
        days_ago = (today - target_date).days
        
        if target_date > today:
            # Future date - can't have real events
            print(f"  ⚠️  Warning: Target date is in the future. OpenAI cannot provide real events.")
            print(f"     Consider using a past date (e.g., {today - timedelta(days=7)})")
            return []
        elif days_ago == 0:
            date_context = f"{date_str} (today)"
        elif days_ago <= 7:
            date_context = f"{date_str} (recent - {days_ago} days ago)"
        else:
            date_context = f"{date_str} (historical date - {days_ago} days ago)"
        
        prompt = f"""You are an expert at finding significant world events. List 3-5 significant world events that occurred on or around {date_context}.

For each event, provide:
1. A clear, factual title
2. A 2-3 sentence description
3. Category (e.g., Natural Disaster, Political, Economic, Technology, Health, Social, War, etc.)
4. Location (City, Country format)
5. Impact level (low, medium, high, or critical)
6. Relevant tags (2-4 keywords)

Format as a JSON array with this EXACT structure:
[
  {{
    "title": "Event Title",
    "description": "Detailed description of the event",
    "category": "Category Name",
    "location": "City, Country",
    "impact_level": "medium",
    "tags": ["tag1", "tag2"]
  }}
]

IMPORTANT REQUIREMENTS:
- If you cannot find events for the exact date, include events from within 1-2 days before or after
- Include events from any part of the world
- Be factual and objective
- Always return a valid JSON array (even if it contains just 1-2 events)
- Do not return an empty array unless absolutely no events can be found

Return ONLY the JSON array, no markdown, no explanations."""

        print(f"  📝 Requesting events for {date_str}...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides factual information about world events. Always respond with valid JSON only, no markdown, no explanation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"} if target_date > today else None
        )
        
        content = response.choices[0].message.content.strip()
        print(f"  📥 Received response from OpenAI ({len(content)} characters)")
        
        # Debug: Show first 200 chars of response
        if len(content) < 200:
            print(f"  🔍 Full response: {repr(content)}")
        else:
            print(f"  🔍 Response preview: {content[:200]}...")
        
        # Remove markdown code blocks if present
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        # If content is empty or just brackets, warn
        if not content or content == '[]' or content == '{}':
            print(f"  ⚠️  OpenAI returned empty response. This might mean:")
            print(f"     - The date is too recent/future (OpenAI knowledge cutoff)")
            print(f"     - No significant events found for this date")
            print(f"     - API returned empty result")
            return []
        
        # Try to parse as JSON
        try:
            # Handle case where OpenAI might wrap in an object
            parsed = json.loads(content)
            
            # If it's an object, look for common keys
            if isinstance(parsed, dict):
                # Check for common keys that might contain the array
                if 'events' in parsed:
                    events = parsed['events']
                elif 'data' in parsed:
                    events = parsed['data']
                elif 'results' in parsed:
                    events = parsed['results']
                else:
                    # If it's a single event object, wrap it in array
                    if 'title' in parsed:
                        events = [parsed]
                    else:
                        print(f"  ⚠️  Response is an object but no recognizable structure: {list(parsed.keys())}")
                        print(f"  📄 Content preview: {content[:200]}...")
                        events = []
            elif isinstance(parsed, list):
                events = parsed
            else:
                print(f"  ⚠️  Unexpected response type: {type(parsed)}")
                events = []
            
            print(f"  ✅ Parsed {len(events)} events from response")
            return events if isinstance(events, list) else []
            
        except json.JSONDecodeError as je:
            print(f"  ❌ JSON parsing error: {je}")
            print(f"  📄 Content received: {content[:500]}")
            return []
    
    except Exception as e:
        print(f"  ❌ Error fetching events from OpenAI: {e}")
        print(f"  🔍 Error type: {type(e).__name__}")
        import traceback
        print(f"  📋 Traceback: {traceback.format_exc()}")
        return []

def create_event_in_db(supabase: Client, event_data: Dict, target_date: date) -> Optional[Dict]:
    """Create event in Supabase database"""
    try:
        event_record = {
            'date': target_date.isoformat(),
            'title': event_data.get('title', ''),
            'description': event_data.get('description', ''),
            'category': event_data.get('category', ''),
            'location': event_data.get('location', ''),
            'impact_level': event_data.get('impact_level', 'medium'),
            'event_type': 'world',
            'tags': event_data.get('tags', [])
        }
        
        result = supabase.table('events').insert(event_record).execute()
        
        if result.data:
            return result.data[0]
        return None
    
    except Exception as e:
        print(f"❌ Error creating event '{event_data.get('title', 'Unknown')}': {e}")
        return None

def trigger_analysis_for_event(event_id: int) -> bool:
    """Trigger analysis for a specific event via Next.js API"""
    try:
        # The analysis is automatically triggered when an event is created
        # via the Next.js API endpoint, but we can manually trigger recalculation
        url = f"{NEXTJS_API_URL}/api/events/recalculate-correlations"
        
        # This endpoint recalculates for all events, but it runs in background
        # For now, we'll just ensure the event exists - analysis should happen automatically
        response = requests.post(url, timeout=30)
        
        if response.status_code in [200, 201]:
            return True
        else:
            # It's okay if this fails - analysis will happen when event is accessed via API
            return False
    except Exception as e:
        print(f"⚠️  Could not trigger analysis endpoint: {e}")
        # Not critical - analysis happens automatically on event creation via API
        return False

def send_email_notification(subject: str, body: str, success: bool = True):
    """Send email notification"""
    if not EMAIL_USER or not EMAIL_PASSWORD or not RECIPIENT_EMAIL:
        print("⚠️  Email credentials not configured. Skipping email notification.")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        
        print(f"✅ Email notification sent to {RECIPIENT_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def format_email_body(success: bool, target_date: date, events_created: List[Dict], details: str):
    """Format HTML email body"""
    status_icon = "✅" if success else "❌"
    status_color = "#22c55e" if success else "#ef4444"
    status_text = "SUCCESS" if success else "FAILED"
    
    events_list = ""
    if events_created:
        for i, event in enumerate(events_created, 1):
            events_list += f"""
            <div style="background: #f3f4f6; padding: 12px; margin: 8px 0; border-radius: 5px; border-left: 4px solid #667eea;">
                <strong>{i}. {event.get('title', 'Unknown Event')}</strong><br>
                <span style="color: #6b7280; font-size: 0.9em;">
                    Category: {event.get('category', 'N/A')} | 
                    Impact: {event.get('impact_level', 'medium')} | 
                    Location: {event.get('location', 'N/A')}
                </span>
            </div>
            """
    else:
        events_list = "<p style='color: #ef4444;'>No events were created.</p>"
    
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 700px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 20px; border-radius: 0 0 10px 10px; }}
            .status {{ background: {status_color}; color: white; padding: 10px 15px; 
                      border-radius: 5px; display: inline-block; margin: 10px 0; }}
            .details {{ background: white; padding: 15px; border-radius: 5px; 
                       margin: 15px 0; border-left: 4px solid {status_color}; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; 
                      font-size: 12px; }}
            .event-count {{ background: #dbeafe; color: #1e40af; padding: 8px 12px; 
                           border-radius: 5px; display: inline-block; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📅 Cosmic Diary - Event Collection Report</h1>
            </div>
            <div class="content">
                <div class="status">
                    {status_icon} <strong>{status_text}</strong>
                </div>
                
                <h2>Job Execution Summary</h2>
                <div class="details">
                    <p><strong>Target Date:</strong> {target_date.isoformat()}</p>
                    <p><strong>Execution Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                    <p><strong>Status:</strong> {status_text}</p>
                    <div class="event-count">
                        <strong>{len(events_created)} Events Created</strong>
                    </div>
                </div>
                
                <h3>Events Created:</h3>
                <div class="details">
                    {events_list if events_list else '<p>No events were created.</p>'}
                </div>
                
                <h3>Details:</h3>
                <div class="details">
                    <pre style="white-space: pre-wrap; font-family: monospace; font-size: 0.9em;">{details}</pre>
                </div>
                
                <div style="background: #e0e7ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <h4 style="margin-top: 0;">✨ Automatic Analysis</h4>
                    <p style="margin-bottom: 0;">
                        Each event will automatically have:
                        <ul style="margin-top: 5px;">
                            <li>House mapping calculated</li>
                            <li>Planetary aspects determined</li>
                            <li>Planetary correlations analyzed</li>
                        </ul>
                    </p>
                </div>
                
                <div class="footer">
                    <p>This is an automated notification from Cosmic Diary</p>
                    <p>System generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_body

def main():
    """Main function"""
    print("📅 Starting On-Demand Event Collection & Analysis with Email Notification")
    print("=" * 70)
    
    # Determine target date
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"❌ Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        # Default to yesterday (more likely to have events)
        target_date = date.today() - timedelta(days=1)
    
    print(f"📅 Target date: {target_date.isoformat()}")
    print(f"📧 Notification will be sent to: {RECIPIENT_EMAIL or 'Not configured'}")
    print("")
    
    # Initialize
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Fetch events via OpenAI
    print("🤖 Fetching events from OpenAI...")
    openai_client = get_openai_client()
    
    if not openai_client:
        print("❌ Error: OPENAI_API_KEY not set. Cannot fetch events.")
        print("   Please set OPENAI_API_KEY in .env.local")
        sys.exit(1)
    
    print(f"   Using OpenAI API key (length: {len(OPENAI_API_KEY)})")
    events = fetch_events_via_openai(openai_client, target_date)
    
    if not events:
        print("⚠️  No events fetched from OpenAI")
        details = "No events were returned from OpenAI API."
        success = False
        events_created = []
    else:
        print(f"✅ Fetched {len(events)} events from OpenAI")
        print("")
        
        # Create events in database
        print("💾 Creating events in database...")
        events_created = []
        details = ""
        
        for i, event_data in enumerate(events, 1):
            print(f"  [{i}/{len(events)}] Creating: {event_data.get('title', 'Unknown')[:50]}")
            
            created_event = create_event_in_db(supabase, event_data, target_date)
            
            if created_event:
                events_created.append({
                    **event_data,
                    'id': created_event.get('id'),
                    'db_id': created_event.get('id')
                })
                details += f"✅ Created: {event_data.get('title')} (ID: {created_event.get('id')})\n"
            else:
                details += f"❌ Failed: {event_data.get('title')}\n"
        
        print("")
        print(f"✅ Created {len(events_created)}/{len(events)} events in database")
        
        # Trigger analysis (optional - happens automatically via API)
        if events_created:
            print("")
            print("🔮 Analysis will be automatically triggered when events are accessed via API")
            print("   (House mapping, aspects, and correlations will be calculated)")
        
        success = len(events_created) > 0
        details += f"\nTotal: {len(events_created)}/{len(events)} events created successfully."
    
    # Send email notification
    print("")
    print("📧 Sending email notification...")
    
    subject = f"📅 Cosmic Diary - Event Collection {'Success' if success else 'Completed'}"
    body = format_email_body(success, target_date, events_created, details)
    
    email_sent = send_email_notification(subject, body, success)
    
    # Final status
    print("")
    if success:
        print(f"✅ Job completed successfully! Created {len(events_created)} events.")
    else:
        print("⚠️  Job completed with no events created.")
    
    if email_sent:
        print("✅ Email notification sent")
    else:
        print("⚠️  Email notification not sent (check configuration)")
    
    print("")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

