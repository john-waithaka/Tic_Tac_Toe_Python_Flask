"""Utils helps with Validating and making moves, Checking for winners and draws, Creating new games, crating helper functions, 
Integrating with an AI player using the TicTacToeAI class and -Updating the game state and committing changes to the database.

"""

import json
from . import db
from .models import Game
from .ai import TicTacToeAI

def make_move(game_state, player, position, grid_size):
    if position < 0 or position >= grid_size * grid_size:
        return None, "Position out of bounds"
    
    ## Check if the chosen position is empty ('').
    # If it is, the move is valid, and the player's symbol is placed in that position.
    if game_state[position] == '':
        game_state[position] = player
        return game_state, None
    return None, "Invalid move"



def check_winner(game_state, grid_size):
    if not game_state or len(game_state) != grid_size * grid_size:
        # Invalid state or incomplete board
        return None

    # Check rows and columns
    for i in range(grid_size):
        # Row check
        if game_state[i * grid_size:(i + 1) * grid_size].count(game_state[i * grid_size]) == grid_size and game_state[i * grid_size] != "":
            return game_state[i * grid_size]
        # Column check
        col = [game_state[i + j * grid_size] for j in range(grid_size)]
        if col.count(col[0]) == grid_size and col[0] != "":
            return col[0]

    # Check diagonals - (from top-left to bottom-right)
    diag1 = [game_state[i * (grid_size + 1)] for i in range(grid_size)]
    if diag1.count(diag1[0]) == grid_size and diag1[0] != "":
        return diag1[0]
    # Check the second diagonal (from top-right to bottom-left)
    diag2 = [game_state[(i + 1) * (grid_size - 1)] for i in range(grid_size)]
    if diag2.count(diag2[0]) == grid_size and diag2[0] != "":
        return diag2[0]

    return None

def check_draw(game_state):
    return all(cell != '' for cell in game_state)


#helper functions help with modularity- small chunks better meaning, reusability, maintainability, readability

# New helper function to create a game
def create_game(player_x_id, player_o_id=None, grid_size=3):
    # # Initialize the game board as a list of empty strings (representing empty positions)
    initial_state = [''] * (grid_size * grid_size)
    game = Game(
        player_x_id=player_x_id,
        player_o_id=player_o_id, # Player 'O' ID (optional, could be AI if not provided)
        grid_size=grid_size,
        state=json.dumps(initial_state), #Serialize the game state (list) to JSON
        current_turn='X'
    )
    return game

# New helper function to play against AI
def ai_move(game_state, grid_size):
    ai = TicTacToeAI(grid_size)
    return ai.make_move(game_state)

# New helper function to handle game state updates after a move
def handle_game_state_update(game, updated_state):
    game.state = json.dumps(updated_state) #store the state in the database as a string format.
    db.session.commit()
    return game


