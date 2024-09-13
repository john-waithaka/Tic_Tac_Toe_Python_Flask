#creating the Flask app, initializing database and migration components, and registering necessary blueprints.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Create a migration engine for managing database schema changes
migrate = Migrate()

def create_app():
    """
    Creates the Flask application and initializes its components.

    Returns:
        The Flask application instance.
    """

    # Create a Flask application instance
    app = Flask(__name__)

    # Load configuration settings from the `config.Config` module
    app.config.from_object('config.Config')

    # Initialize the SQLAlchemy database with the application
    db.init_app(app)

    # Initialize the migration engine with the application and database
    migrate.init_app(app, db)

    # Register blueprints for different routes
    from .user_routes import user_blueprint
    from .game_routes import game_blueprint
    from .user_games_routes import user_games_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(user_games_blueprint)

    return app