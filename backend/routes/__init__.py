from flask import Flask
from .home_routes import home_bp
from .insights_routes import insights_bp


def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(insights_bp)

