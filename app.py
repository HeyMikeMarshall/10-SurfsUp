from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)









#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    query = session.query(Measurement.station, Measurement.date, Measurement.prcp)
    querydict = {}
    for i in query:
        if i[1] in querydict:
            querydict[i[1]].append(i[2])
        else:
            querydict.update({i[1]:[i[2]]})
    
    return jsonify(querydict)



@app.route("/api/v1.0/stations")
def stations():
    return jsonify(session.query(Station.id, Station.station,\
         Station.name, Station.latitude, Station.longitude, Station.elevation).all())


@app.route("/api/v1.0/tobs")
def tobs():
    lst_dt = dt.datetime.strptime((session.query(Measurement.date).\
                                 order_by(Measurement.date.desc()).first()[0]), '%Y-%m-%d')
    lst_yr = lst_dt - dt.timedelta(days=365)

    query = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= lst_yr).all()
    querydict = {}
    for i in query:
        if i[1] in querydict:
            querydict[i[1]].append(i[2])
        else:
            querydict.update({i[1]:[i[2]]})
    return jsonify(querydict)

@app.route("/api/v1.0/<start>")
def datetoend():
    

    return jsonify()

@app.route("/api/v1.0/<start>/<end>")
def datetodate():
    

    return jsonify()


@app.route("/")
def welcome():
    return (
        f"Welcome to the Surf's Up API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start_date<br>"
        f"/api/v1.0/start_date/<end_date<br>"

    )


if __name__ == "__main__":
    app.run(debug=True)
