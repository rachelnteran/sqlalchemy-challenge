# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return("<h1> Welcome to our climate app! </h1>"
            f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>")
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query for last 12 months of precipitation
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()
    precipitation_list = list(np.ravel(precipitation))
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    session.close()
    #Return a JSON list of stations from the dataset.
    stations = session.query(station.station).all()
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    session.close()
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    yeartemp = list(np.ravel(session.query(measurement.tobs).filter(measurement.date >= dt.date(2016, 8, 23)).filter(measurement.station == "USC00519281").all()))
    #Return a JSON list of temperature observations for the previous year.
    return yeartemp

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    session.close()
    return()

@app.route("/api/v1.0/<start>/<end>")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    session.close()
    return()

if __name__ == "__main__":
    app.run(debug=True)