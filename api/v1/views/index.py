#!/usr/bin/python3
"""Index view."""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return OK status."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return stats."""
