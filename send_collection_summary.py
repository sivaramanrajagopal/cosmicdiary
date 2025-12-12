#!/usr/bin/env python3
"""
Email Summary for Event Collection
Sends a brief summary email after each 2-hour event collection run.
"""

import os
import sys
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

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

# Supabase configuration (optional - for fetching stats)
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', os.getenv('SUPABASE_KEY', ''))

def send_summary_email(
    events_detected: int,
    events_stored: int,
    correlations_created: int,
    avg_correlation_score: Optional[float] = None,
    error_message: Optional[str] = None
) -> bool:
    """
    Send summary email after event collection.
    
    Args:
        events_detected: Number of events detected
        events_stored: Number of events stored
        correlations_created: Number of correlations created
        avg_correlation_score: Average correlation score (optional)
        error_message: Error message if collection failed (optional)
    
    Returns:
        True if email sent successfully, False otherwise
    """
    if not all([EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL]):
        print("⚠️  Email configuration missing. Skipping email notification.")
        return False
    
    try:
        now = datetime.now()
        collection_time = now.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Determine status
        if error_message:
            status = "❌ FAILED"
            status_color = "#dc2626"
            title = "Event Collection Failed"
        else:
            status = "✅ SUCCESS"
            status_color = "#10b981"
            title = "Event Collection Summary"
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f'🌟 Cosmic Diary: {title} - {collection_time}'
        
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
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .stat-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #e0e0e0;
                }}
                .stat-row:last-child {{
                    border-bottom: none;
                }}
                .stat-label {{
                    color: #666;
                    font-weight: 500;
                }}
                .stat-value {{
                    color: #333;
                    font-weight: bold;
                }}
                .error-box {{
                    background: #fee;
                    border-left: 4px solid #dc2626;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e0e0e0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌟 Cosmic Diary</h1>
                <p>Event Collection Summary</p>
                <div class="status">{status}</div>
            </div>
            
            <div class="stats">
                <div class="stat-row">
                    <span class="stat-label">Collection Time:</span>
                    <span class="stat-value">{collection_time}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Events Detected:</span>
                    <span class="stat-value">{events_detected}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Events Stored:</span>
                    <span class="stat-value">{events_stored}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Correlations Created:</span>
                    <span class="stat-value">{correlations_created}</span>
                </div>
        """
        
        if avg_correlation_score is not None:
            html_body += f"""
                <div class="stat-row">
                    <span class="stat-label">Avg Correlation Score:</span>
                    <span class="stat-value">{avg_correlation_score:.2f}/100</span>
                </div>
            """
        
        html_body += """
            </div>
        """
        
        if error_message:
            html_body += f"""
            <div class="error-box">
                <strong>Error Details:</strong><br>
                <pre style="white-space: pre-wrap; font-size: 12px;">{error_message}</pre>
            </div>
            """
        
        html_body += """
            <div class="footer">
                <p>This is an automated notification from Cosmic Diary event collection system.</p>
                <p>Generated at: """ + collection_time + """</p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = f"""
Cosmic Diary - Event Collection Summary
{'=' * 50}

Status: {status}
Collection Time: {collection_time}

Statistics:
- Events Detected: {events_detected}
- Events Stored: {events_stored}
- Correlations Created: {correlations_created}
"""
        
        if avg_correlation_score is not None:
            text_body += f"- Avg Correlation Score: {avg_correlation_score:.2f}/100\n"
        
        if error_message:
            text_body += f"\nError:\n{error_message}\n"
        
        text_body += f"\nGenerated at: {collection_time}\n"
        
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
        
        print(f"✅ Summary email sent to {RECIPIENT_EMAIL}")
        return True
    
    except Exception as e:
        print(f"❌ Error sending summary email: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function - can be called from GitHub Actions"""
    # This function can parse command-line arguments or environment variables
    # For now, it's designed to be called from GitHub Actions with stats
    
    import sys
    
    # Parse arguments (if provided)
    events_detected = int(os.getenv('EVENTS_DETECTED', '0'))
    events_stored = int(os.getenv('EVENTS_STORED', '0'))
    correlations_created = int(os.getenv('CORRELATIONS_CREATED', '0'))
    avg_score = os.getenv('AVG_CORRELATION_SCORE')
    avg_correlation_score = float(avg_score) if avg_score else None
    
    error_message = os.getenv('ERROR_MESSAGE', '')
    
    # Send email
    success = send_summary_email(
        events_detected=events_detected,
        events_stored=events_stored,
        correlations_created=correlations_created,
        avg_correlation_score=avg_correlation_score,
        error_message=error_message if error_message else None
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

