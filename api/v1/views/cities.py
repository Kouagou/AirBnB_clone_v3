#!/usr/bin/python3
"""
Handle all default RESTFull API actions for City class.
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities_by_state(state_id):
    """ Retrieve the list of all City objects of a State. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def one_city(city_id):
    """ Retrieve a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Delete a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a City. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    req = request.get_json()
    city = City(**req)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id):
    """ Update a City. """
    if not request.get_json():
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
