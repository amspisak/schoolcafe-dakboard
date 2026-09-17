import requests

url = "https://webapis.schoolcafe.com/api/GetSchoolsList"

response = requests.get(url)

print(response.status_code)
print(response.text)
