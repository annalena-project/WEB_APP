import requests

URL = " https://geocoding-api.open-meteo.com/v1/search"

parameters = {
    "name": "Toronto",      # name[city]
    "country": "Canada",
    "count": 1
}

response = requests.get(URL, params = parameters, timeout = 10)

print(response.status_code)
print(response.json())

data = response.json()

result = data["results"]
first_result = result[0]

latitude = first_result["latitude"]
longitude = first_result["longitude"]

print("latitude:", latitude)
print("longitude:", longitude)

