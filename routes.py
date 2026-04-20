
from flask import Flask

from populate import DatabaseManager
db = DatabaseManager()

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Weather Tracker Homepage 🌞🌧️❄️"

@app.route("/ingest", methods = ["POST"])
def create_observation():
    return "Create a new weather observation"

@app.route("/observations", methods = ["GET"])
def observations():
    data = db.get_all_observations()
    return str(data)

@app.route("/observations/<int:observation_id>", methods = ["GET"])
def observation(observation_id):
    data = db.get_observation_by_id(observation_id)
    return str(data)

@app.route("/observations/<int:observation_id>", methods = ["PUT"])
def edit_observation(observation_id):
    db.update(observation_id, 59.33, 18.06)
    return f"Updated ID: {observation_id}"    

@app.route("/observations/<int:observation_id>", methods = ["DELETE"])
def delete_observation(observation_id):
    db.delete_observation_by_id(observation_id)
    return f"Deleted ID: {observation_id}"
    

if __name__ == "__main__":
    app.run(debug=True)

