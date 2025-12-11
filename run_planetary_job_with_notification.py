#!/usr/bin/env python3
"""
On-Demand Planetary Job with Email Notification
Runs the daily planetary job and sends email notification on completion
"""

import os
import sys
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()

# Load .env files from script directory
env_local_path = SCRIPT_DIR / '.env.local'
env_path = SCRIPT_DIR / '.env'

if env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

# Import the daily planetary job functions
sys.path.insert(0, str(SCRIPT_DIR))
from daily_planetary_job import main as run_planetary_job

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', EMAIL_USER)  # Default to sender if not set

def send_email_notification(subject: str, body: str, success: bool = True):
    """Send email notification"""
    if not EMAIL_USER or not EMAIL_PASSWORD or not RECIPIENT_EMAIL:
        print("⚠️  Email credentials not configured. Skipping email notification.")
        print("   Set EMAIL_USER, EMAIL_PASSWORD, and RECIPIENT_EMAIL in .env.local")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html'))
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, text)
        server.quit()
        
        print(f"✅ Email notification sent to {RECIPIENT_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def format_email_body(success: bool, target_date: date, details: str):
    """Format HTML email body"""
    status_icon = "✅" if success else "❌"
    status_color = "#22c55e" if success else "#ef4444"
    status_text = "SUCCESS" if success else "FAILED"
    
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 20px; border-radius: 0 0 10px 10px; }}
            .status {{ background: {status_color}; color: white; padding: 10px 15px; 
                      border-radius: 5px; display: inline-block; margin: 10px 0; }}
            .details {{ background: white; padding: 15px; border-radius: 5px; 
                       margin: 15px 0; border-left: 4px solid {status_color}; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; 
                      font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Cosmic Diary - Planetary Job Report</h1>
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
                </div>
                
                <h3>Details:</h3>
                <div class="details">
                    <pre style="white-space: pre-wrap; font-family: monospace;">{details}</pre>
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
    """Main function - Run planetary job and send notification"""
    print("🌙 Starting On-Demand Planetary Job with Email Notification")
    print("=" * 60)
    
    # Determine target date (default to today)
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"❌ Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = date.today()
    
    print(f"📅 Target date: {target_date.isoformat()}")
    print(f"📧 Notification will be sent to: {RECIPIENT_EMAIL or 'Not configured'}")
    print("")
    
    # Capture output
    import io
    from contextlib import redirect_stdout, redirect_stderr
    
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    success = False
    details = ""
    
    try:
        # Temporarily override sys.argv for the planetary job
        original_argv = sys.argv.copy()
        sys.argv = [sys.argv[0], str(target_date)]
        
        # Capture stdout and stderr
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            # Run the planetary job
            try:
                run_planetary_job()
                success = True
            except SystemExit as e:
                # The planetary job uses sys.exit(0) for success, sys.exit(1) for failure
                success = (e.code == 0)
                if e.code != 0:
                    details = f"Job exited with code {e.code}"
            except Exception as e:
                success = False
                details = f"Exception occurred: {str(e)}"
        
        # Restore original argv
        sys.argv = original_argv
        
        # Get captured output
        stdout_output = output_buffer.getvalue()
        stderr_output = error_buffer.getvalue()
        
        # Combine output for details
        details = stdout_output + stderr_output + details
        
        print("📊 Job Output:")
        print("-" * 60)
        print(stdout_output)
        if stderr_output:
            print("⚠️  Errors/Warnings:")
            print(stderr_output)
        print("-" * 60)
        
    except Exception as e:
        success = False
        details = f"Failed to run job: {str(e)}"
        print(f"❌ Error: {details}")
    
    # Send email notification
    print("")
    print("📧 Sending email notification...")
    
    subject = f"🌙 Cosmic Diary - Planetary Job {'Success' if success else 'Failed'}"
    body = format_email_body(success, target_date, details or "No additional details available")
    
    email_sent = send_email_notification(subject, body, success)
    
    # Final status
    print("")
    if success:
        print("✅ Job completed successfully!")
    else:
        print("❌ Job failed!")
    
    if email_sent:
        print("✅ Email notification sent")
    else:
        print("⚠️  Email notification not sent (check configuration)")
    
    print("")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

