import os
from http import client
import smtplib

from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

        self.SMTP_USERNAME = os.getenv('EMAIL')
        self.SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
        self.connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.connection.starttls()
        self.connection.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)


    def send_notification(self, departure_airport, destination_airport, out_date, return_date, price):
        message = self.client.messages.create(
            body=f"-Low price alert! Only {price} to fly from {departure_airport} to {destination_airport} on {out_date} until {return_date}",
            from_="whatsapp:+14155238886",
            to="whatsapp:+447305974095"
        )
        print(f"Message sent: {message.status}")

    def send_email(self, email_list, departure_airport, destination_airport, out_date, return_date, price):
        for email in email_list:
            self.connection.sendmail(
                from_addr=self.SMTP_USERNAME,
                to_addrs=email,
                msg=f"Subject: Low Price Alert!\n\n-Low price alert! Only {price} to fly from {departure_airport} to {destination_airport} on {out_date} until {return_date}"
            )

