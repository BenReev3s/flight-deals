
class FlightData:
    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, stops ):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    def __repr__(self):
        return f"{self.destination_city}: £{self.price} ({self.out_date} → {self.return_date}, {self.stops})"

    @staticmethod
    def find_cheapest_flight(data):
        try:
            flights = data["data"]
            if not flights:
                return None

            cheapest = flights[0]

            price = cheapest["price"]["total"]

            #outbound segments
            outbound_segments = cheapest["itineraries"][0]["segments"]
            outbound = cheapest["itineraries"][0]["segments"][0]
            inbound = cheapest["itineraries"][1]["segments"][0]

            num_of_stops = len(cheapest["itineraries"][0]["segments"]) - 1

            departure_airport = outbound["departure"]["iataCode"]
            final_segment = outbound_segments[-1]
            destination_airport = final_segment["arrival"]["iataCode"]
            out_date = outbound["departure"]["at"]
            return_airport = inbound["arrival"]["iataCode"]
            return_time = inbound["arrival"]["at"]

            print(cheapest["itineraries"][0]["segments"])

            return FlightData(
                price=price,
                origin_city="London",
                origin_airport=departure_airport,
                destination_city=destination_airport,
                destination_airport=destination_airport,
                out_date=out_date,
                return_date=return_time,
                stops=num_of_stops
            )
        except(KeyError, IndexError, TypeError):
            return None

