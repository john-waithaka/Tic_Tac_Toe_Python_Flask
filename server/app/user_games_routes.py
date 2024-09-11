from flask import Blueprint, jsonify
from .models import Game
from .utils import check_winner
import json

user_games_blueprint = Blueprint('user_games', __name__)

@user_games_blueprint.route('/user/games', methods=['GET'])
def user_games():
    games = Game.query.all()  # Adjust this if you want to filter by a specific user

    return jsonify([{
        "game_id": game.id,
        "player_x": game.player_x_id,
        "player_o": game.player_o_id,
        "grid_size": game.grid_size,
        "status": "completed" if check_winner(json.loads(game.state) if game.state else [], game.grid_size) else "ongoing"
    } for game in games]), 200
