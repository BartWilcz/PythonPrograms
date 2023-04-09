import requests
import os

SHEET_ENDPOINT = os.get_env("SHEET_ENDPOINT")  
SHEET_USERS_ENDPOINT = os.get_env("USER_ENDPOINT"


class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.data = {}

    def getWorksheetData(self):
        response = requests.get(url=SHEET_ENDPOINT)
        self.data = response.json()['prices']
        return self.data

    def updateIataColumn(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEET_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_Users_data(self):
        response = requests.get(url=SHEET_USERS_ENDPOINT)
        self.data = response.json()['users']
        return self.data
