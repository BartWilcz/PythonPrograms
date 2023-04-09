import requests
from flight_data import FlightData
import pprint
import os

TEQUILA_API = os.get_env("Tequila_api")
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
headers = {"apikey": TEQUILA_API}


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def get_Iata_Codes(self, data):
        new_data = [dict(item, iataCode='TESTING') for item in data]
        return new_data

    def get_Airport_Code_By_City_Name(self, city_name):
        """Returning city IATA code based on city name"""
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        return results[0]["code"]

    def find_Flight(self, city_from, city_to, date_from, date_to):
        """Finding best flight from a given city"""
        location_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        query = {
            "fly_from": city_from,
            "fly_to": city_to,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR",
        }
        try:
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {city_to}.")
            query["max_stopovers"] = 2
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            data = response.json()["data"][0]
            print(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(price=data["price"],
                                     origin_city=data["route"][0]["cityFrom"],
                                     origin_airport=data["route"][0]["flyFrom"],
                                     destination_city=data["route"][0]["cityTo"],
                                     destination_airport=data["route"][0]["flyTo"],
                                     out_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0])
            pprint.pprint(vars(flight_data))
            return flight_data

