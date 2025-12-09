"""
Email Reports for Cosmic Diary
- Daily Summary: End of day summary of events
- Weekly Analysis: Weekly astrological analysis report
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import requests
from typing import List, Dict
from supabase import create_client, Client

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use environment variables directly

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '')

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')  # Use service_role key for server-side

# Initialize Supabase client if configured
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_events_from_api(date_str: str = None) -> List[Dict]:
    """Fetch events from Supabase (or fallback to API/JSON)"""
    # Try Supabase first
    if supabase:
        try:
            query = supabase.table('events').select('*')
            if date_str:
                query = query.eq('date', date_str)
            
            response = query.execute()
            if response.data:
                return response.data
        except Exception as e:
            print(f"⚠️ Error fetching from Supabase: {e}")
    
    # Fallback: Try Next.js API
    api_url = os.getenv('NEXTJS_API_URL', 'http://localhost:3000')
    
    try:
        url = f"{api_url}/api/events"
        if date_str:
            url += f"?date={date_str}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            events = response.json()
            if date_str and isinstance(events, list):
                events = [e for e in events if e.get('date') == date_str]
            return events if isinstance(events, list) else []
    except Exception as e:
        print(f"⚠️ Could not fetch from API: {e}")
    
    # Fallback: Read from exported events JSON
    if os.path.exists('exported_events.json'):
        try:
            with open('exported_events.json', 'r', encoding='utf-8') as f:
                events = json.load(f)
                if date_str:
                    return [e for e in events if e.get('date') == date_str]
                return events if isinstance(events, list) else []
        except Exception as e:
            print(f"⚠️ Error reading exported_events.json: {e}")
    
    return []

def get_planetary_data_from_api(date_str: str) -> Dict:
    """Fetch planetary data from Supabase (or fallback to API)"""
    # Try Supabase first
    if supabase:
        try:
            response = supabase.table('planetary_data')\
                .select('*')\
                .eq('date', date_str)\
                .single()\
                .execute()
            
            if response.data:
                # Transform to expected format
                data = response.data
                if data.get('planetary_data') and data['planetary_data'].get('planets'):
                    return {
                        'planetary_data': data['planetary_data']['planets']
                    }
        except Exception as e:
            print(f"⚠️ Error fetching from Supabase: {e}")
    
    # Fallback: Fetch from API
    try:
        response = requests.get(
            f"http://localhost:8000/api/planets/daily?date={date_str}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching planetary data from API: {e}")
    return None

def get_correlations_for_event(event_id: int) -> List[Dict]:
    """Fetch planetary correlations for an event from Supabase"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('event_planetary_correlations')\
            .select('*')\
            .eq('event_id', event_id)\
            .order('correlation_score', desc=True)\
            .execute()
        
        if response.data:
            return response.data
    except Exception as e:
        print(f"⚠️ Error fetching correlations: {e}")
    
    return []

def get_correlations_for_date(date_str: str) -> Dict[int, List[Dict]]:
    """Fetch all correlations for events on a specific date"""
    if not supabase:
        return {}
    
    try:
        # Get all events for the date
        events_response = supabase.table('events')\
            .select('id')\
            .eq('date', date_str)\
            .execute()
        
        if not events_response.data:
            return {}
        
        event_ids = [e['id'] for e in events_response.data]
        
        # Get correlations for all events
        correlations_response = supabase.table('event_planetary_correlations')\
            .select('*')\
            .in_('event_id', event_ids)\
            .order('correlation_score', desc=True)\
            .execute()
        
        # Group by event_id
        correlations_by_event = {}
        if correlations_response.data:
            for corr in correlations_response.data:
                event_id = corr['event_id']
                if event_id not in correlations_by_event:
                    correlations_by_event[event_id] = []
                correlations_by_event[event_id].append(corr)
        
        return correlations_by_event
    except Exception as e:
        print(f"⚠️ Error fetching correlations for date: {e}")
    
    return {}

def send_email(subject: str, html_body: str, text_body: str = None):
    """Send email using SMTP"""
    if not EMAIL_USER or not EMAIL_PASSWORD or not RECIPIENT_EMAIL:
        print("⚠️ Email configuration missing. Saving to file instead.")
        # Save to file
        output_file = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_body)
        print(f"✅ Email saved to {output_file}")
        return
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        
        # Add both text and HTML versions
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        # Save to file as backup
        output_file = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_body)
        print(f"💾 Email saved to {output_file} as backup")

