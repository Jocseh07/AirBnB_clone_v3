#!/usr/bin/python3
"""Index view."""

from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return OK status."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return stats."""
    dictionary = {}
    for obj in classes.values():
        dictionary[obj.__name__] = storage.count(obj.__name__)
    return jsonify(dictionary)
