import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'a_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///life_planner.db')  # Updated to new database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