def generate_daily_summary(date_str: str) -> str:
    """Generate daily summary HTML"""
    events = get_events_from_api(date_str)
    planetary_data = get_planetary_data_from_api(date_str)
    
    world_events = [e for e in events if e.get('event_type', 'world') == 'world']
    personal_events = [e for e in events if e.get('event_type') == 'personal']
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
            .section {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
            .event {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .event-title {{ font-weight: bold; color: #667eea; font-size: 16px; }}
            .event-meta {{ color: #666; font-size: 12px; margin-top: 5px; }}
            .planet-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }}
            .planet-item {{ background: white; padding: 10px; border-radius: 5px; text-align: center; }}
            .planet-name {{ font-weight: bold; color: #667eea; }}
            .planet-position {{ font-size: 12px; color: #666; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-box {{ text-align: center; padding: 15px; background: white; border-radius: 5px; }}
            .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
            .stat-label {{ font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌟 Cosmic Diary - Daily Summary</h1>
                <p>Date: {date_str}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{len(world_events)}</div>
                    <div class="stat-label">World Events</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(personal_events)}</div>
                    <div class="stat-label">Personal Events</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(events)}</div>
                    <div class="stat-label">Total Events</div>
                </div>
            </div>
    """
    
    # Get correlations for all events
    correlations_by_event = get_correlations_for_date(date_str)
    
    if world_events:
        html += """
            <div class="section">
                <h2>🌍 World Events</h2>
        """
        for event in world_events:
            event_id = event.get('id')
            correlations = correlations_by_event.get(event_id, []) if event_id else []
            
            html += f"""
                <div class="event">
                    <div class="event-title">{event.get('title', 'Unknown')}</div>
                    <div class="event-meta">
                        {event.get('category', 'Other')} • {event.get('impact_level', 'medium').upper()} Impact
                        {f"• {event.get('location', '')}" if event.get('location') else ''}
                    </div>
                    {f"<p style='margin-top: 10px;'>{event.get('description', '')}</p>" if event.get('description') else ''}
            """
            
            # Add planetary correlations if available
            if correlations:
                html += """
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                        <div style="font-weight: bold; color: #667eea; margin-bottom: 10px;">🔮 Planetary Significance:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """
                for corr in correlations[:5]:  # Top 5 correlations
                    score = corr.get('correlation_score', 0)
                    planet = corr.get('planet_name', 'Unknown')
                    reason = corr.get('reason', '')
                    percentage = int(score * 100)
                    
                    html += f"""
                        <div style="background: #f0f4ff; padding: 8px 12px; border-radius: 5px; flex: 1; min-width: 150px;">
                            <div style="font-weight: bold; color: #667eea;">{planet}</div>
                            <div style="font-size: 12px; color: #666; margin-top: 5px;">
                                <div style="background: #e0e0e0; height: 6px; border-radius: 3px; margin-top: 5px;">
                                    <div style="background: #667eea; height: 100%; width: {percentage}%; border-radius: 3px;"></div>
                                </div>
                                <div style="margin-top: 3px;">{percentage}% relevance</div>
                                {f"<div style='font-size: 11px; color: #888; margin-top: 3px;'>{reason}</div>" if reason else ''}
                            </div>
                        </div>
                    """
                html += """
                        </div>
                    </div>
                """
            
            html += "</div>"
        html += "</div>"
    
    if personal_events:
        html += """
            <div class="section">
                <h2>👤 Personal Events</h2>
        """
        for event in personal_events:
            html += f"""
                <div class="event">
                    <div class="event-title">{event.get('title', 'Unknown')}</div>
                    <div class="event-meta">
                        {event.get('category', 'Other')} • {event.get('impact_level', 'medium').upper()} Impact
                    </div>
                    {f"<p style='margin-top: 10px;'>{event.get('description', '')}</p>" if event.get('description') else ''}
                </div>
            """
        html += "</div>"
    
    if planetary_data and planetary_data.get('planetary_data'):
        html += """
            <div class="section">
                <h2>🔮 Planetary Positions</h2>
                <div class="planet-grid">
        """
        for planet in planetary_data['planetary_data']:
            html += f"""
                    <div class="planet-item">
                        <div class="planet-name">{planet.get('name', 'Unknown')}</div>
                        <div class="planet-position">
                            {planet.get('rasi', {}).get('name', 'Unknown')} {planet.get('longitude', 0):.1f}°
                            {f"<br><span style='color: blue;'>Retrograde</span>" if planet.get('is_retrograde') else ''}
                        </div>
                    </div>
            """
        html += """
                </div>
            </div>
        """
    
    html += """
            <div class="section" style="text-align: center; margin-top: 30px;">
                <p style="color: #666;">Generated by Cosmic Diary - Your Astrological Research Companion</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generate_weekly_analysis(start_date: str, end_date: str) -> str:
    """Generate weekly analysis report HTML"""
    # Get all events for the week
    events = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_dt:
        date_str = current_date.strftime('%Y-%m-%d')
        day_events = get_events_from_api(date_str)
        events.extend(day_events)
        current_date += timedelta(days=1)
    
    world_events = [e for e in events if e.get('event_type', 'world') == 'world']
    personal_events = [e for e in events if e.get('event_type') == 'personal']
    
    # Analyze patterns
    category_counts = {}
    impact_counts = {}
    retrograde_days = []
    
    for event in events:
        category = event.get('category', 'Other')
        category_counts[category] = category_counts.get(category, 0) + 1
        
        impact = event.get('impact_level', 'medium')
        impact_counts[impact] = impact_counts.get(impact, 0) + 1
    
    # Check retrograde days
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    while current_date <= end_dt:
        date_str = current_date.strftime('%Y-%m-%d')
        planetary_data = get_planetary_data_from_api(date_str)
        if planetary_data and planetary_data.get('planetary_data'):
            has_retrograde = any(p.get('is_retrograde') for p in planetary_data['planetary_data'])
            if has_retrograde:
                retrograde_days.append(date_str)
        current_date += timedelta(days=1)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
            .section {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
            .chart-container {{ background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            .insight {{ background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 15px 0; }}
            .insight-title {{ font-weight: bold; color: #856404; margin-bottom: 10px; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat-number {{ font-size: 32px; font-weight: bold; color: #667eea; }}
            .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌟 Cosmic Diary - Weekly Analysis Report</h1>
                <p>Week: {start_date} to {end_date}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(world_events)}</div>
                    <div class="stat-label">World Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(personal_events)}</div>
                    <div class="stat-label">Personal Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(retrograde_days)}</div>
                    <div class="stat-label">Retrograde Days</div>
                </div>
            </div>
    """
    
    # Category distribution
    if category_counts:
        html += """
            <div class="section">
                <h2>📊 Event Categories</h2>
                <div class="chart-container">
        """
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(events)) * 100
            html += f"""
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>{category}</strong></span>
                            <span>{count} events ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #667eea; height: 100%; width: {percentage}%; transition: width 0.3s;"></div>
                        </div>
                    </div>
            """
        html += "</div></div>"
    
    # Impact analysis
    if impact_counts:
        html += """
            <div class="section">
                <h2>⚡ Impact Level Distribution</h2>
                <div class="chart-container">
        """
        for impact, count in sorted(impact_counts.items(), key=lambda x: ['low', 'medium', 'high', 'critical'].index(x[0])):
            percentage = (count / len(events)) * 100
            color = {
                'low': '#10b981',
                'medium': '#f59e0b',
                'high': '#f97316',
                'critical': '#ef4444'
            }.get(impact, '#667eea')
            
            html += f"""
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>{impact.upper()}</strong></span>
                            <span>{count} events ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: {color}; height: 100%; width: {percentage}%;"></div>
                        </div>
                    </div>
            """
        html += "</div></div>"
    
    # Astrological insights
    html += """
            <div class="section">
                <h2>🔮 Astrological Insights</h2>
    """
    
    if retrograde_days:
        html += f"""
                <div class="insight">
                    <div class="insight-title">Retrograde Periods</div>
                    <p>This week had {len(retrograde_days)} days with retrograde planets. Retrograde periods often correlate with delays, introspection, and revisiting past issues.</p>
                    <p><strong>Retrograde Days:</strong> {', '.join(retrograde_days)}</p>
                </div>
        """
    
    if personal_events:
        html += f"""
                <div class="insight">
                    <div class="insight-title">Personal Events Analysis</div>
                    <p>You recorded {len(personal_events)} personal events this week. Review the planetary positions on those dates to identify patterns in your life.</p>
                </div>
        """
    
    html += """
            </div>
            
            <div class="section" style="text-align: center; margin-top: 30px;">
                <p style="color: #666;">Generated by Cosmic Diary - Your Astrological Research Companion</p>
                <p style="color: #666; font-size: 12px;">Continue recording events to build a comprehensive database for pattern analysis</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_daily_summary():
    """Send daily summary email"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get events for today
    events = get_events_from_api(today)
    
    if not events:
        print(f"No events found for {today}")
        # Still send email with planetary data
        html = generate_daily_summary(today)
        text = f"Daily Summary for {today}\n\nNo events recorded today.\n\nSee HTML version for planetary positions."
    else:
        html = generate_daily_summary(today)
        text = f"Daily Summary for {today}\n\n{len(events)} events recorded.\n\nSee HTML version for full details."
    
    send_email(
        subject=f"🌟 Cosmic Diary - Daily Summary ({today})",
        html_body=html,
        text_body=text
    )

def send_weekly_analysis():
    """Send weekly analysis email"""
    today = datetime.now()
    # Get Monday of current week
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    
    start_date = monday.strftime('%Y-%m-%d')
    end_date = sunday.strftime('%Y-%m-%d')
    
    html = generate_weekly_analysis(start_date, end_date)
    text = f"Weekly Analysis Report\n\nWeek: {start_date} to {end_date}\n\nSee HTML version for full details."
    
    send_email(
        subject=f"🌟 Cosmic Diary - Weekly Analysis ({start_date} to {end_date})",
        html_body=html,
        text_body=text
    )

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'daily':
            send_daily_summary()
        elif sys.argv[1] == 'weekly':
            send_weekly_analysis()
        else:
            print("Usage: python3 email_reports.py [daily|weekly]")
    else:
        # Default: send daily summary
        send_daily_summary()

