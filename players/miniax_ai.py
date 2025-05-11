from utils.evaluator import evaluate_board

class MinimaxAI:
    def get_move(self, board): ...  # Uses minimax algorithm
    def minimax(self, board, depth, maximizing): ...