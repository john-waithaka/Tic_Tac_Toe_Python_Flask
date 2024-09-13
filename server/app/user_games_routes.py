#This code defines a Blueprint for retrieving a user's game list. 

from flask import Blueprint, jsonify
from .models import Game
from .utils import check_winner
import json

user_games_blueprint = Blueprint('user_games', __name__)


@user_games_blueprint.route('/user/games', methods=['GET'])
def user_games():
    """
    Retrieves a list of all games (can be adjusted to filter by user).

    Returns:
        A JSON response containing information about all games.
    """
    # Get all games (modify this to filter by specific user)
    games = Game.query.all()

    # Prepare game information for JSON response
    game_data = [{
        "game_id": game.id,
        "player_x": game.player_x_id,  # Player X ID
        "player_o": game.player_o_id,  # Player O ID (can be null for AI)
        "grid_size": game.grid_size,
        "status": "completed" if check_winner(json.loads(game.state) if game.state else [], game.grid_size) else "ongoing"
    } for game in games]

    return jsonify(game_data), 200