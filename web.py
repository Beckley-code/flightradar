import json, time

from flask import Flask
from flask import Response
from flask import render_template
from flask import jsonify

from adsb.config import Config
from adsb.basestationdb import BaseStationDB

from updateThread import UpdaterThread

app = Flask(__name__)

adsb_config = Config()
adsb_config.from_file('config.json')
bs_db = BaseStationDB(adsb_config.data_folder + "BaseStation.sqb")        

updater = UpdaterThread(adsb_config)
updater.start()

@app.route("/api")
def rest_api():
    response = []

    for icao24, tmstmp in updater.aircraft.items():
        aircraft = bs_db.query_aircraft(icao24)

        if aircraft:
            response.append((aircraft.__dict__, time.ctime(tmstmp)))

    return Response(json.dumps(response), mimetype='application/json')

@app.route("/") 
def index():

    response = []

    #for icao24, tmstmp in updater.aircraft.items():
    for entry in updater.get_active_entries():

        aircraft = bs_db.query_aircraft(entry[0])

        if aircraft:
            response.append((aircraft.__dict__, time.ctime(entry[1].last_seen)))

        response.sort(key=lambda tup: tup[1],reverse=True)

    return render_template('aircraft.html', airplanes=response)

@app.route("/pos/<icao24>") 
def get_positions(icao24):

    entries = updater.get_entry(icao24)

    if entries:
        return Response(json.dumps(entries.pos), mimetype='application/json')
    else:
        return "Not found", 404


@app.route("/map/<icao24>") 
def get_map(icao24):
    return render_template('map.html', icao24=icao24)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
