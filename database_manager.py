# database_manager.py – connects to the database and handles all database operations

import psycopg2                    # To connect to PostgreSQL database
import os                          # Get acces to hidden values (like password)
from dotenv import load_dotenv     # To load the .env file containing log in details

# Load the .env file to be able to use our login details 
load_dotenv()

username = os.getenv("DB_USER")         # Databse username 
password = os.getenv("password")        # Database password    
database = os.getenv("DATABASE_URL")    # Database name    

#--------------------- Weather Report ----------------------------------------------------
#This is a class that holds all weather data for one city
 
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

#--------------------- Database Manager --------------------------------------------------
# This class handles everything using login details 
class DatabaseManager:
    def __init__(self): 
        # Connect to the database using login details 
        self.con = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host="localhost",
    )  
        self.cur = self.con.cursor()   # Cursor = to run SQL queries
    
    def insert_observation(self, report):
        # Save a new weather observation to the database 
        self.cur.execute(""" INSERT INTO observation (city, country, latitude, longitude, temperature, elevation, windspeed, observation_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
        (report.city, report.country, report.latitude, report.longitude, report.temperature, report.elevation, report.windspeed, report.observation_time))
        self.con.commit()
        print("Added:", report.city) # To print confirmation in terminal
    
    def get_all_observations(self):
        # Get all observations from the database 
        self.cur.execute("SELECT * FROM observation;")
        results = self.cur.fetchall()   # Fetch all rows from the database and store them as a list
        return results
    
    def get_observation_by_id(self, id):
        # Get one specific observation from database by ID number 
        self.cur.execute("SELECT * FROM observation WHERE id_number = %s;", (id,))
        result = self.cur.fetchone()    # Fetch only one row from the database
        return result 
    
    def update(self, id, latitude, longitude):
        # Update the cordinates for a specific observation 
        self.cur.execute(""" 
            UPDATE observation 
            SET latitude = %s, longitude = %s 
            WHERE id_number = %s """, (latitude, longitude, id))
        self.con.commit()
        print("Updated id:", id)

    def update_notes(self, id, notes):
        # Save a note for a specific observation by ID number 
        self.cur.execute("UPDATE observation SET notes = %s WHERE id_number = %s", (notes, id))
        self.con.commit()
        print("Updated notes for id:", id)
    
    def delete_observation_by_id(self, id):
        # Delete a specific observation from the database by ID number 
        self.cur.execute("DELETE FROM observation WHERE id_number = %s", (id,))
        self.con.commit()
        print("Deleted id:", id)

