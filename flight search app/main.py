from data_manager import DataManager
from flight_search import FlightSearch
import datetime
from notification_manager import NotificationManager
import pprint

STARTING_CITY ="Warsaw"
#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

sheetly = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = sheetly.getWorksheetData()
users_data = sheetly.get_Users_data()
emails_list = [email['email'] for email in users_data]

iata_list = [item['iataCode'] for item in sheet_data if len(item['iataCode']) > 0]

if not iata_list:
    for item in sheet_data:
        city_code = flight_search.get_Airport_Code_By_City_Name(item["city"])
        item["iataCode"] = city_code

sheetly.data = sheet_data

fly_from_city_code = flight_search.get_Airport_Code_By_City_Name(STARTING_CITY)
date_from = datetime.datetime.now() + datetime.timedelta(days=1)
date_to = datetime.datetime.now() + datetime.timedelta(days=6*30)

pp = pprint.PrettyPrinter(indent=4)
price_list = []

for city in sheet_data:
    city_to = city["iataCode"]
    flight = flight_search.find_Flight(fly_from_city_code, city_to, date_from, date_to)

    if flight is None:
        continue

    if flight.price < city["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only EUR{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )
        email_message = f"Subject:New Low price flight\n\n\Low price alert! Only {flight.price } EUR to fly {STARTING_CITY} to {city['city']} ({city_to}) from {date_from} to  {date_to} "
        notification_manager.send_email(email_message, email_message)




