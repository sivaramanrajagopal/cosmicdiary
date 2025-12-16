#!/usr/bin/env python3
"""
Enhanced Email Summary for Event Collection
Sends detailed summary with mini dashboard after each collection run.
"""

import os
import sys
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, List, Dict

# Load environment variables
SCRIPT_DIR = Path(__file__).parent.resolve()
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_local_path, override=True)
elif env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path, override=False)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '')

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', os.getenv('SUPABASE_KEY', ''))


def fetch_recent_events(hours: int = 2) -> List[Dict]:
    """Fetch events from the last N hours"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []

    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        # Calculate cutoff time
        cutoff_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

        # Fetch recent events
        response = supabase.table('events')\
            .select('id, title, date, category, location, impact_level, description, created_at')\
            .gte('created_at', cutoff_time)\
            .order('created_at', desc=True)\
            .execute()

        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []


def get_impact_color(impact_level: str) -> str:
    """Get color for impact level"""
    colors = {
        'critical': '#dc2626',
        'high': '#f97316',
        'medium': '#fbbf24',
        'low': '#10b981'
    }
    return colors.get(impact_level, '#6b7280')


def get_category_emoji(category: str) -> str:
    """Get emoji for category"""
    emojis = {
        'Natural Disaster': '🌪️',
        'War': '⚔️',
        'Economic': '💰',
        'Political': '🏛️',
        'Technology': '💻',
        'Health': '🏥',
        'Personal': '👤',
        'Other': '📌'
    }
    return emojis.get(category, '📌')


def send_enhanced_summary_email(
    events_detected: int,
    events_stored: int,
    correlations_created: int,
    avg_correlation_score: Optional[float] = None,
    error_message: Optional[str] = None,
    collection_type: str = '2-hour'  # '2-hour' or 'daily'
) -> bool:
    """
    Send enhanced summary email with mini dashboard

    Args:
        events_detected: Number of events detected
        events_stored: Number of events stored
        correlations_created: Number of correlations created
        avg_correlation_score: Average correlation score (optional)
        error_message: Error message if collection failed (optional)
        collection_type: '2-hour' for regular runs, 'daily' for daily summary

    Returns:
        True if email sent successfully, False otherwise
    """
    if not all([EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL]):
        print("⚠️  Email configuration missing. Skipping email notification.")
        return False

    try:
        now = datetime.utcnow()
        collection_time = now.strftime('%Y-%m-%d %H:%M:%S UTC')

        # Fetch recent events
        hours_lookback = 24 if collection_type == 'daily' else 2
        recent_events = fetch_recent_events(hours=hours_lookback)

        # Determine status
        if error_message:
            status = "❌ FAILED"
            status_color = "#dc2626"
            title = "Event Collection Failed"
        else:
            status = "✅ SUCCESS"
            status_color = "#10b981"
            if collection_type == 'daily':
                title = "Daily Summary"
            else:
                title = "Event Collection Summary"

        # Create email
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL

        if collection_type == 'daily':
            msg['Subject'] = f'🌟 Cosmic Diary: Daily Summary - {now.strftime("%B %d, %Y")}'
        else:
            msg['Subject'] = f'🌟 Cosmic Diary: {title} - {collection_time}'

        # Build event cards HTML
        events_html = ""
        if recent_events:
            for event in recent_events[:10]:  # Limit to 10 events
                impact_color = get_impact_color(event.get('impact_level', 'low'))
                category_emoji = get_category_emoji(event.get('category', 'Other'))

                description = event.get('description', '')
                description_preview = description[:150] + '...' if len(description) > 150 else description

                events_html += f"""
                <div style="background: #f9fafb; border-left: 4px solid {impact_color}; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <h4 style="margin: 0; color: #111827; font-size: 16px;">
                            {category_emoji} {event.get('title', 'Untitled Event')}
                        </h4>
                        <span style="background: {impact_color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; text-transform: uppercase;">
                            {event.get('impact_level', 'low')}
                        </span>
                    </div>
                    <div style="color: #6b7280; font-size: 13px; margin-bottom: 8px;">
                        <span>📅 {event.get('date', 'N/A')}</span>
                        <span style="margin: 0 8px;">•</span>
                        <span>📍 {event.get('location', 'Unknown')}</span>
                        <span style="margin: 0 8px;">•</span>
                        <span>🏷️ {event.get('category', 'Other')}</span>
                    </div>
                    {f'<p style="color: #4b5563; font-size: 13px; margin: 0; line-height: 1.5;">{description_preview}</p>' if description_preview else ''}
                </div>
                """
        else:
            events_html = '<p style="text-align: center; color: #9ca3af; padding: 20px;">No events collected in this period.</p>'

        # Create HTML body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f3f4f6;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                .status {{
                    background: {status_color};
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    display: inline-block;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .stats {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .stat-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    margin: 15px 0;
                }}
                .stat-box {{
                    background: #f9fafb;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    border: 1px solid #e5e7eb;
                }}
                .stat-value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #8b5cf6;
                    display: block;
                }}
                .stat-label {{
                    font-size: 12px;
                    color: #6b7280;
                    text-transform: uppercase;
                    margin-top: 5px;
                }}
                .events-section {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .section-title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #111827;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #e5e7eb;
                }}
                .footer {{
                    text-align: center;
                    color: #6b7280;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="margin: 0;">🌟 Cosmic Diary</h1>
                <p style="margin: 10px 0 0 0;">{title}</p>
                <div class="status">{status}</div>
            </div>

            <div class="stats">
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 15px;">
                    {'Daily Summary for ' + now.strftime('%B %d, %Y') if collection_type == 'daily' else 'Collection Time: ' + collection_time}
                </p>

                <div class="stat-grid">
                    <div class="stat-box">
                        <span class="stat-value">{events_detected}</span>
                        <span class="stat-label">Events Detected</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{events_stored}</span>
                        <span class="stat-label">Events Stored</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{correlations_created}</span>
                        <span class="stat-label">Correlations</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{f'{avg_correlation_score:.0f}' if avg_correlation_score else 'N/A'}</span>
                        <span class="stat-label">Avg Score</span>
                    </div>
                </div>
            </div>
        """

        if error_message:
            html_body += f"""
            <div class="events-section" style="background: #fee; border-left: 4px solid #dc2626;">
                <div class="section-title" style="color: #dc2626;">❌ Error Details</div>
                <pre style="white-space: pre-wrap; font-size: 12px; color: #991b1b;">{error_message}</pre>
            </div>
            """

        if recent_events:
            html_body += f"""
            <div class="events-section">
                <div class="section-title">
                    📋 {'Events Collected Today' if collection_type == 'daily' else 'Recently Collected Events'} ({len(recent_events)})
                </div>
                {events_html}
            </div>
            """

        html_body += f"""
            <div class="footer">
                <p>This is an automated notification from Cosmic Diary event collection system.</p>
                <p>Generated at: {collection_time}</p>
                <p style="margin-top: 10px;">
                    <a href="https://cosmicdiary.vercel.app/dashboard" style="color: #8b5cf6; text-decoration: none;">
                        📊 View Dashboard
                    </a>
                    <span style="margin: 0 10px;">•</span>
                    <a href="https://cosmicdiary.vercel.app/events" style="color: #8b5cf6; text-decoration: none;">
                        📅 View All Events
                    </a>
                </p>
            </div>
        </body>
        </html>
        """

        # Create plain text version
        text_body = f"""
Cosmic Diary - {title}
{'=' * 50}

Status: {status}
{'Daily Summary for ' + now.strftime('%B %d, %Y') if collection_type == 'daily' else 'Collection Time: ' + collection_time}

Statistics:
- Events Detected: {events_detected}
- Events Stored: {events_stored}
- Correlations Created: {correlations_created}
- Avg Correlation Score: {f'{avg_correlation_score:.2f}' if avg_correlation_score else 'N/A'}

{'Recent Events (' + str(len(recent_events)) + '):' if recent_events else 'No events collected in this period.'}
"""

        if recent_events:
            for i, event in enumerate(recent_events[:10], 1):
                text_body += f"\n{i}. {event.get('title', 'Untitled')}\n"
                text_body += f"   Date: {event.get('date', 'N/A')}\n"
                text_body += f"   Category: {event.get('category', 'Other')} | Impact: {event.get('impact_level', 'low').upper()}\n"
                text_body += f"   Location: {event.get('location', 'Unknown')}\n"
                if event.get('description'):
                    desc = event['description'][:100] + '...' if len(event['description']) > 100 else event['description']
                    text_body += f"   {desc}\n"

        if error_message:
            text_body += f"\nError:\n{error_message}\n"

        text_body += f"\n\nView Dashboard: https://cosmicdiary.vercel.app/dashboard"
        text_body += f"\nView Events: https://cosmicdiary.vercel.app/events"
        text_body += f"\n\nGenerated at: {collection_time}\n"

        # Attach both versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')

        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Enhanced summary email sent to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Error sending enhanced summary email: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function - can be called from GitHub Actions"""
    import sys

    # Parse arguments (if provided)
    events_detected = int(os.getenv('EVENTS_DETECTED', '0'))
    events_stored = int(os.getenv('EVENTS_STORED', '0'))
    correlations_created = int(os.getenv('CORRELATIONS_CREATED', '0'))
    avg_score = os.getenv('AVG_CORRELATION_SCORE')
    avg_correlation_score = float(avg_score) if avg_score else None

    error_message = os.getenv('ERROR_MESSAGE', '')
    collection_type = os.getenv('COLLECTION_TYPE', '2-hour')  # '2-hour' or 'daily'

    # Send email
    success = send_enhanced_summary_email(
        events_detected=events_detected,
        events_stored=events_stored,
        correlations_created=correlations_created,
        avg_correlation_score=avg_correlation_score,
        error_message=error_message if error_message else None,
        collection_type=collection_type
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
