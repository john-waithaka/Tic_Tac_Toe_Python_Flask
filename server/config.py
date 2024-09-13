#The Config class holds configuration settings for the Flask app

import os

class Config:
    # The SECRET_KEY is used by Flask for securely signing sessions and other security-related needs.
    # It tries to get the value from the environment variable 'SECRET_KEY'.
    # If 'SECRET_KEY' is not set in the environment, it defaults to 'dev_secret_key'.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    
    # SQLALCHEMY_DATABASE_URI defines the database connection string for SQLAlchemy (the ORM).
    # It first tries to get the value from the environment variable 'DATABASE_URL'.
    # If 'DATABASE_URL' is not set, it defaults to a local SQLite database 'tictactoe.db'.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tictactoe.db'
    
    # Disables the SQLAlchemy feature that tracks modifications to objects and emits signals.
    # This can reduce overhead as it is not usually needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
