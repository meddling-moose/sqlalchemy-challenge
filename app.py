# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")

    session = Session(engine)

    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.date(int(recent[0:4]), int(recent[5:7]), int(recent[8:10])) - dt.timedelta(days=365) #'2016-08-23'

    data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(one_year_ago, recent)).\
        order_by(Measurement.date).all()

    results = {date: prcp for date, prcp in data}

    session.close()
    return jsonify(precipitation=results)

@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'Station' page...")
    session = Session(engine)

    results = session.query(Station.station).all()
    stations = list(np.ravel(results))

    session.close()
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date.between('2016-08-18', '2017-08-18')).all()

    temperatures = list(np.ravel(results))

    return jsonify(temperatures=temperatures)

@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start, '%m%d%Y')

    print(f'date: {start}')

    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    stats = list(np.ravel(results))

    return jsonify(minmaxavg=stats)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    start = dt.datetime.strptime(start, '%m%d%Y')
    end = dt.datetime.strptime(end, '%m%d%Y')

    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).\
        filter(Measurement.date.between(start, end)).all()

    stats = list(np.ravel(results))

    return jsonify(minmaxavg=stats)

if __name__ == "__main__":
    app.run(debug=True)