#!/usr/bin/python3
"""Handle RESTFul API actions."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Return a state."""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return a state given state id."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@ app_views.route('/states/<state_id>', methods=['DELETE'],
                  strict_slashes=False)
def del_state(state_id):
    """Delete a state given state id."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@ app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state."""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new = State(**request.get_json())
    new.save()
    return jsonify(new.to_dict()), 201


@ app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state given state id."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
