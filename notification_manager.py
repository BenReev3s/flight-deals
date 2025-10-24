import os
from http import client

from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()


class NotificationManager:
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

    def send_notification(self, departure_airport, destination_airport, out_date, return_date, price):
        message = self.client.messages.create(
            body=f"-Low price alert! Only {price} to fly from {departure_airport} to {destination_airport} on {out_date} until {return_date}",
            from_="whatsapp:+14155238886",
            to="whatsapp:+447305974095"
        )
        print(f"Message sent: {message.status}")