import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        # Set up the email server (Zoho Mail in this example)
        smtp_server = 'smtp.zoho.com'
        port = 465  # For SSL encryption

        server = smtplib.SMTP_SSL(smtp_server, port)

        # Log in to the email server
        server.login(sender_email, sender_password)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the connection to the server
        server.quit()

        print('Email sent successfully!')

    except Exception as e:
        print(f'Error sending email: {str(e)}')

if __name__ == '__main__':
    sender_email = os.environ.get('ZOHO_USER')  # ZOHO_USER is the environment variable which contains actual email
    sender_password = os.environ.get('ZOHO_APP_PWD')  # ZOHO_APP_PWD is also the environment variable
    
    recipient_email = sender_email.replace('zoho', 'live')  # Replace with the recipient's email address
    subject = 'Test Email from Zoho Mail using app with environment variable'
    message = 'This is a test email sent from a Python script using Zoho Mail.'

    send_email(sender_email, sender_password, recipient_email, subject, message)
