import requests

URL = "https://geocoding-api.open-meteo.com/v1/search"

parameters = {
    "name": "Chicago",      # name[city]
    "country": "USA",
    "count": 1
}

response = requests.get(URL, params = parameters, timeout = 10)
print(response.status_code)

data = response.json()

result = data["results"]
first_result = result[0]

latitude = first_result["latitude"]
longitude = first_result["longitude"]

print("latitude:", latitude)
print("longitude:", longitude)

Forcaste_URL = " https://api.open-meteo.com/v1/forecast?current_weather=true" 

forecast_parameters = {
    "longitude": longitude,
    "latitude": latitude,
}

forecast_response = requests.get(Forcaste_URL, params = forecast_parameters, timeout = 10)
forecast_data = forecast_response.json()

print(forecast_response.status_code)

class WeatherReport:
    def __init__(self, city, country, latitude, longitude, temperature, elevation, windspeed, observation_time):
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.elevation = elevation
        self.windspeed = windspeed
        self.observation_time = observation_time

report = WeatherReport(
    city=parameters["name"],
    country=parameters["country"],
    latitude=forecast_parameters["latitude"],
    longitude=forecast_parameters["longitude"],
    temperature=forecast_data["current_weather"]["temperature"],
    elevation=forecast_data["elevation"],
    windspeed=forecast_data["current_weather"]["windspeed"],
    observation_time=forecast_data["current_weather"]["time"]
)

print("city:", report.city)
print("country:", report.country)
print("latitude:", report.latitude)
print("longitude:", report.longitude)
print("temperature:", report.temperature)
print("elevation:", report.elevation)
print("windspeed:", report.windspeed)
print("time:", report.observation_time)
