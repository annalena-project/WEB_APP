
from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Weather Tracker Homepage 🌞🌧️❄️"

@app.route("/ingest", methods = ["POST"])
def create_observation():
    return "Create a new weather observation"

@app.route("/observations", methods = ["GET"])
def observations():
    return "Retrieve all the weather observations"

@app.route("/observations/<int:observation_id>", methods = ["GET"])
def observation(observation_id):
    return f"Retrieve the weather observation with ID: {observation_id}"

@app.route("/observations/<int:observation_id>", methods = ["PUT"])
def edit_observation(observation_id):
    return f"Update the weather observation with ID: {observation_id}"

@app.route("/observations/<int:observation_id>", methods = ["DELETE"])
def delete_observation(observation_id):
    return f"Delete the weather observation with ID: {observation_id}"

if __name__ == "__main__":
    app.run(debug=True)

