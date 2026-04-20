import psycopg2                    # To connect to PostgreSQL database
import os                          # Get hidden values (like password)
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("password")
database = os.getenv("DATABASE_URL") 

print(database) 

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

class DatabaseManager:
    def __init__(self): 
        self.con = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host="localhost",
    )  
        self.cur = self.con.cursor()   # Cursor = to run SQL queries
    
    def insert_observation(self, report):
        self.cur.execute(""" INSERT INTO observation (city, country, latitude, longitude, temperature, elevation, windspeed)
        VALUES (%s, %s, %s, %s, %s, %s, %s) """,
        (report.city, report.country, report.latitude, report.longitude, report.temperature, report.elevation, report.windspeed))
    # Insert data into database table + %s are placeholders for values
        self.con.commit()
        print("Added:", report.city) # To print confirmation in terminal
    
    def get_all_observations(self):
        self.cur.execute("SELECT * FROM observation;")
        results = self.cur.fetchall()
        return results
    
    def get_observation_by_id(self, id):
        self.cur.execute("SELECT * FROM observation WHERE id_number = %s;", (id,))
        result = self.cur.fetchone()
        return result 
    
    def update(self, id, latitude, longitude):
        self.cur.execute(""" 
            UPDATE observation 
            SET latitude = %s, longitude = %s 
            WHERE id_number = %s """, (latitude, longitude, id))
        self.con.commit()
        print("Updated id:", id)
    
    def delete_observation_by_id(self, id):
        self.cur.execute("DELETE FROM observation WHERE id_number = %s", (id,))
        self.con.commit()
        print("Deleted id:", id)

