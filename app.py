import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os # used to access environment variable

from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS # to allow access methods from external domain

app = Flask(__name__)
origin="./static/contact.html"
CORS(app, origins=origin)

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
        return True

    except Exception as e:
        print(f'Error sending email: {str(e)}')
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/send", methods=["GET","POST"])
def send():
    if request.method == "GET":
        return render_template("success.html")
    elif request.method == "POST":
        print('You post data')
        sender_email = os.environ.get('ZOHO_USER')  # ZOHO_USER is the environment variable which contains actual email
        sender_password = os.environ.get('ZOHO_APP_PWD')  # ZOHO_APP_PWD is also the environment variable
        
        recipient_email = sender_email.replace('zoho','live')
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('sub')
        message = request.form.get('msg')
        total_msg = f'{name} having email {email} sent message through contact page\n\n\
                    ---------\n\
                    Subject: {subject}\n\
                    ----------\n\
                    {message}'

        print(name, email, subject, message)
        # send_email(sender_email, sender_password, recipient_email, subject, total_msg)
        # return render_template("success.html")
        return redirect(url_for('static', filename='contact.html'))
    else:
        return render_template("failure.html")

if __name__ == '__main__':
    app.run()