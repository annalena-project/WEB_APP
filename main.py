import requests

URL = " https://geocoding-api.open-meteo.com/v1/search"

parameters = {
    "name": "Toronto",
    "country": "Canada",
    "count": 1
}

response = requests.get(URL, params = parameters, timeout = 10)

print(response.status_code)
print(response.json())
