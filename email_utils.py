import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def send_email(subject: str, body: str, recipient_email: str) -> None:
    """
    Send an email using SMTP.
    
    Args:
        subject (str): Email subject
        body (str): Email body
        recipient_email (str): Recipient's email address
    """
    try:
        # Email configuration
        sender_email = os.getenv('EMAIL_ADDRESS')
        sender_password = os.getenv('EMAIL_PASSWORD')
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Add body
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            
        logger.info(f"Email sent successfully to {recipient_email}")
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise

def format_thought_email(original_text: str, corrected_text: str) -> tuple[str, str]:
    """
    Format the email content for the thought.
    
    Args:
        original_text (str): Original text from OCR
        corrected_text (str): Grammar-corrected text
        
    Returns:
        tuple[str, str]: Email subject and body
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Captured Thought - {timestamp}"
    
    body = f"""Your captured thought has been processed and is ready for safekeeping!

Original Text:
{original_text}

Corrected Version:
{corrected_text}

Captured on: {timestamp}
"""
    
    return subject, body 