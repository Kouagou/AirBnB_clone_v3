#!/usr/bin/python3
"""
Handle all default RESTFull API actions for the link
between Place objects and Amenity objects.
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities_by_place(place_id):
    """ Retrieve the list of all Amenity objects of a Place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """ Delete a Amenity object to a Place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify({amenity.to_dict()}), 200)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify({amenity.to_dict()}), 201)
