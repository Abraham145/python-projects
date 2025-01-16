from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('expense_tracker.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from expense_tracker.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.config['WTF_CSRF_ENABLED'] = False

    return app
