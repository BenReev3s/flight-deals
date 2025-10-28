import requests
import time
from pprint import pprint
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from notification_manager import NotificationManager
load_dotenv()

USERNAME = os.getenv('SHEETY_USERNAME')
PASSWORD = os.getenv("SHEETY_PASSWORD")

SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
SHEETY_URL = "https://api.sheety.co/495bee945b60f16d5a876dcd6f631538/flightDeals/prices"

res = requests.get(url=SHEETY_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
res.raise_for_status()
data = res.json()
sheet_data = data["prices"]

flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()

customer_data = data_manager.get_customer_emails()
customer_emails = [user["whatIsYourEmail?"] for user in customer_data["users"]]
print(customer_emails)

for item in sheet_data:
    if item["iataCode"] == "":
        code = flight_search.get_iata_code(item["city"])
        time.sleep(2)
        if code:
            item["iataCode"] = code
            data_manager.update_iata_code(item["id"], code)


for item in sheet_data:
    if item["iataCode"] != "":
        flight = flight_search.search_flights(item["iataCode"])
        if flight:
            print(flight)
            lowest_price = item["lowestPrice"]
            print(flight.price)
            if float(flight.price) < float(lowest_price):
                notification_manager.send_notification(flight.origin_airport, flight.destination_airport, flight.out_date, flight.return_date, flight.price)
            else:
                pass
        else:
            print(f"No offers found for {item['city']}")
    else:
        print(f"no Iata code for {item['city']}")





