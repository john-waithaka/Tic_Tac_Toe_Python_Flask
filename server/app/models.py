from werkzeug.security import generate_password_hash, check_password_hash #imports functions for securely hashing and verifying user passwords.
from sqlalchemy import Column, Integer, String, ForeignKey #Imports necessary data types for defining database columns.
from sqlalchemy.orm import relationship #Imports functionality for defining relationships between models.
from . import db  # import the database

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False) #hashed pswd stored

    # Relationships with Game model
    games_as_player_x = relationship('Game', foreign_keys='Game.player_x_id', back_populates='player_x', lazy=True)
    games_as_player_o = relationship('Game', foreign_keys='Game.player_o_id', back_populates='player_o', lazy=True)

    # Stats fields
    wins = Column(Integer, default=0, nullable=False)  #default set to 0
    losses = Column(Integer, default=0, nullable=False)
    draws = Column(Integer, default=0, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The size of the grid for the game (e.g., 3x3, 4x4)
    grid_size = db.Column(db.Integer, nullable=False)
    # Foreign key referencing the User model (Player X or O)
    player_x_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_o_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(db.String(1000), nullable=False, default='')
    # Tracks whose turn it is ('X' for Player X and 'O' for Player O)
    current_turn = db.Column(db.String(1), nullable=False, default='X')  # 'X' for player X and 'O' for player O

    # Relationships with the user model
    player_x = db.relationship('User', foreign_keys=[player_x_id], back_populates='games_as_player_x')
    player_o = db.relationship('User', foreign_keys=[player_o_id], back_populates='games_as_player_o')
