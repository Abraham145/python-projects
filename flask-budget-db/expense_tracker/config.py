import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'a_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data.db')  # Fallback to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
