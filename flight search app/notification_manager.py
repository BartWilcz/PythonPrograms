import smtplib
from twilio.rest import Client
import os

TWILIO_SID = os.get_env("TWILIO_SID")#"ACf19b4d58d7f922ea01d6f952c2a103b8"
TWILIO_AUTH_TOKEN =  os.get_env("TWILIO_AUTH_TOKEN")     #"e689fb8ac7edc2c592383a25a8bc8157"
TWILIO_VIRTUAL_NUMBER = os.get_env("TWILIO_VIRTUAL_NUMBER")     #"+12708354704"
TWILIO_VERIFIED_NUMBER = os.get_env("TWILIO_VERIFIED_NUMBER")     #"+48533555882"

my_email = os.get_env("EMAIL")     #"barpython28@gmail.com"
password = os.get_env("EMAIL_PASS")      #"ddeldmtesnomktan"

class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)


    def send_email(self, emails, message, google_flight_link=""):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for email in emails:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=message,
                )