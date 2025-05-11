from board import GomokuBoard
from players.human import HumanPlayer
from players.minimax_ai import MinimaxAI
from players.alphabeta_ai import AlphaBetaAI

def run_game():
    """Main game loop for human vs AI or AI vs AI"""
    # Initialize board and players
    # Game loop handling turns