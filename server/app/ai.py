import random

class TicTacToeAI:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def make_move(self, current_state):
        available_positions = [i for i, cell in enumerate(current_state) if cell == '']
        if available_positions:
            return random.choice(available_positions)
        return None
