
import random

class TicTacToeAI:
    """
    A simple random AI player for Tic-Tac-Toe.
    """

    def __init__(self, grid_size):
        """
        Initializes the AI player with the given grid size.

        Args:
            grid_size (int): The size of the Tic-Tac-Toe grid.
        """
        self.grid_size = grid_size

    def make_move(self, current_state):
        """
        Makes a move for the AI player.

        Args:
            current_state (list): The current state of the Tic-Tac-Toe game board, represented as a list of strings ('X', 'O', or '').

        Returns:
            int: The index of the chosen move, or None if there are no available moves.
        """

        # Find available positions on the board
        available_positions = [i for i, cell in enumerate(current_state) if cell == '']

        # Check if there are any available moves
        if available_positions:
            # Choose a random available position
            return random.choice(available_positions)
        else:
            # If there are no available moves, return None
            return None