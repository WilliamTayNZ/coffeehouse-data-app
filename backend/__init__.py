from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from backend.routes import register_routes
    register_routes(app)

    # Delegates route registration to a register_routes(app) function inside routes.py
    # This avoids circular imports and keeps __init__.py clean

    return app

















