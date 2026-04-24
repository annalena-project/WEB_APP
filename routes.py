
# This file runs the web app and handles all the page routes

# Import what we need from Flask to build the app
from flask import Flask, render_template, redirect,  url_for, abort, request
# Used to call the weather API
import requests

# Import database functions and the WeatherReport object
from populate import DatabaseManager, WeatherReport
# Create connection to the database
db = DatabaseManager() 

# Create the Flask app
app = Flask(__name__)  
#------------------- Home Page ----------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

#----------------- Create New Observation  ----------------------------------------------------
@app.route("/ingest", methods = ["POST"])
def create_observation():
    # Get city and country from the form on the home page
    city = request.form.get("city")
    country = request.form.get("country")

    # Search for the city coordinates using Open-Meteo
    search_query = f"{city}, {country}"
    geo_response = requests.get("https://geocoding-api.open-meteo.com/v1/search",
    params={"name": search_query, "count": 1}).json()

     # If the city was not found, show a 404 error
    if "results" not in geo_response:
        abort(404) 

    geo = geo_response["results"][0]
    latitude = geo["latitude"]
    longitude = geo["longitude"]

    # Use the coordinates to get live weather data
    weather = requests.get("https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "current_weather": "true"}).json()["current_weather"]

    # Save everything to the database
    report = WeatherReport(city, country, latitude, longitude, weather["temperature"], 0, weather["windspeed"], weather["time"])
    db.insert_observation(report)

    # Show result on home page
    return render_template("index.html", weather=report)

#------------------- Show All Observations ----------------------------------------------------------
@app.route("/observations", methods = ["GET"])
def observations():
    data = db.get_all_observations()
    return render_template("observations.html", data=data)

#------------------- Show One Observation -----------------------------------------------------------
@app.route("/observations/<int:observation_id>", methods=["GET"])
def show_observation(observation_id):
    # Look up one specific observation by ID number 
    data = db.get_observation_by_id(observation_id)
    # Non-existent ID number, show a 404 error
    if not data:
        abort(404)
    return render_template("show_observation.html", observation=data)

#------------------------ Edit / Add Note ----------------------------------------------------
@app.route("/observations/<int:observation_id>/edit", methods=["GET", "POST"])
def edit_observation(observation_id):
    data = db.get_observation_by_id(observation_id)
    if not data:
        abort(404)
    
    if request.method == "POST":
        # Save the note that was typed in the form  
        notes = request.form.get("notes")
        db.update_notes(observation_id, notes)
        return redirect(url_for("show_observation", observation_id=observation_id))
    
    # Show the edit form 
    return render_template("edit_observation.html", observation=data)

#------------------------ Delete Observation ----------------------------------------------
@app.route("/observations/<int:id>/delete", methods=["POST"])
def delete_observation(id):
    db.delete_observation_by_id(id)
    return redirect(url_for("observations"))

#------------------------ Start the App ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

