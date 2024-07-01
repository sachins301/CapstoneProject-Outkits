# Function to send email
import os
import smtplib
from email.message import EmailMessage


def send_email(subject, body, to, attachment_paths):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "outkitsteam@gmail.com"
    msg['To'] = to
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

    email_password = 'linq uvgf vagb beay'  # Replace with the generated app-specific password

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("outkitsteam@gmail.com", email_password)
            smtp.send_message(msg)
        print("Email alert has been sent.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")