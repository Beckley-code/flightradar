from . import api
from .. util.flask_util import get_boolean_arg
from .. adsb.db.dbrepository import DBRepository
from .. exceptions import ValidationError
from .. adsb.db.dbmodels import Flight

from flask import current_app as app, Response, request, jsonify, abort

@api.route('/info')
def get_meta_info():
    return jsonify(app.metaInfo.__dict__)

@api.route('/flights')
def get_flights():

    result_set = (Flight.select(Flight.id, Flight.callsign, Flight.modeS, Flight.archived, Flight.last_contact)
                        .order_by(Flight.last_contact.desc()))

    return jsonify([f for f in result_set])    

@api.route('/positions/live')
def get_live_positions():
    return jsonify(app.updater.get_cached_flights())


@api.route('/flight/<flight_id>/positions') 
def get_positions(flight_id):
    try:
        int(flight_id)

        if DBRepository.flight_exists(flight_id):
            positions = DBRepository.get_positions(flight_id)
            return jsonify([[p for p in positions]])
        else:
            abort(404)

    except ValueError:
        raise ValidationError('Invalid flight id format')

@api.route('/positions') 
def get_all_positions():
    archived = get_boolean_arg('archived')
    positions = DBRepository.get_all_positions(archived)
    return jsonify(positions)


@api.after_request
def after_request(response):

    #TODO: look into Flask-Cors (https://flask-cors.readthedocs.io)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')  
    return response    
@api.errorhandler(ValidationError)
def validation_error(e):
    return jsonify({'error': e.args[0]}), 400

@api.app_errorhandler(500)
def handle_generic_err(e):

    message = e.args[0]
    if isinstance(e, NameError):
        message = 'An internal eror occured'

    return jsonify({'error':message}), 500

@api.app_errorhandler(404)
def not_found(e):
    return '', 404