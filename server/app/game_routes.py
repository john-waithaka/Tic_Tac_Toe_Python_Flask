from flask import Blueprint, request, jsonify
from .models import Game, User  # Import Game and User models
from . import db  # Import the database instance
from .utils import make_move, check_winner, check_draw, create_game, ai_move, handle_game_state_update  # Utility functions for game logic
import json
from threading import Lock  # Import threading for locking mechanisms to handle concurrency

# Define a Blueprint for the game-related routes
game_blueprint = Blueprint('game', __name__)

# Lock for handling concurrent moves - Prevents multiple moves being made simultaneously in the same game.
game_move_lock = Lock()

# Route for creating a new game
@game_blueprint.route('/game', methods=['POST'])
def create_game_route():
    data = request.get_json()  # Parse the incoming request's JSON data
    
    # Check if required fields are provided in the request
    if not data or 'grid_size' not in data or 'player_x' not in data:
        return jsonify({"message": "Missing fields"}), 400

    grid_size = data['grid_size']
    
    # Validate the grid size (must be at least 3x3)
    if grid_size < 3:
        return jsonify({"message": "Invalid grid size"}), 400

    # Fetch players from the database
    player_x = User.query.get(data['player_x'])
    player_o = User.query.get(data.get('player_o'))

    # Validate Player X
    if not player_x:
        return jsonify({"message": "Player X not found"}), 404
    
    # Validate Player O if provided
    if data.get('player_o') and not player_o:
        return jsonify({"message": "Player O not found"}), 404

    # Create a new game with the provided player IDs and grid size
    new_game = create_game(player_x_id=player_x.id, player_o_id=player_o.id if player_o else None, grid_size=grid_size)
    
    try:
        # Add and commit the new game to the database
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            "game_id": new_game.id,
            "player_x": player_x.username,
            "player_o": player_o.username if player_o else "AI"  # Use AI if no Player O
        }), 201
    except Exception as e:
        # Rollback the transaction in case of any errors
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Route for making a move in an existing game
@game_blueprint.route('/move', methods=['POST'])
def make_move_route():
    data = request.get_json()  # Parse the incoming JSON data
    
    # Validate required fields
    if not data or 'game_id' not in data or 'player' not in data or 'position' not in data:
        return jsonify({"message": "Missing fields"}), 400

    # Fetch the game from the database by its ID
    game = Game.query.get(data['game_id'])
    if not game:
        return jsonify({"message": "Game not found"}), 404

    try:
        # Load the current game state (as a list) from the database
        game_state = json.loads(game.state) if game.state else []
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid game state"}), 500

    # Validate that the position is within the game board boundaries
    position = data['position']
    if position < 0 or position >= game.grid_size * game.grid_size:
        return jsonify({"error": "Position out of bounds"}), 400

    # Determine if the player is Player X or Player O
    if data['player'] == game.player_x_id:
        player_symbol = 'X'
    elif data['player'] == game.player_o_id:
        player_symbol = 'O'
    else:
        return jsonify({"error": "Invalid player"}), 400

    with game_move_lock:  # Use the lock to prevent simultaneous moves
        # Make the move and update the game state
        updated_state, error = make_move(game_state, player_symbol, position, game.grid_size)
        if error:
            return jsonify({"error": error}), 400

        # Check if there's a winner after the move
        winner = check_winner(updated_state, game.grid_size)
        if winner:
            # Update player stats based on the winner
            if winner == 'X':
                game.player_x.wins += 1
                if game.player_o:
                    game.player_o.losses += 1
            elif winner == 'O':
                game.player_o.wins += 1
                if game.player_x:
                    game.player_x.losses += 1
            
            db.session.commit()

            # Return the result and updated game state
            return jsonify({
                "winner": winner,
                "player_x": game.player_x.username,
                "player_o": game.player_o.username if game.player_o else "AI",
                "game_state": updated_state
            })

        # Check if the game is a draw
        if check_draw(updated_state):
            # Update player stats for a draw
            if game.player_x:
                game.player_x.draws += 1
            if game.player_o:
                game.player_o.draws += 1

            db.session.commit()

            # Return the result and updated game state
            return jsonify({
                "result": "draw",
                "player_x": game.player_x.username,
                "player_o": game.player_o.username if game.player_o else "AI",
                "game_state": updated_state
            })

        # No winner or draw yet, so update the game state in the database
        game = handle_game_state_update(game, updated_state)

        # If AI is playing as Player O, let AI make its move after Player X
        if game.player_o_id is None and player_symbol == 'X':
            ai_move_position = ai_move(updated_state, game.grid_size)
            updated_state, error = make_move(updated_state, 'O', ai_move_position, game.grid_size)
            if error:
                return jsonify({"error": error}), 400

            # Check if AI won after its move
            if check_winner(updated_state, game.grid_size):
                game.player_x.losses += 1
                db.session.commit()

                return jsonify({
                    "winner": "O",
                    "player_x": game.player_x.username,
                    "player_o": "AI",
                    "game_state": updated_state
                })
            
            # Check for a draw after AI's move
            if check_draw(updated_state):
                game.player_x.draws += 1
                db.session.commit()

                return jsonify({
                    "result": "draw",
                    "player_x": game.player_x.username,
                    "player_o": "AI",
                    "game_state": updated_state
                })

            # Update the game state after AI's move
            game = handle_game_state_update(game, updated_state)

    # Return the updated game state and player details
    return jsonify({
        "game_state": updated_state,
        "player_x": game.player_x.username,
        "player_o": game.player_o.username if game.player_o else "AI"
    }), 200

# Route for retrieving the details of an existing game by its id
@game_blueprint.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    # Fetch the game by its ID
    game = Game.query.get(game_id)
    if game:
        # Return the game's grid size, current state, and player details
        return jsonify({
            "grid_size": game.grid_size,
            "game_state": json.loads(game.state) if game.state else [],
            "player_x": game.player_x.username,
            "player_o": game.player_o.username if game.player_o else "AI"
        }), 200
    
    # If the game is not found, return an error
    return jsonify({"error": "Game not found"}), 404
