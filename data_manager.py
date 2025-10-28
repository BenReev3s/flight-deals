import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

USERNAME = os.getenv('SHEETY_USERNAME')
PASSWORD = os.getenv("SHEETY_PASSWORD")
SHEETY_PRICES_ENDPOINT = os.getenv('SHEETY_PRICES_ENDPOINT')
SHEETY_USERS_ENDPOINT = os.getenv('SHEETY_USERS_ENDPOINT')

print(SHEETY_USERS_ENDPOINT)
print(SHEETY_PRICES_ENDPOINT)
# print("USERNAME:", USERNAME)
# print("PASSWORD:", PASSWORD)
class DataManager:
    def __init__(self):
        self.customer_email_data = SHEETY_USERS_ENDPOINT
        self.flight_data = SHEETY_PRICES_ENDPOINT


    def update_iata_code(self, row_id, iata_code):
        url = f"{self.flight_data}/{row_id}"
        parameters = {
            "price": {
                "iataCode": iata_code
            }
        }
        res = requests.put(url=url, json=parameters,auth=HTTPBasicAuth(USERNAME, PASSWORD))
        print(res.status_code, res.text)
        res.raise_for_status()
        return res.json()

    def get_customer_emails(self):
        response = requests.get(self.customer_email_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        customer_data = response.json()
        return customer_data
