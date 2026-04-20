import requests
from populate import DatabaseManager, WeatherReport

cities = [                      
    ("Chicago", "USA"),
    ("New York", "USA"),
    ("Paris", "France"),
    ("Rome", "Italy"),
    ("Copenhagen", "Denmark"),
    ("Stockholm", "Sweden"),
    ("Barcelona", "Spain"),
    ("London", "UK"),
    ("Berlin", "Germany"),
    ("Amsterdam", "Netherlands")
]

db = DatabaseManager()

for city, country in cities:
    geo = requests.get( "https://geocoding-api.open-meteo.com/v1/search",params={"name": city, "count": 1}).json()["results"][0]
    # Loop + geocoding API to find where the city is

    latitude = geo["latitude"]
    longitude = geo["longitude"]

    weather = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": latitude, "longitude": longitude, "current_weather": "true"}).json()["current_weather"]
    # Call weather API to get current weather data

    report = WeatherReport(
        city,
        country,
        latitude,
        longitude,
        weather["temperature"],
        0,
        weather["windspeed"],
        weather["time"]
    )

    db.insert_observation(report)     # Insert new data into database

data = db.get_all_observations()      # Get all observations

for row in data:
    print(f"ID: {row[0]}, City: {row[1]}, Temp: {row[5]}") # Printing all observation 

print(db.get_observation_by_id(1)) # Get one observation by ID number

db.update(1, 59.33, 18.06)         # Update latitude & longitude for ID number 1
print(db.get_observation_by_id(1)) # Checking updated observation

db.delete_observation_by_id(1)      # Delete observation with ID number 1

data = db.get_all_observations()    # Get all observations again after delete

for row in data:
    print(f"ID: {row[0]}, City: {row[1]}, Temp: {row[5]}")  # Print teh remaining observations

db.con.close()      # Close database connection 

