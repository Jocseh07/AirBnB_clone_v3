#!/usr/bin/python3
"""Handle RESTFul API actions."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Return places in a city."""
    city = storage.get(City, city_id)
    if city is None or city == {}:
        return jsonify({"error": "Not found"}), 404
    places = storage.all(Place)
    if places is None:
        return jsonify({"error": "Not found"}), 404
    total = []
    for place in places.values():
        place = place.to_dict()
        if place['city_id'] == city_id:
            total.append(place)
    return jsonify(total)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return a place given place id."""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Delete a place given place id."""
    if place_id is None:
        return jsonify({"error": "Not found"}), 404
    place = storage.get(Place, place_id)
    if place is None or place == {}:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place."""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400
    if not data or data == {}:
        return jsonify({"error": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if city is None or city == {}:
        return jsonify({"error": "Not found"}), 404
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None or user == {}:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['city_id'] = city_id
    new = Place(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place given place id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
