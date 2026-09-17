import requests
from datetime import datetime

SCHOOL_ID = "d9edb69f-dc06-41a4-8d8d-15c3e47d812f"

today = datetime.now().strftime("%m-%d-%Y")

url = "https://webapis.schoolcafe.com/api/CalendarView/GetDailyMenuitems"

params = {
"SchoolId": SCHOOL_ID,
"ServingDate": today,
"ServingLine": "Main Line",
"MealType": "Lunch",
"compressImages": "false"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

print(data)
