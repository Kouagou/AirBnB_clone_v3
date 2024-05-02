#!/usr/bin/python3
"""
Handle all default RESTFull API actions for Review class.
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_by_place(place_id):
    """ Retrieve the list of all Review objects of a Place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'])
def one_review(review_id):
    """ Retrieve a Review object. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Delete a Review object. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a Review. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    req = request.get_json()
    review = Review(**req)
    review.place_id = place_id
    review.user_id = req['user_id']
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    """ Update a Review. """
    if not request.get_json():
        abort(400, description="Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
