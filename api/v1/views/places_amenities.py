
#!/usr/bin/python3
"""Handle RESTFul API actions."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User


@app_views.route('places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """Return amenities in a place."""
    place = storage.get(Place, place_id)
    if place is None or place == {}:
        return jsonify({"error": "Not found"}), 404
    amenities = storage.all(Amenity)
    if amenities is None:
        return jsonify({"error": "Not found"}), 404
    total = []
    for amenity in amenities.values():
        amenity = amenity.to_dict()
        if amenity['place_id'] == place_id:
            total.append(amenity)
    return jsonify(total)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(place_id, amenity_id):
    """Delete a amenity given amenity id."""
    place = storage.get(Place, place_id)
    if place is None or place == {}:
        return jsonify({"error": "Not found"}), 404
    if amenity_id is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity == {}:
        return jsonify({"error": "Not found"}), 404
    print(place)
    print(amenity)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id):
    """Create a new amenity."""
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
    new = Amenity(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a amenity given amenity id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
