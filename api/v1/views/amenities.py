#!/usr/bin/python3
"""Handle RESTFul API actions."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Return a amenity."""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Return a amenity given amenity id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete a amenity given amenity id."""
    if amenity_id is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new = Amenity(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a amenity given amenity id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
