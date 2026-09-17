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

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.schoolcafe.com/"
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

def find_items(obj):
    if isinstance(obj, dict):
        if obj.get("Category") == "ENTREES":
            description = obj.get("MenuItemDescription")
            if isinstance(description, str) and description.strip():
                items.append(description.strip())
        else:
            for value in obj.values():
                find_items(value)

    elif isinstance(obj, list):
        for item in obj:
            find_items(item)

find_items(data)

items = list(dict.fromkeys(items))

date_display = datetime.now().strftime("%A, %B %-d, %Y")

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="3600">
<title>Butts Road Intermediate Lunch</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
}}
h1 {{
    margin-bottom: 5px;
}}
h2 {{
    margin-top: 0;
    font-weight: normal;
}}
li {{
    font-size: 24px;
    margin: 12px 0;
}}
</style>
</head>
<body>
<h1>Butts Road Intermediate</h1>
<h2>Lunch — {date_display}</h2>
<ul>
"""

for item in items:
    html += f"<li>{item}</li>\n"

html += """
</ul>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

import json

menu_data = {
    "school": "Butts Road Intermediate",
    "date": date_display,
    "items": items,
    "items_text": "\n".join(items)
}

with open("menu.json", "w", encoding="utf-8") as f:
    json.dump(menu_data, f, indent=2)

print("Created index.html")
print("Created menu.json")
print("\n".join(items))
