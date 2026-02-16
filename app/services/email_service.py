import smtplib
from email.mime.text import MIMEText


def send_email(subject: str, body: str, to_email: str):

    sender_email = "abhay20043@gmail.com"
    sender_password = "lqrrrpziqmvvqqas"  # App password

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, message.as_string())
    server.quit()
