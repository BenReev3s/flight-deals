import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from flight_data import FlightData
load_dotenv()

class FlightSearch:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("AMADUES_API_KEY")
        self._api_secret = os.getenv("AMADUES_API_SECRET")
        self._token = self._get_new_token()


    def _get_new_token(self):
        token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }

        res = requests.post(token_url, headers=headers, data=data)
        res.raise_for_status()

        token_info = res.json()
        access_token = token_info["access_token"]
        return access_token

    def get_iata_code(self, city_name):
        flight_search_url = "https://test.api.amadeus.com/v1/reference-data/locations"
        headers = {
            "Authorization": f"Bearer {self._token}",
        }
        params = {
            "subType": "AIRPORT,CITY",
            "keyword": city_name,
        }

        res = requests.get(flight_search_url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json()

        if data.get("data") and len(data.get("data")) > 0:
            iata_code = data["data"][0]["iataCode"]
            print(iata_code)
            return iata_code
        else:
            print(f"{city_name} not found")
            return None

    def search_flights(self, iata_code):
        flight_search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        today = datetime.now()
        tommorow = today + timedelta(days=1)
        six_months_later = tommorow + timedelta(days=180)

        headers = {
            "Authorization": f"Bearer {self._token}",
        }
        params = {
            "originLocationCode": "LON",
            "destinationLocationCode": iata_code,
            "departureDate": tommorow.strftime("%Y-%m-%d"),
            "returnDate": six_months_later.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
        }

        res = requests.get(flight_search_url, headers=headers, params=params)
        flight_details = res.json()

        return FlightData.find_cheapest_flight(flight_details)