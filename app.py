# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


MAX_POSS_DATE = dt.date(dt.MAXYEAR, 12, 31)

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
        f"/api/v1.0/tstats/&lt;start&gt;<br/>"
        f"/api/v1.0/tstats/&lt;start&gt;/&lt;end&gt;")


@app.route("/api/v1.0/precipitation/")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query for last 12 months of precipitation
    # Calculate the date one year from the last date in data set.
    last_date_str = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    last_date = dt.date.fromisoformat(last_date_str)
    year_ago = last_date-dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()
    precipitation_list = list(np.ravel(precipitation))
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations/")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Return a JSON list of stations from the dataset.
    stations = session.query(station.station).all()
    all_stations = list(np.ravel(stations))
    session.close()
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs/")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    last_date_str = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    last_date = dt.date.fromisoformat(last_date_str)
    yeartemp = list(np.ravel(session.query(measurement.tobs).filter(measurement.date >= last_date).filter(measurement.station == "USC00519281").all()))
    session.close()
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(yeartemp)


@app.route("/api/v1.0/tstats/<start>/")
@app.route("/api/v1.0/tstats/<start>/<end>/")
def tstats(start, end=MAX_POSS_DATE):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    temps= list(np.ravel(session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()))
    session.close()
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)