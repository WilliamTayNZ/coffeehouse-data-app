import os
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from backend.routes import register_routes
    register_routes(app)

    # Delegates route registration to a register_routes(app) function inside routes.py
    # This avoids circular imports and keeps __init__.py clean

    return app

















