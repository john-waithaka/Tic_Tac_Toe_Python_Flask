from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from .user_routes import user_blueprint
    from .game_routes import game_blueprint
    from .user_games_routes import user_games_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(user_games_blueprint)

    return app

