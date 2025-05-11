from utils.evaluator import evaluate_board

class AlphaBetaAI:
    def get_move(self, board): ...  # Uses alpha-beta pruning
    def alphabeta(self, board, depth, alpha, beta, maximizing): ...