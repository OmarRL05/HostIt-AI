from re import A
from flask import Flask
from flask_cors import CORS
from app.config import Config
from .extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all routes
    # Allows Vue to talk to Flask without CORS errors
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # Change * to Vue app's URL when deployed

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models 

    # Register blueprints (routes)
    from .routes.base import base_bp
    app.register_blueprint(base_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    return app