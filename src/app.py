# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd
import datetime as dt

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Get Last Date
    last_measurement = session.query(Measurements).order_by(Measurements.date.desc()).first()
    print(last_measurement.date)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    last_date_str = last_measurement.date
    year,month,day = str.split(last_date_str,'-')
    last_date = dt.date(int(year),int(month),int(day)) 

    # Calculate the date one year from the last date in data set.
    first_date = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precip_by_date = (session.query(
                        Measurements.date, 
                        #func.sum(Measurements.prcp)
                        Measurements.prcp
                        )
                    .filter(Measurements.date >= first_date)
                    .order_by(Measurements.date))
    
    session.close()

    prcp_dict = [{'date': x.date, 'prcp': x.prcp} for x in precip_by_date]

    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    return "stations"

@app.route("/api/v1.0/tobs")
def tobs():
    return "tobs"

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_since(start,end=None):
    return "start"

if __name__ == '__main__':
    app.run(debug=True)
