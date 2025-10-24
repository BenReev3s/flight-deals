import requests
import time
from pprint import pprint
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
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

for item in sheet_data:
    if item["iataCode"] == "":
        code = flight_search.get_iata_code(item["city"])
        time.sleep(2)
        if code:
            item["iataCode"] = code
            data_manager.update_iata_code(item["id"], code)

# pprint(sheet_data)

for item in sheet_data:
    if item["iataCode"] != "":
        price = flight_search.search_flights(item["iataCode"])
        if price:
            print(price)
        else:
            print(f"No offers found for {item['city']}")
    else:
        print(f"no Iata code for {item['city']}")





