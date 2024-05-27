#!/usr/bin/python3
"""Flask app."""

from os import getenv

from flask import Flask

from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close storage."""
    storage.close()


if __name__ == "__main__":
    """Main function."""
    HBNB_API_HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', default='5000')
    app.run(host=HBNB_API_HOST, port=int(HBNB_API_PORT), threaded=True)
