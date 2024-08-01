# Function to send email
import os
import smtplib
from email.message import EmailMessage
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path: str = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return base_path + relative_path


import os
import json
import smtplib
from email.message import EmailMessage


def send_email(subject, body, attachment_paths):
    json_path = resource_path("/config/email-config.json")
    # json_path = "../config/email-config.json"
    # Read sender and recipient details from JSON file
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    sender_email = data['sender']['email']
    email_password = data['sender']['password']
    recipient_emails = data['recipient']['email_list']

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg.set_content(body)

    # Add the attachments
    for attachment_path in attachment_paths:
        if os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        else:
            print(f"File {attachment_path} does not exist.")

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender_email, email_password)
            smtp.send_message(msg)
        print("Email alert has been sent.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
