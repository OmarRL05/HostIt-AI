from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all routes
    # Allows Vue to talk to Flask without CORS errors
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Change * to Vue app's URL when deployed

    # Register blueprints (routes)
    from .routes.base import base_bp
    app.register_blueprint(base_bp)

    return app