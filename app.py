# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///hawaii.sqlite')

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

routes_dict = {'home': '/',
               'precipitation': '/api/v1.0/precipitation',
               'stations': '/api/v1.0/stations',
               'tobs': '/api/v1.0/tobs',
               'start': '/api/v1.0/<start>',
               'startend': '/api/v1.0/<start>/<end>'}

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

    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.date(int(recent[0:4]), int(recent[5:7]), int(recent[8:10])) - dt.timedelta(days=365) #'2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(one_year_ago, recent)).all()

    # Sort the dataframe by date
    df = df.sort_values('date')

    return "Welcome to my 'Precipitation' page"

@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'Station' page...")
    return "Welcome to my 'Station' page"

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")
    return "Welcome to my 'Tobs' page"

@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'Start' page...")
    return "Welcome to my 'Start' page"

@app.route("/api/v1.0/<start>/<end>")
def startend():
    print("Server received request for 'Start and End' page...")
    return "Welcome to my 'Start and End' page"

if __name__ == "__main__":
    app.run(debug=True)