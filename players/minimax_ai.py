import math
import time
from board import is_full, is_win
from utils.constants import AI, HUMAN, EMPTY
from utils.evaluator import utility

class MinimaxAI:
    def __init__(self, depth_limit=2):
        self.depth_limit = depth_limit

    def get_move(self, board,):
        best_score = -math.inf
        best_move = None

        for depth in range(1, self.depth_limit + 1):
            _, move = self.minimax(board, depth, True, time.time())  
            if move:
                best_move = move
        return best_move

    def minimax(self, board, depth, maximizing, start_time, time_limit=3):
        if is_win(board, HUMAN) or is_win(board, AI) or is_full(board) or depth == 0:
            return utility(board), None

        valid_moves = board.get_available_moves()
        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                row, col = move
                board.board[row][col] = AI  # make move
                eval, _ = self.minimax(board, depth - 1, False, start_time, time_limit)
                board.board[row][col] = EMPTY  # undo move
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                row, col = move
                board.board[row][col] = HUMAN  # make move
                eval, _ = self.minimax(board, depth - 1, True, start_time, time_limit)
                board.board[row][col] = EMPTY  # undo move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
