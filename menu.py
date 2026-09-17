import requests
import json
from datetime import datetime, timedelta

SCHOOL_ID = "d9edb69f-dc06-41a4-8d8d-15c3e47d812f"

url = "https://webapis.schoolcafe.com/api/CalendarView/GetDailyMenuitems"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.schoolcafe.com/"
}


def get_entrees(date):
    params = {
        "SchoolId": SCHOOL_ID,
        "ServingDate": date.strftime("%m-%d-%Y"),
        "ServingLine": "Main Line",
        "MealType": "Lunch",
        "compressImages": "false"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    items = []

    def find_entrees(obj):
        if isinstance(obj, dict):
            if obj.get("Category") == "ENTREES":
                description = obj.get("MenuItemDescription")
                if isinstance(description, str) and description.strip():
                    items.append(description.strip())
            else:
                for value in obj.values():
                    find_entrees(value)

        elif isinstance(obj, list):
            for item in obj:
                find_entrees(item)

    find_entrees(data)

    return list(dict.fromkeys(items))


today = datetime.now()
tomorrow = today + timedelta(days=1)

today_items = get_entrees(today)
tomorrow_items = get_entrees(tomorrow)

today_display = today.strftime("%A, %B %-d")
tomorrow_display = tomorrow.strftime("%A, %B %-d")


menu_data = {
    "school": "Butts Road Intermediate",

    "today": today_display,
    "today_item1": today_items[0] if len(today_items) > 0 else "",
    "today_item2": today_items[1] if len(today_items) > 1 else "",
    "today_item3": today_items[2] if len(today_items) > 2 else "",
    "today_item4": today_items[3] if len(today_items) > 3 else "",
    "today_item5": today_items[4] if len(today_items) > 4 else "",

    "tomorrow": tomorrow_display,
    "tomorrow_item1": tomorrow_items[0] if len(tomorrow_items) > 0 else "",
    "tomorrow_item2": tomorrow_items[1] if len(tomorrow_items) > 1 else "",
    "tomorrow_item3": tomorrow_items[2] if len(tomorrow_items) > 2 else "",
    "tomorrow_item4": tomorrow_items[3] if len(tomorrow_items) > 3 else "",
    "tomorrow_item5": tomorrow_items[4] if len(tomorrow_items) > 4 else ""
}


with open("menu.json", "w", encoding="utf-8") as f:
    json.dump(menu_data, f, indent=2)


print("Created menu.json")
print()
print(today_display)
for item in today_items:
    print(item)

print()
print(tomorrow_display)
for item in tomorrow_items:
    print(item)
