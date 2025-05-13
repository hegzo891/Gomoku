import math
import time
from board import is_full, is_win
from utils.constants import AI, HUMAN, EMPTY
from utils.evaluator import utility


class AlphaBetaAI:
    def __init__(self, depth_limit=3):
        self.depth_limit = depth_limit

    def get_move(self, board):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for depth in range(1, self.depth_limit + 1):
            score, move = self.alphabeta(board, depth, alpha, beta, True)
            if move:
                best_move = move
        return best_move

    def alphabeta(self, board, depth, alpha, beta, maximizing):
        if is_win(board, HUMAN) or is_win(board, AI) or is_full(board) or depth == 0:
            return utility(board), None

        valid_moves = board.get_available_moves()
        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                row, col = move
                board.board[row][col] = AI
                eval, _ = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.board[row][col] = EMPTY

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                row, col = move
                board.board[row][col] = HUMAN
                eval, _ = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.board[row][col] = EMPTY

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move