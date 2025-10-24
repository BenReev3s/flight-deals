import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

USERNAME = os.getenv('SHEETY_USERNAME')
PASSWORD = os.getenv("SHEETY_PASSWORD")

# print("USERNAME:", USERNAME)
# print("PASSWORD:", PASSWORD)
class DataManager:
    def __init__(self):
        self.end_point = "https://api.sheety.co/495bee945b60f16d5a876dcd6f631538/flightDeals/prices"

    def update_iata_code(self, row_id, iata_code):
        url = f"{self.end_point}/{row_id}"
        parameters = {
            "price": {
                "iataCode": iata_code
            }
        }
        res = requests.put(url=url, json=parameters,auth=HTTPBasicAuth(USERNAME, PASSWORD))
        print(res.status_code, res.text)
        res.raise_for_status()
        return res.json()