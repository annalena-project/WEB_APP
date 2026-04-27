
# This file runs the web app and handles all the page routes

# Import what needed from Flask to build the app
from flask import Flask, render_template, redirect,  url_for, abort, request
import requests # Used to call the weather API

# Import DatabaseManager and WeatherReport from database_manager.py
from database_manager import DatabaseManager, WeatherReport

# Create connection to the database
db = DatabaseManager() 

# Create the Flask app
app = Flask(__name__)  

#------------------- Home Page ----------------------------------------------------------------
# Shows the start page (index.html)
@app.route("/")
def home():
    return render_template("index.html")

#----------------- Create New Observation  ----------------------------------------------------
# POST /ingest – gets city and country from the search box, fetches live weather and saves it to the database
@app.route("/ingest", methods = ["POST"])
def create_observation():
    # Get city and country that user typed in on home page (index.html)
    city = request.form.get("city")
    country = request.form.get("country")

    # Use the geocoding API to convert the city name into latitude and longitude
    search_query = f"{city}, {country}"
    geo_response = requests.get("https://geocoding-api.open-meteo.com/v1/search",
    params={"name": search_query, "count": 1}).json()

     # If the city was not found, show a 404 error
    if "results" not in geo_response:
        abort(404) 

    # The API returns a list of results, take the first result [0] and save the coordinates (latitude and longitude)
    geo = geo_response["results"][0]
    latitude = geo["latitude"]
    longitude = geo["longitude"]

    # Use the coordinates to call weather API and get live weather data
    weather = requests.get("https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "current_weather": "true"}).json()["current_weather"]

    # Create a WeatherReport object and save it to database 
    report = WeatherReport(city, country, latitude, longitude, weather["temperature"], 0, weather["windspeed"], weather["time"])
    db.insert_observation(report)

    # Send back weather data snd show result on home page (index.html)
    return render_template("index.html", weather=report)

#------------------- Show All Observations ----------------------------------------------------------
# Get /observations - get all observations from the database and shows on observation.html
@app.route("/observations", methods = ["GET"])
def observations():
    data = db.get_all_observations()
    return render_template("observations.html", data=data)

#------------------- Show One Observation -----------------------------------------------------------
# GET /observations/<id> – fetches one specific observation by ID number and shows it in show_observation.html
@app.route("/observations/<int:observation_id>", methods=["GET"])
def show_observation(observation_id):
    # Look up one specific observation by ID number 
    data = db.get_observation_by_id(observation_id)
    # If ID number dont exist, show a 404 error
    if not data:
        abort(404)
    return render_template("show_observation.html", observation=data)

#------------------------ Edit / Add Note ----------------------------------------------------
# GET /observations/<id>/edit – shows the observation and lets the user write or change a note
# POST /observations/<id>/edit – saves the note to the database
@app.route("/observations/<int:observation_id>/edit", methods=["GET", "POST"])
def edit_observation(observation_id):
    data = db.get_observation_by_id(observation_id)

    # If ID number dont exist, show a 404 error
    if not data:
        abort(404)

    if request.method == "POST":
        # Get the note that was typed or edit 
        notes = request.form.get("notes")
        # Save note to database
        db.update_notes(observation_id, notes)
        # After saving the note, send the user back to the observations page (observations.html)
        return redirect(url_for("observations"))
    # If not saving, stay on the same page and show the observation
    else:
        return render_template("show_observation.html", observation=data)
    

#------------------------ Delete Observation ----------------------------------------------
# POST /observations/<id>/delete – deletes the observation from the database 
@app.route("/observations/<int:id>/delete", methods=["POST"])
def delete_observation(id):
    db.delete_observation_by_id(id)
    return redirect(url_for("observations"))

#------------------------ Start the App ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

