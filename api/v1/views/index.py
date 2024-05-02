#!/usr/bin/python3
"""
Initialization
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def get_status():
    """ Returns a JSON: "status": "OK" """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_statistics():
    """ Retrieves the number of each objects by type. """
    models_ = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states"
    }
    response = {}

    for k, v in models_.items():
        response[v] = storage.count(k)

    return jsonify(response)
