
class FlightData:
    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date ):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

    def __repr__(self):
        return f"{self.destination_city}: £{self.price} ({self.out_date} → {self.return_date})"

    @staticmethod
    def find_cheapest_flight(data):
        try:
            flights = data["data"]
            if not flights:
                return None

            cheapest = flights[0]
            price = cheapest["price"]["total"]

            #outbound segments
            outbound = cheapest["itineraries"][0]["segments"][0]
            inbound = cheapest["itineraries"][1]["segments"][0]

            departure_airport = outbound["departure"]["iataCode"]
            destination_airport = outbound["arrival"]["iataCode"]
            out_date = outbound["departure"]["at"]
            return_airport = inbound["arrival"]["iataCode"]
            return_time = inbound["arrival"]["at"]

            return FlightData(
                price=price,
                origin_city="London",
                origin_airport=departure_airport,
                destination_city=destination_airport,
                destination_airport=destination_airport,
                out_date=out_date,
                return_date=return_time,
            )
        except(KeyError, IndexError, TypeError):
            return None

