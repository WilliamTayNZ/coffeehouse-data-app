from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'  # Will secure later

    from app.routes import register_routes
    register_routes(app)

    # Delegates route registration to a register_routes(app) function inside routes.py
    # This avoids circular imports and keeps __init__.py clean

    return app

















