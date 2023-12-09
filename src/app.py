# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify






#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return "ok"

@app.route("/api/v1.0/precipitation")
def precip():
    return "prcp"

@app.route("api/v1.0/stations")
def stations():
    return "stations"

@app.route("api/v1.0/tobs")
def tobs():
    return "tobs"

@app.route("api/v1.0/<start>")
def temp_stats(start):
    return "start"

@app.route("api/v1.0/<start>/<end>")
def temp_stats(start,end):
    return "start/end"