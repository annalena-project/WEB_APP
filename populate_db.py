# populate_db.py - Fetches live weather data for 10 cities and saves it to the database

import requests                                               # To call the weather API
from database_manager import DatabaseManager, WeatherReport   # Import database tools from database_manager.py

#---------------------- List of Cities ----------------------------------------
# List of cities I want to add to the database
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

#--------------------- Fetch And Save Weather Data ----------------------------- 

# Create database connection 
db = DatabaseManager()      

for city, country in cities:
    #  Use the geocoding API to convert the city name into latitude and longitude
    geo = requests.get( "https://geocoding-api.open-meteo.com/v1/search",params={"name": city, "count": 1}).json()["results"][0]
   
    # The API returns a list of results – take the first one and save the coordinates
    latitude = geo["latitude"]
    longitude = geo["longitude"]

    # Use the coordinates to call weather API to get current weather
    weather = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": latitude, "longitude": longitude, "current_weather": "true"}).json()["current_weather"]

    # Create a WeatherReport object with all the data
    report = WeatherReport(
        city,
        country,
        latitude,
        longitude,
        weather["temperature"],
        0,                          # elevation is not used here so I just set it to 0
        weather["windspeed"],
        weather["time"]
    )

    # Save data to database
    db.insert_observation(report)  

# Get all observations from database
data = db.get_all_observations() 

# Print all observations
for row in data:
    print(f"ID: {row[0]}, City: {row[1]}, Temp: {row[5]}") 


#--------------------- COMMENTED OUT ----------------------------------------------------
# These lines are kept here for testing purposes

# Get one observation by ID number 1
# print(db.get_observation_by_id(1)) 

#db.update(1, 59.33, 18.06)         # Update latitude & longitude for ID number 1
#print(db.get_observation_by_id(1)) # Checking updated observation

# db.delete_observation_by_id(1)      # Delete observation with ID number 1

# Get all observations again 
# data = db.get_all_observations()    

# # Print all observations
# for row in data:
#      print(f"ID: {row[0]}, City: {row[1]}, Temp: {row[5]}")  

#----------------------------------------------------------------------------------------

db.con.close()      # Close database connection 

