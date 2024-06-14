import importlib.util
import os
import smtplib
import time
from email.message import EmailMessage
import datetime

# Load the existing code from the provided file
file_path = 'xlsx_mercari.py'

spec = importlib.util.spec_from_file_location("mercari_script", file_path)
mercari_script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mercari_script)

def send_email(subject, body, to, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "jhondow@gmail.com" #add you email
    msg['To'] = to
    msg.set_content(body)

    # Add the attachment
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Use the app-specific password
    email_password = 'xxxx xxxx xxxx xxxx'  # Replace with the generated app-specific password that needs to be create for google here https://myaccount.google.com/u/2/apppasswords?pli=1&pageId=none&rapt=AEjHL4MXBCiMMgMYhIVabX58Z9jc_3aHAI7_D4_1RSm35WDfWOHQzXJUVg3SWnwyPIfM9uZ_y_WfS3smDXkCL0cyCpTzFkgD4PXXRcQMD1w7KO7Apb0tMN0

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("Johndow@gmail.com", email_password) # add your email
            smtp.send_message(msg)
        print("Email alert has been sent.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Assuming the imported script saves the output file as "search_results.xlsx"
output_file = "search_results.xlsx"

# Send email alert with the Excel file attached
send_email(
    subject="Search Results",
    body="Please find attached the search results.",
    to="mariadow@gmail.com",
    attachment_path=output_file
)

print ('successfully sent the mail')
# Sleep for 24 hours (86400 seconds)
        time.sleep(86400)

if __name__ == "__main__":
    main()

