#!/usr/bin/env python3
"""
On-Demand Event Collection & Analysis with Email Notification
- Collects events using NewsAPI + OpenAI (hybrid approach)
- Calculates astrological charts and correlations
- Creates events in database with full astrological metadata
- Sends email notification

This script now uses the main collection script's logic for consistency.
"""

import os
import sys
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from supabase import create_client, Client
from typing import List, Dict, Optional, Tuple, Any

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()

# Add to path for imports
sys.path.insert(0, str(SCRIPT_DIR))

# Load .env files from script directory
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

# Import from main collection script for consistency and feature parity
try:
    from collect_events_with_cosmic_state import (
        capture_cosmic_snapshot,
        fetch_newsapi_events,
        detect_events_openai,
        store_event_with_chart,
        correlate_and_store
    )
    MAIN_SCRIPT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Could not import from main collection script: {e}")
    print("   Falling back to legacy on-demand logic")
    MAIN_SCRIPT_AVAILABLE = False

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

def fetch_events_for_date(target_date: date) -> Tuple[List[Dict], str]:
    """
    Fetch events for a specific date using hybrid approach (NewsAPI + OpenAI).
    Uses the main collection script's superior logic.

    Returns:
        Tuple of (events_list, source_info_string)
    """
    today = date.today()
    days_ago = (today - target_date).days

    # Check for future dates
    if target_date > today:
        print(f"  ⚠️  Warning: Target date is in the future. Cannot fetch real events.")
        print(f"     Consider using a past date (e.g., {today - timedelta(days=7)})")
        return [], "Future date - no events available"

    date_str = target_date.strftime('%B %d, %Y')
    print(f"  📅 Target date: {date_str} ({days_ago} days ago)")
    print("")

    if not MAIN_SCRIPT_AVAILABLE:
        print("  ⚠️  Main script functions not available - cannot fetch events")
        return [], "Main script import failed"

    # Calculate lookback hours from target date to now
    # For on-demand jobs, we want events around the target date (±1-2 days)
    lookback_hours = min(days_ago * 24 + 48, 7 * 24)  # Up to 7 days max

    print(f"  🔍 Using lookback window: {lookback_hours} hours")
    print("")

    # Try NewsAPI first (if available and date is recent enough)
    newsapi_key = os.getenv('NEWSAPI_KEY')
    events = []
    source_info = ""

    if newsapi_key and days_ago <= 30:  # NewsAPI free tier: last 30 days
        print("  🔄 Attempting NewsAPI for real-time news...")
        try:
            newsapi_events = fetch_newsapi_events(lookback_hours=lookback_hours)
            if len(newsapi_events) >= 5:
                print(f"  ✅ Using {len(newsapi_events)} events from NewsAPI")
                events = newsapi_events
                source_info = f"NewsAPI ({len(events)} real-time articles)"
            else:
                print(f"  ⚠️  NewsAPI returned only {len(newsapi_events)} events, trying OpenAI...")
        except Exception as e:
            print(f"  ⚠️  NewsAPI failed: {e}")

    # Fall back to OpenAI if NewsAPI didn't work or not available
    if not events:
        print("  🤖 Using OpenAI for event detection...")
        try:
            openai_events = detect_events_openai(lookback_hours=lookback_hours)
            events = openai_events
            source_info = f"OpenAI ({len(events)} events detected)"
            print(f"  ✅ OpenAI returned {len(events)} events")
        except Exception as e:
            print(f"  ❌ OpenAI failed: {e}")
            import traceback
            traceback.print_exc()
            return [], f"Error: {str(e)}"

    print("")
    return events, source_info

