#!/usr/bin/python3
"""Handle RESTFul API actions."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Return reviews in a place."""
    place = storage.get(Place, place_id)
    if place is None or place == {}:
        return jsonify({"error": "Not found"}), 404
    reviews = storage.all(Review)
    if reviews is None:
        return jsonify({"error": "Not found"}), 404
    total = []
    for review in reviews.values():
        review = review.to_dict()
        if review['place_id'] == place_id:
            total.append(review)
    return jsonify(total)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Return a review given review id."""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Delete a review given review id."""
    if review_id is None:
        return jsonify({"error": "Not found"}), 404
    review = storage.get(Review, review_id)
    if review is None or review == {}:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review."""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400
    if not data or data == {}:
        return jsonify({"error": "Not a JSON"}), 400
    place = storage.get(Place, place_id)
    if place is None or place == {}:
        return jsonify({"error": "Not found"}), 404
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None or user == {}:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['place_id'] = place_id
    new = Review(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review given review id."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
