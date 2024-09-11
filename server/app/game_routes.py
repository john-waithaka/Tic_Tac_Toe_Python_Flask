from flask import Blueprint, request, jsonify
from .models import Game, User
from . import db
from .utils import make_move, check_winner, check_draw, create_game, ai_move, handle_game_state_update
import json
from threading import Lock

game_blueprint = Blueprint('game', __name__)

# Lock for handling concurrent moves
game_move_lock = Lock()

@game_blueprint.route('/game', methods=['POST'])
def create_game_route():
    data = request.get_json()
    
    if not data or 'grid_size' not in data or 'player_x' not in data:
        return jsonify({"message": "Missing fields"}), 400

    grid_size = data['grid_size']
    if grid_size < 3:
        return jsonify({"message": "Invalid grid size"}), 400

    player_x = User.query.get(data['player_x'])
    player_o = User.query.get(data.get('player_o'))

    if not player_x:
        return jsonify({"message": "Player X not found"}), 404
    if data.get('player_o') and not player_o:
        return jsonify({"message": "Player O not found"}), 404

    new_game = create_game(player_x_id=player_x.id, player_o_id=player_o.id if player_o else None, grid_size=grid_size)
    
    try:
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            "game_id": new_game.id,
            "player_x": player_x.username,
            "player_o": player_o.username if player_o else "AI"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@game_blueprint.route('/move', methods=['POST'])
def make_move_route():
    data = request.get_json()
    if not data or 'game_id' not in data or 'player' not in data or 'position' not in data:
        return jsonify({"message": "Missing fields"}), 400

    game = Game.query.get(data['game_id'])
    if not game:
        return jsonify({"message": "Game not found"}), 404

    try:
        game_state = json.loads(game.state) if game.state else []
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid game state"}), 500

    position = data['position']
    if position < 0 or position >= game.grid_size * game.grid_size:
        return jsonify({"error": "Position out of bounds"}), 400

    # Check if the player is player_x or player_o and use the corresponding symbol
    if data['player'] == game.player_x_id:
        player_symbol = 'X'
    elif data['player'] == game.player_o_id:
        player_symbol = 'O'
    else:
        return jsonify({"error": "Invalid player"}), 400

    with game_move_lock:
        updated_state, error = make_move(game_state, player_symbol, position, game.grid_size)
        if error:
            return jsonify({"error": error}), 400

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

            return jsonify({
                "winner": winner,
                "player_x": game.player_x.username,
                "player_o": game.player_o.username if game.player_o else "AI",
                "game_state": updated_state
            })

        if check_draw(updated_state):
            # Update player stats for a draw
            if game.player_x:
                game.player_x.draws += 1
            if game.player_o:
                game.player_o.draws += 1

            db.session.commit()

            return jsonify({
                "result": "draw",
                "player_x": game.player_x.username,
                "player_o": game.player_o.username if game.player_o else "AI",
                "game_state": updated_state
            })

        # Update game state
        game = handle_game_state_update(game, updated_state)

        # If AI is playing as O and X made the move, AI makes its move
        if game.player_o_id is None and player_symbol == 'X':
            ai_move_position = ai_move(updated_state, game.grid_size)
            updated_state, error = make_move(updated_state, 'O', ai_move_position, game.grid_size)
            if error:
                return jsonify({"error": error}), 400

            if check_winner(updated_state, game.grid_size):
                # Update player stats if AI wins
                game.player_x.losses += 1
                db.session.commit()

                return jsonify({
                    "winner": "O",
                    "player_x": game.player_x.username,
                    "player_o": "AI",
                    "game_state": updated_state
                })
            
            if check_draw(updated_state):
                # Update player stats for a draw
                game.player_x.draws += 1
                db.session.commit()

                return jsonify({
                    "result": "draw",
                    "player_x": game.player_x.username,
                    "player_o": "AI",
                    "game_state": updated_state
                })

            game = handle_game_state_update(game, updated_state)

    return jsonify({
        "game_state": updated_state,
        "player_x": game.player_x.username,
        "player_o": game.player_o.username if game.player_o else "AI"
    }), 200

@game_blueprint.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game:
        return jsonify({
            "grid_size": game.grid_size,
            "game_state": json.loads(game.state) if game.state else [],
            "player_x": game.player_x.username,
            "player_o": game.player_o.username if game.player_o else "AI"
        }), 200
    return jsonify({"error": "Game not found"}), 404