def create_event_with_analysis(
    event_data: Dict,
    target_date: date,
    snapshot_id: Optional[int] = None,
    snapshot_chart: Optional[Dict] = None
) -> Tuple[Optional[int], Optional[Dict], bool]:
    """
    Create event in database with full astrological analysis.
    Uses the main script's store_event_with_chart function.

    Returns:
        Tuple of (event_id, event_chart, correlation_created)
    """
    if not MAIN_SCRIPT_AVAILABLE:
        print("  ⚠️  Main script not available, using legacy create")
        # Fallback to simple insert
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

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            result = supabase.table('events').insert(event_record).execute()

            if result.data:
                return result.data[0].get('id'), None, False
            return None, None, False

        except Exception as e:
            print(f"  ❌ Error creating event: {e}")
            return None, None, False

    # Use main script's superior logic
    try:
        # Ensure event has date field (store_event_with_chart expects it in the event dict)
        if 'date' not in event_data:
            event_data['date'] = target_date.isoformat()

        # Store event with chart calculation
        event_id, event_chart = store_event_with_chart(event_data)

        if not event_id:
            return None, None, False

        # Create correlation with snapshot if available
        correlation_created = False
        if snapshot_id and snapshot_chart and event_chart:
            try:
                correlation_created = correlate_and_store(
                    event_id=event_id,
                    event_chart=event_chart,
                    snapshot_id=snapshot_id,
                    snapshot_chart=snapshot_chart
                )
            except Exception as corr_error:
                print(f"  ⚠️  Could not create correlation: {corr_error}")

        return event_id, event_chart, correlation_created

    except Exception as e:
        print(f"  ❌ Error in create_event_with_analysis: {e}")
        import traceback
        traceback.print_exc()
        return None, None, False

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
    """Main function - now uses main collection script's logic for consistency"""
    print("📅 Starting On-Demand Event Collection & Analysis with Email Notification")
    print("=" * 70)
    print("✨ Using enhanced collection logic (NewsAPI + OpenAI + Charts + Correlations)")
    print("")

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

    # Validate configuration
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)

    if not MAIN_SCRIPT_AVAILABLE:
        print("❌ Error: Could not import from main collection script")
        print("   Make sure collect_events_with_cosmic_state.py is in the same directory")
        sys.exit(1)

    # Step 1: Capture cosmic snapshot
    print("STEP 1: CAPTURING COSMIC SNAPSHOT")
    print("-" * 70)
    try:
        snapshot_id, snapshot_chart = capture_cosmic_snapshot()
        print(f"✅ Snapshot captured (ID: {snapshot_id})")
        print("")
    except Exception as e:
        print(f"⚠️  Could not capture snapshot: {e}")
        snapshot_id, snapshot_chart = None, None
        print("")

    # Step 2: Fetch events
    print("STEP 2: FETCHING EVENTS")
    print("-" * 70)
    events, source_info = fetch_events_for_date(target_date)

    if not events:
        print("⚠️  No events fetched")
        details = f"No events were returned. Source: {source_info}"
        success = False
        events_created = []
        correlations_count = 0
    else:
        print(f"✅ Fetched {len(events)} events from {source_info}")
        print("")

        # Step 3: Create events with charts and correlations
        print("STEP 3: CREATING EVENTS WITH ASTROLOGICAL ANALYSIS")
        print("-" * 70)
        events_created = []
        correlations_count = 0
        details = ""

        for i, event_data in enumerate(events, 1):
            title = event_data.get('title', 'Unknown')[:60]
            print(f"  [{i}/{len(events)}] Processing: {title}")

            event_id, event_chart, correlation_created = create_event_with_analysis(
                event_data,
                target_date,
                snapshot_id,
                snapshot_chart
            )

            if event_id:
                events_created.append({
                    **event_data,
                    'id': event_id,
                    'db_id': event_id,
                    'has_chart': event_chart is not None,
                    'has_correlation': correlation_created
                })

                status_parts = [f"ID: {event_id}"]
                if event_chart:
                    status_parts.append("Chart: ✓")
                if correlation_created:
                    status_parts.append("Correlation: ✓")
                    correlations_count += 1

                details += f"✅ Created: {event_data.get('title')} ({', '.join(status_parts)})\n"
                print(f"      ✅ {', '.join(status_parts)}")
            else:
                details += f"❌ Failed: {event_data.get('title')}\n"
                print(f"      ❌ Failed to create")

        print("")
        print(f"✅ Created {len(events_created)}/{len(events)} events in database")
        print(f"   • Events with charts: {sum(1 for e in events_created if e.get('has_chart'))}")
        print(f"   • Correlations created: {correlations_count}")
        print("")

        success = len(events_created) > 0
        details += f"\n📊 Summary:\n"
        details += f"   • Total events: {len(events_created)}/{len(events)}\n"
        details += f"   • Source: {source_info}\n"
        details += f"   • Charts calculated: {sum(1 for e in events_created if e.get('has_chart'))}\n"
        details += f"   • Correlations: {correlations_count}\n"
        if snapshot_id:
            details += f"   • Snapshot ID: {snapshot_id}\n"

    # Step 4: Send email notification
    print("STEP 4: SENDING EMAIL NOTIFICATION")
    print("-" * 70)

    subject = f"📅 Cosmic Diary - Event Collection {'Success' if success else 'Completed'} ({target_date.isoformat()})"
    body = format_email_body(success, target_date, events_created, details)

    email_sent = send_email_notification(subject, body, success)
    print("")

    # Final status
    print("=" * 70)
    print("FINAL STATUS")
    print("=" * 70)
    if success:
        print(f"✅ Job completed successfully!")
        print(f"   • Events created: {len(events_created)}")
        print(f"   • Source: {source_info}")
        print(f"   • Charts: {sum(1 for e in events_created if e.get('has_chart'))}")
        print(f"   • Correlations: {correlations_count}")
    else:
        print("⚠️  Job completed with no events created.")
        print(f"   • Reason: {details}")

    if email_sent:
        print(f"✅ Email notification sent to {RECIPIENT_EMAIL}")
    else:
        print("⚠️  Email notification not sent (check configuration)")

    print("=" * 70)
    print("")

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

