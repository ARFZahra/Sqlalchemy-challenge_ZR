# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
#Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Start at the homepage.List all the available routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate APP!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date_tobs<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation Data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        all()

    session.close()

#Convert the query results to a dictionary by using date as the key and prcp as the value.

# Convert the list to Dictionary
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)
#Return the JSON representation of your dictionary.
    return jsonify(all_prcp)


#Query Sation list and return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Query for all the stations
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations = [{"station": station, "name": name} for station, name in results]

    return jsonify(stations)


#Query the dates and temperature observations of the most-active station for the previous year of data and return a JSON list of temperature observation
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.

    results = session.query(Measurement.date,  Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

# Convert the list to Dictionary
    all_tobs = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_date_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_date_tobs.append(start_date_tobs_dict)
    
    if start_date_tobs:
        return jsonify(start_date_tobs)
    else:
        return jsonify({"error": "No data found, data format should be YYYY-MM-DD"}), 404

#For a specified start date and end date, calculate MIN, AVG, and MAX for the dates from the start date to the end date.
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    # Query all tobs
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(
        Measurement.date >= start_date
    ).filter(
        Measurement.date <= end_date
    ).all()
    
    session.close()
  
    # Create a dictionary from data and append to a list of start_end_date_tobs

    start_end_tobs = []
    
    for min_temp, avg_temp, max_temp in results:
        start_end_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_end_tobs.append(start_end_tobs_dict)
    
    if start_end_tobs:
        return jsonify(start_end_tobs)
    else:
        return jsonify({"error": "No data found, data format should be YYYY-MM-DD"}), 404

if __name__ == "__main__":
    app.run(debug=True)

