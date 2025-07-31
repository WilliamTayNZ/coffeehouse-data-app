from flask import Flask
from .clean_routes import clean_bp
from .cleaned_sheets_routes import cleaned_sheets_bp
from .insights_routes import insights_bp


def register_routes(app):
    app.register_blueprint(clean_bp)
    app.register_blueprint(cleaned_sheets_bp)
    app.register_blueprint(insights_bp)