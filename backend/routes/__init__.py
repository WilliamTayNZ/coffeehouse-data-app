from flask import Flask
from .clean_routes import clean_bp
from .insights_routes import insights_bp


def register_routes(app):
    app.register_blueprint(clean_bp)
    app.register_blueprint(insights_bp)

